# API Gateway & Cognito

> **In plain English:** API Gateway is the "front door" for your APIs — it receives HTTP requests from the internet and routes them to Lambda (or another backend), handling throttling, caching, and auth checks along the way. Cognito is AWS's user login system — sign-up, sign-in, password reset, and issuing tokens, so you don't have to build authentication from scratch.

## Real-world analogy

- **API Gateway** = the reception desk of an office building — every visitor (HTTP request) checks in here first. The receptionist checks ID (auth), applies visitor limits (throttling), and directs people to the right department (Lambda function/backend).
- **Resource & Method** = the department name (`/users`) and the specific action there (`GET`, `POST`).
- **Lambda Proxy Integration** = the receptionist hands the *entire* visitor form (raw request) straight to the department, letting the department (your Lambda code) decide what to do with every detail, instead of the receptionist pre-sorting it.
- **Lambda Authorizer** = a security guard who checks a badge (token) before letting anyone reach the receptionist at all.
- **Cognito User Pool** = the company's HR system — handles employee (user) sign-up, login, password resets, and issues ID badges (JWT tokens).
- **Cognito Identity Pool** = a badge-exchange desk — trades your HR ID badge (Cognito/Google/Facebook login) for temporary AWS access keys, so your app itself can call other AWS services (like S3) directly.
- **Usage Plan + API Key** = a punch-card system for external partners — limits how many times they can visit per month.

## Core concepts (memorize these first)

| Term | What it means |
|---|---|
| **REST API vs HTTP API** | REST API = older, full-featured (request validation, usage plans, more integrations). HTTP API = newer, cheaper, faster, but fewer features — pick HTTP API unless you specifically need something only REST API offers. |
| **Resource** | A URL path segment (e.g. `/users`). |
| **Method** | An HTTP verb on a resource (`GET /users`). |
| **Lambda Proxy Integration** | Passes the whole raw HTTP request to Lambda and expects a specific response shape back — most common/flexible setup. |
| **Lambda Authorizer** | A Lambda function that runs *before* your main function, validating a token and returning an Allow/Deny IAM policy. |
| **Request Validation** | API Gateway rejects malformed requests (using a JSON Schema model) before your Lambda even runs — saves compute and simplifies your code. |
| **Usage Plan + API Key** | Throttling/quota rules tied to an API key — used to give different partners different rate limits. |
| **Caching** | API Gateway can cache responses per-method for a TTL, reducing backend load for repeat identical requests. |
| **Cognito User Pool** | The actual identity store — sign-up, sign-in, MFA, password policies; issues JWT tokens (ID token, Access token, Refresh token). |
| **Cognito Identity Pool** | Exchanges a login (from a User Pool or a 3rd party like Google) for *temporary AWS credentials* — used when your frontend needs to call AWS services directly. |
| **JWT (JSON Web Token)** | A signed token proving who the user is; API Gateway/your backend can verify its signature without calling Cognito on every request. |

**Interview-favorite distinction:** User Pool vs Identity Pool. User Pool = "who is this person" (authentication, login). Identity Pool = "what temporary AWS permissions does this person get" (authorization to AWS resources). You often use both together: User Pool authenticates, Identity Pool then hands out scoped AWS credentials.

## Memory hooks

- **"User Pool = login desk. Identity Pool = AWS keys desk."**
- **Lambda Authorizer runs *before* your Lambda — it's a bouncer, not the party.**
- REST API = more features, pricier. HTTP API = leaner, cheaper, faster — default to HTTP API unless you need something REST-only (like usage plans/API keys or request validation models).

---

## API Gateway REST API

The manual, step-by-step way to wire up a REST API: create the API, add a resource (path), add a method (verb), integrate it with Lambda, then deploy to a stage.

```bash
# Create REST API
aws apigateway create-rest-api \
  --name "My API" \
  --description "Production API"

# Get root resource
aws apigateway get-resources --rest-api-id abc123

# Create resource
aws apigateway create-resource \
  --rest-api-id abc123 \
  --parent-id xyz789 \
  --path-part users

# Create method
aws apigateway put-method \
  --rest-api-id abc123 \
  --resource-id def456 \
  --http-method GET \
  --authorization-type NONE

# Create integration
aws apigateway put-integration \
  --rest-api-id abc123 \
  --resource-id def456 \
  --http-method GET \
  --type AWS_PROXY \
  --integration-http-method POST \
  --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:123456789012:function:MyFunction/invocations

# Deploy API
aws apigateway create-deployment \
  --rest-api-id abc123 \
  --stage-name prod
```

## API Gateway with Lambda

With proxy integration, your Lambda receives the entire raw request (method, path, headers, body, params) and must return a specific response shape (`statusCode`, `headers`, `body`) — you do all the routing logic yourself inside the function.

```javascript
// Lambda function for API Gateway
export const handler = async (event) => {
  console.log("Event:", JSON.stringify(event));

  const { httpMethod, path, body, queryStringParameters, pathParameters } =
    event;

  // CORS headers
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
  };

  try {
    // Handle different routes
    if (httpMethod === "GET" && path === "/users") {
      const users = await getUsers();
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(users),
      };
    }

    if (httpMethod === "GET" && path.startsWith("/users/")) {
      const userId = pathParameters.id;
      const user = await getUserById(userId);

      if (!user) {
        return {
          statusCode: 404,
          headers,
          body: JSON.stringify({ error: "User not found" }),
        };
      }

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(user),
      };
    }

    if (httpMethod === "POST" && path === "/users") {
      const userData = JSON.parse(body);
      const user = await createUser(userData);

      return {
        statusCode: 201,
        headers,
        body: JSON.stringify(user),
      };
    }

    return {
      statusCode: 404,
      headers,
      body: JSON.stringify({ error: "Route not found" }),
    };
  } catch (error) {
    console.error("Error:", error);

    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: "Internal server error" }),
    };
  }
};
```

## Request Validation

A JSON Schema attached to a method — API Gateway rejects bad requests automatically (missing required fields, wrong types) before your Lambda code ever runs.

```json
// Request model
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "title": "CreateUserRequest",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "email": {
      "type": "string",
      "format": "email"
    },
    "age": {
      "type": "integer",
      "minimum": 18,
      "maximum": 120
    }
  },
  "required": ["name", "email"]
}
```

## Lambda Authorizer

Runs *before* your main Lambda — validates a token and returns an IAM policy document (Allow/Deny) for that specific request. Anything returned in `context` becomes available to your downstream Lambda via `event.requestContext.authorizer`.

```javascript
// Custom authorizer
export const handler = async (event) => {
  const token = event.authorizationToken;

  try {
    // Validate token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    // Generate policy
    return generatePolicy(decoded.userId, "Allow", event.methodArn, decoded);
  } catch (error) {
    return generatePolicy("user", "Deny", event.methodArn);
  }
};

const generatePolicy = (principalId, effect, resource, context = {}) => {
  return {
    principalId,
    policyDocument: {
      Version: "2012-10-17",
      Statement: [
        {
          Action: "execute-api:Invoke",
          Effect: effect,
          Resource: resource,
        },
      ],
    },
    context, // Available in Lambda as event.requestContext.authorizer
  };
};

// Access authorizer context in Lambda
export const handler = async (event) => {
  const userId = event.requestContext.authorizer.userId;
  const user = await getUser(userId);
  return {
    statusCode: 200,
    body: JSON.stringify(user),
  };
};
```

## API Gateway Caching

Caches a method's response for a TTL so repeat identical requests don't hit your backend/Lambda at all — reduces cost and latency for read-heavy, rarely-changing endpoints.

```bash
# Enable caching
aws apigateway update-stage \
  --rest-api-id abc123 \
  --stage-name prod \
  --patch-operations \
    op=replace,path=/cacheClusterEnabled,value=true \
    op=replace,path=/cacheClusterSize,value=0.5

# Cache per method
aws apigateway update-method \
  --rest-api-id abc123 \
  --resource-id def456 \
  --http-method GET \
  --patch-operations \
    op=replace,path=/caching/enabled,value=true \
    op=replace,path=/caching/ttlInSeconds,value=300
```

## API Gateway Throttling

A Usage Plan ties rate limits + monthly quotas to an API Key — the standard way to give different external partners different access tiers ("Basic Plan" vs "Premium Plan").

```bash
# Set usage plan
aws apigateway create-usage-plan \
  --name "Basic Plan" \
  --throttle burstLimit=100,rateLimit=50 \
  --quota limit=10000,period=MONTH

# Create API key
aws apigateway create-api-key \
  --name "Client1Key" \
  --enabled

# Associate key with usage plan
aws apigateway create-usage-plan-key \
  --usage-plan-id abc123 \
  --key-id def456 \
  --key-type API_KEY
```

## Cognito User Pool

The identity store — handles sign-up, sign-in, verification, and password policy. `--generate-secret` is used when the client is a confidential backend app (not a public frontend/mobile app, which shouldn't hold a secret).

```bash
# Create user pool
aws cognito-idp create-user-pool \
  --pool-name MyUserPool \
  --auto-verified-attributes email \
  --mfa-configuration OPTIONAL \
  --password-policy MinimumLength=8,RequireUppercase=true,RequireLowercase=true,RequireNumbers=true

# Create user pool client
aws cognito-idp create-user-pool-client \
  --user-pool-id us-east-1_ABC123 \
  --client-name MyApp \
  --generate-secret

# Create user
aws cognito-idp admin-create-user \
  --user-pool-id us-east-1_ABC123 \
  --username john@example.com \
  --user-attributes Name=email,Value=john@example.com
```

## Cognito Authentication

The standard sign-up → confirm → sign-in flow, plus password reset. Sign-in returns three tokens: **Access token** (for calling APIs), **ID token** (contains user identity info), **Refresh token** (get new tokens without re-entering a password).

```javascript
import {
  CognitoIdentityProviderClient,
  InitiateAuthCommand,
  SignUpCommand,
  ConfirmSignUpCommand,
  ForgotPasswordCommand,
  ConfirmForgotPasswordCommand,
} from "@aws-sdk/client-cognito-identity-provider";

const cognito = new CognitoIdentityProviderClient({ region: "us-east-1" });
const clientId = "your-client-id";

// Sign up
const signUp = async (email, password) => {
  const command = new SignUpCommand({
    ClientId: clientId,
    Username: email,
    Password: password,
    UserAttributes: [{ Name: "email", Value: email }],
  });

  const response = await cognito.send(command);
  return response.UserSub;
};

// Confirm sign up
const confirmSignUp = async (email, code) => {
  const command = new ConfirmSignUpCommand({
    ClientId: clientId,
    Username: email,
    ConfirmationCode: code,
  });

  await cognito.send(command);
};

// Sign in
const signIn = async (email, password) => {
  const command = new InitiateAuthCommand({
    AuthFlow: "USER_PASSWORD_AUTH",
    ClientId: clientId,
    AuthParameters: {
      USERNAME: email,
      PASSWORD: password,
    },
  });

  const response = await cognito.send(command);
  return {
    accessToken: response.AuthenticationResult.AccessToken,
    idToken: response.AuthenticationResult.IdToken,
    refreshToken: response.AuthenticationResult.RefreshToken,
  };
};

// Refresh token
const refreshToken = async (refreshToken) => {
  const command = new InitiateAuthCommand({
    AuthFlow: "REFRESH_TOKEN_AUTH",
    ClientId: clientId,
    AuthParameters: {
      REFRESH_TOKEN: refreshToken,
    },
  });

  const response = await cognito.send(command);
  return {
    accessToken: response.AuthenticationResult.AccessToken,
    idToken: response.AuthenticationResult.IdToken,
  };
};

// Forgot password
const forgotPassword = async (email) => {
  const command = new ForgotPasswordCommand({
    ClientId: clientId,
    Username: email,
  });

  await cognito.send(command);
};

// Confirm forgot password
const confirmForgotPassword = async (email, code, newPassword) => {
  const command = new ConfirmForgotPasswordCommand({
    ClientId: clientId,
    Username: email,
    ConfirmationCode: code,
    Password: newPassword,
  });

  await cognito.send(command);
};
```

## API Gateway with Cognito

API Gateway can validate a Cognito JWT directly (as the `DefaultAuthorizer`) without you writing any custom authorizer Lambda code at all — the simplest way to protect an API with Cognito.

```yaml
# SAM template
Resources:
  MyApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: prod
      Auth:
        DefaultAuthorizer: MyCognitoAuthorizer
        Authorizers:
          MyCognitoAuthorizer:
            UserPoolArn: !GetAtt UserPool.Arn

  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.handler
      Runtime: nodejs18.x
      Events:
        GetUsers:
          Type: Api
          Properties:
            RestApiId: !Ref MyApi
            Path: /users
            Method: GET
```

If you're validating the JWT yourself (e.g. in a custom authorizer or a non-API-Gateway backend), you verify its signature against Cognito's public JWKS endpoint:

```javascript
// Verify Cognito JWT in Lambda
import jwt from "jsonwebtoken";
import jwksClient from "jwks-rsa";

const client = jwksClient({
  jwksUri: `https://cognito-idp.us-east-1.amazonaws.com/${process.env.USER_POOL_ID}/.well-known/jwks.json`,
});

const getKey = (header, callback) => {
  client.getSigningKey(header.kid, (err, key) => {
    const signingKey = key.getPublicKey();
    callback(null, signingKey);
  });
};

const verifyToken = (token) => {
  return new Promise((resolve, reject) => {
    jwt.verify(
      token,
      getKey,
      {
        issuer: `https://cognito-idp.us-east-1.amazonaws.com/${process.env.USER_POOL_ID}`,
        audience: process.env.CLIENT_ID,
      },
      (err, decoded) => {
        if (err) reject(err);
        else resolve(decoded);
      }
    );
  });
};

export const handler = async (event) => {
  try {
    const token = event.headers.Authorization.replace("Bearer ", "");
    const decoded = await verifyToken(token);

    // Access user info
    const userId = decoded.sub;
    const email = decoded.email;

    return {
      statusCode: 200,
      body: JSON.stringify({ userId, email }),
    };
  } catch (error) {
    return {
      statusCode: 401,
      body: JSON.stringify({ error: "Unauthorized" }),
    };
  }
};
```

## Cognito Identity Pool

Trades a login (from a User Pool, or Google/Facebook/etc) for temporary AWS credentials — used when your frontend app itself needs to call AWS services directly (e.g. upload straight to S3) without proxying through your backend.

```bash
# Create identity pool
aws cognito-identity create-identity-pool \
  --identity-pool-name MyIdentityPool \
  --allow-unauthenticated-identities false \
  --cognito-identity-providers \
    ProviderName=cognito-idp.us-east-1.amazonaws.com/us-east-1_ABC123,ClientId=client-id
```

```javascript
// Get temporary AWS credentials
import {
  CognitoIdentityClient,
  GetIdCommand,
  GetCredentialsForIdentityCommand,
} from "@aws-sdk/client-cognito-identity";

const getAWSCredentials = async (idToken) => {
  const cognitoIdentity = new CognitoIdentityClient({ region: "us-east-1" });

  // Get identity ID
  const getIdCommand = new GetIdCommand({
    IdentityPoolId: "us-east-1:abc-123",
    Logins: {
      [`cognito-idp.us-east-1.amazonaws.com/${userPoolId}`]: idToken,
    },
  });

  const { IdentityId } = await cognitoIdentity.send(getIdCommand);

  // Get credentials
  const getCredsCommand = new GetCredentialsForIdentityCommand({
    IdentityId,
    Logins: {
      [`cognito-idp.us-east-1.amazonaws.com/${userPoolId}`]: idToken,
    },
  });

  const { Credentials } = await cognitoIdentity.send(getCredsCommand);

  return {
    accessKeyId: Credentials.AccessKeyId,
    secretAccessKey: Credentials.SecretKey,
    sessionToken: Credentials.SessionToken,
  };
};
```

---

## Quick interview answers

**Q: Cognito User Pool vs Identity Pool?**
User Pool = authentication (who is this person — sign-up/sign-in/tokens). Identity Pool = authorization to AWS (temporary AWS credentials, scoped by IAM role, exchanged for a valid login). Often used together: User Pool logs someone in, Identity Pool then gives their app temporary AWS access.

**Q: REST API vs HTTP API in API Gateway?**
HTTP API is newer, cheaper, and lower-latency but has a smaller feature set. REST API supports more advanced features (usage plans/API keys, request validation, more integration types). Default to HTTP API unless you specifically need a REST-only feature.

**Q: What does a Lambda Authorizer actually return?**
An IAM policy document (Allow/Deny) for the specific request, plus an optional `context` object that gets passed through to your main Lambda so it doesn't have to re-validate the token.

**Q: Access token vs ID token vs Refresh token (Cognito)?**
Access token: used to call APIs/authorize requests. ID token: carries identity claims about the user (email, name, etc) for the client app to use. Refresh token: used to get new Access/ID tokens without asking the user to log in again.

**Q: Why validate a JWT's signature against a JWKS endpoint instead of trusting it as-is?**
Anyone can craft a fake JWT-looking string; verifying the cryptographic signature against Cognito's published public keys (JWKS) proves the token was genuinely issued by Cognito and hasn't been tampered with.

**Q: When would you need a Cognito Identity Pool instead of just using your backend as a proxy to AWS?**
When the frontend itself needs direct, scoped access to an AWS service (e.g., browser uploading straight to S3) without round-tripping every request through your backend server.
