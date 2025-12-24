# API Gateway & Cognito

## API Gateway REST API

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
