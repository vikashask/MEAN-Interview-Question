# AWS CLI & SDKs

## AWS CLI Configuration

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
