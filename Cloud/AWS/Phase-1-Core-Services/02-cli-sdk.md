# AWS CLI & SDKs

> **In plain English:** The CLI is a command-line tool for talking to AWS from your terminal. The SDK is the same idea but from inside your code (Node.js, Python, etc). Both do the exact same thing under the hood — call AWS's HTTP APIs — just with different front doors.

## Real-world analogy

Imagine AWS as a giant vending machine with thousands of buttons (APIs).

- **AWS Console** = pressing buttons by hand, one click at a time (good for exploring, bad for repeating).
- **AWS CLI** = a remote control you type commands into — same buttons, but scriptable.
- **AWS SDK** = wiring the vending machine directly into your app, so your code presses the buttons itself.

Whichever front door you use, IAM still checks your badge before anything happens.

## Core concepts (memorize these first)

| Term | What it means |
|---|---|
| **Profile** | A named set of saved credentials (`aws configure --profile X`), so you can switch between accounts without retyping keys. |
| **Region** | Which AWS data center location your commands target (`us-east-1`, `ap-south-1`...). Most services are region-scoped. |
| **JMESPath (`--query`)** | A mini query language to filter/shape the JSON that CLI commands return, instead of dumping everything. |
| **Pagination** | AWS APIs return results in pages (e.g. max 1000 S3 objects per call) — you must loop using a "continuation token" to get everything. |
| **Exponential backoff** | If a request fails (e.g. throttled), wait a little, retry, wait longer, retry again — instead of hammering the API. SDKs do this automatically. |
| **SDK v3 (JS)** | The current AWS SDK for JavaScript — modular (`@aws-sdk/client-s3` etc, install only what you use) vs old SDK v2 which was one giant package. |

## Memory hooks

- **Profile = "which account am I."** Region = "which building am I calling."
- CLI output formats to remember: `json` (default, machine-friendly), `table` (human-friendly), `text` (script-friendly, easy to pipe into `grep`/`awk`).
- **"Send a Command"** — in SDK v3, everything is `new XCommand({...})` then `client.send(command)`. Same pattern for every AWS service.

---

## AWS CLI Configuration

First thing you always do on a new machine — tell the CLI which keys and region to use.

```bash
# Configure AWS CLI
aws configure
# AWS Access Key ID: YOUR_ACCESS_KEY
# AWS Secret Access Key: YOUR_SECRET_KEY
# Default region name: us-east-1
# Default output format: json

# Configure named profile
aws configure --profile production

# List profiles
aws configure list-profiles

# Use specific profile
aws s3 ls --profile production

# Set environment variables
export AWS_PROFILE=production
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=YOUR_KEY
export AWS_SECRET_ACCESS_KEY=YOUR_SECRET
```

## Common AWS CLI Commands

These are the everyday "read/list/start/stop" commands you'll type constantly for each service. Notice the pattern: `aws <service> <verb>-<noun>`.

```bash
# S3
aws s3 ls
aws s3 cp file.txt s3://my-bucket/
aws s3 sync ./local-dir s3://my-bucket/remote-dir/
aws s3 rm s3://my-bucket/file.txt

# EC2
aws ec2 describe-instances
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# Lambda
aws lambda list-functions
aws lambda invoke --function-name MyFunction output.json
aws lambda update-function-code \
  --function-name MyFunction \
  --zip-file fileb://function.zip

# DynamoDB
aws dynamodb list-tables
aws dynamodb get-item \
  --table-name Users \
  --key '{"id": {"S": "123"}}'
aws dynamodb put-item \
  --table-name Users \
  --item '{"id": {"S": "123"}, "name": {"S": "John"}}'

# CloudWatch Logs
aws logs describe-log-groups
aws logs tail /aws/lambda/MyFunction --follow
aws logs filter-log-events \
  --log-group-name /aws/lambda/MyFunction \
  --filter-pattern "ERROR"
```

## AWS CLI Query & Filters

`--query` uses JMESPath to pick out exactly the fields you want from a big JSON response, so you don't have to eyeball a huge dump.

```bash
# JMESPath queries
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].[InstanceId,State.Name,PrivateIpAddress]' \
  --output table

# Filter by tag
aws ec2 describe-instances \
  --filters "Name=tag:Environment,Values=production" \
  --query 'Reservations[*].Instances[*].InstanceId'

# Get specific fields
aws s3api list-buckets \
  --query 'Buckets[?CreationDate>=`2024-01-01`].Name'

# Output as text
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].InstanceId' \
  --output text
```

## AWS SDK for JavaScript (v3)

SDK v3 is modular — install only the client packages you actually need (`client-s3`, `client-dynamodb`...) instead of one giant SDK. The pattern is always: build a client → build a command object → `client.send(command)`.

```javascript
// Install
npm install @aws-sdk/client-s3 @aws-sdk/client-dynamodb

// S3 Client
import { S3Client, PutObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3';

const s3Client = new S3Client({ region: 'us-east-1' });

// Upload file
const uploadParams = {
  Bucket: 'my-bucket',
  Key: 'file.txt',
  Body: 'Hello World'
};

const uploadCommand = new PutObjectCommand(uploadParams);
const uploadResult = await s3Client.send(uploadCommand);

// Download file
const downloadParams = {
  Bucket: 'my-bucket',
  Key: 'file.txt'
};

const downloadCommand = new GetObjectCommand(downloadParams);
const downloadResult = await s3Client.send(downloadCommand);
const fileContent = await downloadResult.Body.transformToString();

// List objects
import { ListObjectsV2Command } from '@aws-sdk/client-s3';

const listCommand = new ListObjectsV2Command({
  Bucket: 'my-bucket',
  Prefix: 'folder/'
});

const listResult = await s3Client.send(listCommand);
console.log(listResult.Contents);
```

## DynamoDB SDK

`DynamoDBDocumentClient` wraps the raw client so you can send/receive plain JS objects instead of DynamoDB's verbose `{ "S": "value" }` typed format.

```javascript
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  PutCommand,
  GetCommand,
  QueryCommand,
  UpdateCommand,
  DeleteCommand,
} from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({ region: "us-east-1" });
const docClient = DynamoDBDocumentClient.from(client);

// Put item
const putCommand = new PutCommand({
  TableName: "Users",
  Item: {
    id: "123",
    name: "John Doe",
    email: "john@example.com",
  },
});

await docClient.send(putCommand);

// Get item
const getCommand = new GetCommand({
  TableName: "Users",
  Key: { id: "123" },
});

const { Item } = await docClient.send(getCommand);

// Query
const queryCommand = new QueryCommand({
  TableName: "Users",
  KeyConditionExpression: "id = :id",
  ExpressionAttributeValues: {
    ":id": "123",
  },
});

const { Items } = await docClient.send(queryCommand);

// Update
const updateCommand = new UpdateCommand({
  TableName: "Users",
  Key: { id: "123" },
  UpdateExpression: "SET #name = :name",
  ExpressionAttributeNames: { "#name": "name" },
  ExpressionAttributeValues: { ":name": "Jane Doe" },
});

await docClient.send(updateCommand);

// Delete
const deleteCommand = new DeleteCommand({
  TableName: "Users",
  Key: { id: "123" },
});

await docClient.send(deleteCommand);
```

## Lambda SDK

```javascript
import { LambdaClient, InvokeCommand } from "@aws-sdk/client-lambda";

const lambdaClient = new LambdaClient({ region: "us-east-1" });

// Invoke Lambda function
const invokeCommand = new InvokeCommand({
  FunctionName: "MyFunction",
  Payload: JSON.stringify({ key: "value" }),
});

const response = await lambdaClient.send(invokeCommand);
const result = JSON.parse(Buffer.from(response.Payload).toString());
```

## Error Handling

Every SDK v3 service error extends a `<Service>ServiceException` class. Check `error.name` for the specific error type (e.g. `NoSuchKey`, `AccessDenied`) to react differently per failure.

```javascript
import { S3ServiceException } from "@aws-sdk/client-s3";

try {
  await s3Client.send(command);
} catch (error) {
  if (error instanceof S3ServiceException) {
    console.error("S3 Error:", error.message);
    console.error("Status Code:", error.$metadata.httpStatusCode);
    console.error("Request ID:", error.$metadata.requestId);
  }

  // Handle specific errors
  if (error.name === "NoSuchKey") {
    console.error("Object not found");
  } else if (error.name === "AccessDenied") {
    console.error("Access denied");
  }
}
```

## Pagination

AWS never hands you a million records in one response — it caps each page and gives you a token to fetch the next page. Two ways to handle it: let the SDK's built-in paginator loop for you, or do it manually.

```javascript
import { paginateListObjects } from "@aws-sdk/client-s3";

// Automatic pagination
const paginator = paginateListObjects(
  { client: s3Client },
  { Bucket: "my-bucket" }
);

for await (const page of paginator) {
  console.log(page.Contents);
}

// Manual pagination
let continuationToken;
do {
  const command = new ListObjectsV2Command({
    Bucket: "my-bucket",
    ContinuationToken: continuationToken,
  });

  const response = await s3Client.send(command);
  console.log(response.Contents);
  continuationToken = response.NextContinuationToken;
} while (continuationToken);
```

## Retry & Exponential Backoff

If AWS throttles you (too many requests), the SDK automatically waits and retries with increasing delay instead of failing immediately. You rarely need to write this by hand — just configure `maxAttempts`.

```javascript
import { S3Client } from "@aws-sdk/client-s3";

const s3Client = new S3Client({
  region: "us-east-1",
  maxAttempts: 3,
  retryMode: "adaptive",
});

// Custom retry strategy
const customRetry = (attempt) => {
  const delay = Math.min(1000 * Math.pow(2, attempt), 10000);
  return new Promise((resolve) => setTimeout(resolve, delay));
};
```

## Environment-Specific Configuration

Point the SDK at LocalStack (a fake local AWS) in dev, and real AWS in production, using the same code.

```javascript
// config.js
const config = {
  development: {
    region: "us-east-1",
    endpoint: "http://localhost:4566", // LocalStack
  },
  production: {
    region: "us-east-1",
  },
};

const env = process.env.NODE_ENV || "development";

export const awsConfig = config[env];

// Usage
import { S3Client } from "@aws-sdk/client-s3";
import { awsConfig } from "./config";

const s3Client = new S3Client(awsConfig);
```

---

## Quick interview answers

**Q: CLI vs SDK — when to use which?**
CLI for one-off/manual/scripted ops tasks (deploy scripts, debugging). SDK when your application code itself needs to talk to AWS at runtime.

**Q: How does the CLI/SDK find credentials if you don't pass any?**
A fixed lookup order: explicit code config → environment variables → shared credentials file (`~/.aws/credentials`) → EC2/ECS/Lambda instance role. This is called the "credential provider chain."

**Q: Why does AWS paginate responses?**
Performance and safety — returning millions of records in one call would be slow and memory-heavy. You loop using a continuation/next token instead.

**Q: What is exponential backoff and why does it matter?**
A retry strategy where wait time doubles each failed attempt. It matters because hammering a throttled API with instant retries makes the throttling worse ("thundering herd").
