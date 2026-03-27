# EC2 & Lambda

## EC2 Instance Management

```bash
# Launch instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name my-key-pair \
  --security-group-ids sg-0123456789abcdef0 \
  --subnet-id subnet-0123456789abcdef0 \
  --user-data file://user-data.sh \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyInstance}]'

# Start/Stop instances
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
aws ec2 reboot-instances --instance-ids i-1234567890abcdef0

# Describe instances
aws ec2 describe-instances \
  --filters "Name=tag:Environment,Values=production" \
  --query 'Reservations[*].Instances[*].[InstanceId,State.Name,PublicIpAddress]'

# Create AMI from instance
aws ec2 create-image \
  --instance-id i-1234567890abcdef0 \
  --name "MyAMI-$(date +%Y%m%d)" \
  --description "Production AMI"
```

## User Data Script

```bash
#!/bin/bash
# Update system
yum update -y

# Install Node.js
curl -sL https://rpm.nodesource.com/setup_18.x | bash -
yum install -y nodejs

# Install application
cd /home/ec2-user
git clone https://github.com/user/app.git
cd app
npm install
npm start &
```

## Auto Scaling with SDK

```javascript
import {
  AutoScalingClient,
  CreateAutoScalingGroupCommand,
  PutScalingPolicyCommand,
} from "@aws-sdk/client-auto-scaling";

const asgClient = new AutoScalingClient({ region: "us-east-1" });

// Create Auto Scaling Group
const createASG = async () => {
  const command = new CreateAutoScalingGroupCommand({
    AutoScalingGroupName: "my-asg",
    MinSize: 2,
    MaxSize: 10,
    DesiredCapacity: 2,
    LaunchTemplate: {
      LaunchTemplateId: "lt-0123456789abcdef0",
      Version: "$Latest",
    },
    VPCZoneIdentifier: "subnet-12345,subnet-67890",
    TargetGroupARNs: ["arn:aws:elasticloadbalancing:..."],
    HealthCheckType: "ELB",
    HealthCheckGracePeriod: 300,
  });

  await asgClient.send(command);
};

// Create scaling policy
const createScalingPolicy = async () => {
  const command = new PutScalingPolicyCommand({
    AutoScalingGroupName: "my-asg",
    PolicyName: "scale-up-policy",
    PolicyType: "TargetTrackingScaling",
    TargetTrackingConfiguration: {
      PredefinedMetricSpecification: {
        PredefinedMetricType: "ASGAverageCPUUtilization",
      },
      TargetValue: 70.0,
    },
  });

  await asgClient.send(command);
};
```

## Lambda Functions

```bash
# Create function
aws lambda create-function \
  --function-name MyFunction \
  --runtime nodejs18.x \
  --role arn:aws:iam::123456789012:role/lambda-execution-role \
  --handler index.handler \
  --zip-file fileb://function.zip \
  --timeout 30 \
  --memory-size 512 \
  --environment Variables={NODE_ENV=production,DB_HOST=localhost}

# Update function code
aws lambda update-function-code \
  --function-name MyFunction \
  --zip-file fileb://function.zip

# Update configuration
aws lambda update-function-configuration \
  --function-name MyFunction \
  --timeout 60 \
  --memory-size 1024 \
  --environment Variables={NODE_ENV=production,API_KEY=secret}

# Invoke function
aws lambda invoke \
  --function-name MyFunction \
  --payload '{"key":"value"}' \
  response.json

# List functions
aws lambda list-functions

# Delete function
aws lambda delete-function --function-name MyFunction
```

## Lambda Function Code

```javascript
// index.js - Basic handler
export const handler = async (event, context) => {
  console.log("Event:", JSON.stringify(event));

  try {
    const result = await processEvent(event);

    return {
      statusCode: 200,
      body: JSON.stringify(result),
    };
  } catch (error) {
    console.error("Error:", error);

    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message }),
    };
  }
};

// API Gateway proxy integration
export const handler = async (event) => {
  const { httpMethod, path, body } = event;

  if (httpMethod === "GET" && path === "/users") {
    const users = await getUsers();
    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(users),
    };
  }

  if (httpMethod === "POST" && path === "/users") {
    const user = JSON.parse(body);
    const created = await createUser(user);
    return {
      statusCode: 201,
      body: JSON.stringify(created),
    };
  }

  return {
    statusCode: 404,
    body: JSON.stringify({ message: "Not found" }),
  };
};

// S3 event handler
export const handler = async (event) => {
  for (const record of event.Records) {
    const bucket = record.s3.bucket.name;
    const key = decodeURIComponent(record.s3.object.key.replace(/\+/g, " "));

    console.log(`Processing ${bucket}/${key}`);

    // Process file
    await processS3File(bucket, key);
  }
};
```

## Lambda Layers

```bash
# Create layer
zip -r layer.zip nodejs/
aws lambda publish-layer-version \
  --layer-name my-dependencies \
  --zip-file fileb://layer.zip \
  --compatible-runtimes nodejs18.x

# Add layer to function
aws lambda update-function-configuration \
  --function-name MyFunction \
  --layers arn:aws:lambda:us-east-1:123456789012:layer:my-dependencies:1
```

## Lambda SDK Usage

```javascript
import {
  LambdaClient,
  InvokeCommand,
  UpdateFunctionCodeCommand,
} from "@aws-sdk/client-lambda";

const lambda = new LambdaClient({ region: "us-east-1" });

// Invoke Lambda
const invokeFunction = async (functionName, payload) => {
  const command = new InvokeCommand({
    FunctionName: functionName,
    Payload: JSON.stringify(payload),
  });

  const response = await lambda.send(command);
  const result = JSON.parse(Buffer.from(response.Payload).toString());
  return result;
};

// Async invoke (no wait for response)
const invokeAsync = async (functionName, payload) => {
  const command = new InvokeCommand({
    FunctionName: functionName,
    InvocationType: "Event", // Async
    Payload: JSON.stringify(payload),
  });

  await lambda.send(command);
};

// Usage
const result = await invokeFunction("MyFunction", { userId: 123 });
```

## Lambda Cold Start Optimization

```javascript
// Keep connections alive
import { S3Client } from '@aws-sdk/client-s3';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';

// Initialize outside handler (reused across invocations)
const s3Client = new S3Client({ region: process.env.AWS_REGION });
const dynamoClient = new DynamoDBClient({ region: process.env.AWS_REGION });

export const handler = async (event) => {
  // Handler code uses clients above
  // Connections are reused across invocations
};

// Provisioned concurrency
aws lambda put-provisioned-concurrency-config \
  --function-name MyFunction \
  --provisioned-concurrent-executions 5 \
  --qualifier $LATEST
```

## Lambda with VPC

```bash
# Configure VPC
aws lambda update-function-configuration \
  --function-name MyFunction \
  --vpc-config SubnetIds=subnet-12345,subnet-67890,SecurityGroupIds=sg-12345
```

## Step Functions Integration

```javascript
// State machine with Lambda
{
  "Comment": "Process order workflow",
  "StartAt": "ValidateOrder",
  "States": {
    "ValidateOrder": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ValidateOrder",
      "Next": "ProcessPayment"
    },
    "ProcessPayment": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ProcessPayment",
      "Next": "SendConfirmation",
      "Catch": [{
        "ErrorEquals": ["PaymentFailed"],
        "Next": "PaymentError"
      }]
    },
    "SendConfirmation": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:SendEmail",
      "End": true
    },
    "PaymentError": {
      "Type": "Fail",
      "Error": "PaymentFailed",
      "Cause": "Payment processing failed"
    }
  }
}
```
