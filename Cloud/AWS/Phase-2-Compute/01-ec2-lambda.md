# EC2 & Lambda

> **In plain English:** EC2 is "rent a virtual computer, running 24/7, you manage the OS." Lambda is "just give me a function to run, AWS handles the computer, and you pay only while it's actually executing." Both run your code — the difference is who manages what, and how you pay.

## Real-world analogy

- **EC2** = renting an apartment. You get a whole space, you pay rent whether you're home or not, you're responsible for cleaning (patching, OS updates), and you can furnish it however you like (install anything).
- **Lambda** = a hotel room you only pay for by the minute you're actually in it. AWS cleans it, AWS provides it, but you can't customize the walls (limited runtime environment, time limits).
- **Auto Scaling Group** = a property manager that adds/removes apartment units automatically based on how many tenants show up.
- **AMI (Amazon Machine Image)** = a "snapshot blueprint" of a fully furnished apartment you can stamp out copies of instantly.
- **Cold start** = walking into a hotel room that hasn't been prepped yet — first guest waits a bit longer while it's set up; after that it's ready-to-go for a while.

## Core concepts (memorize these first)

| Term | What it means |
|---|---|
| **Instance** | One running virtual machine. |
| **AMI** | The OS + software template used to launch an instance (blueprint). |
| **Instance type** | The hardware size (`t3.micro` = tiny/burstable, `m5.large` = general purpose, etc). |
| **User Data** | A startup script that runs once, automatically, the first time an instance boots. |
| **Auto Scaling Group (ASG)** | Automatically adds/removes instances to match demand, keeps a minimum count alive, replaces unhealthy ones. |
| **Spot / Reserved / On-Demand** | Three ways to pay: Spot = cheapest but AWS can reclaim it anytime (use for non-critical/batch work), Reserved = commit for 1-3 yrs for a discount, On-Demand = pay full price, no commitment. |
| **Lambda function** | A single unit of code that runs in response to a trigger (API call, file upload, schedule, queue message) and then stops. |
| **Cold start** | Extra latency the *first* time a Lambda runs (or after being idle) while AWS provisions its execution environment. |
| **Concurrency** | How many copies of your Lambda can run at the same time. |
| **Provisioned Concurrency** | Pre-warms Lambda environments so you never hit a cold start — costs more, used for latency-sensitive APIs. |
| **Lambda Layer** | Shared code/dependencies packaged separately so multiple functions can reuse them without duplicating. |

**The interview-favorite distinction:** EC2 = you manage the server (patches, scaling, uptime). Lambda = fully serverless, AWS manages the server, you only manage the code — but you're bound by execution time limits (15 min max) and no persistent local state between invocations.

## Memory hooks

- **"EC2 = pets, Lambda = cattle."** Common industry phrase — EC2 instances you often nurse/name/keep alive; Lambda invocations are disposable, identical, replaceable.
- Auto Scaling triad to remember: **Min / Desired / Max** capacity.
- **Cold start fix = keep it warm (Provisioned Concurrency) or keep clients outside the handler** (reuse connections across invocations).

---

## EC2 Instance Management

The core lifecycle commands: launch, start/stop/reboot, inspect, and snapshot into a reusable AMI.

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

Runs automatically, once, the very first time the instance boots — the standard way to install software and start your app without logging in manually.

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

An Auto Scaling Group keeps a set number of healthy instances running and replaces failed ones automatically. A scaling policy tells it *when* to add/remove instances (here: keep average CPU near 70%).

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

Create/update/invoke a function from the CLI. Note: memory size and timeout directly affect both performance and cost.

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

Every Lambda handler follows the same shape: `(event, context) => response`. The `event` shape differs by trigger (API Gateway, S3, etc) — you branch on it.

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

A Layer packages shared code/libraries once, so multiple Lambda functions can attach it instead of each bundling the same dependencies.

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

`InvocationType: "Event"` means "fire and forget" — don't wait for the function to finish, useful for background/async work.

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

A "cold start" happens when AWS has to spin up a fresh execution environment before running your code — this adds latency. Two fixes: (1) initialize expensive things like DB clients *outside* the handler so they're reused across warm invocations, (2) pay for Provisioned Concurrency to keep environments pre-warmed.

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

Putting Lambda inside a VPC lets it reach private resources (like an RDS database in a private subnet) — but adds a small amount of cold-start latency since it needs an ENI (network interface) attached.

```bash
# Configure VPC
aws lambda update-function-configuration \
  --function-name MyFunction \
  --vpc-config SubnetIds=subnet-12345,subnet-67890,SecurityGroupIds=sg-12345
```

## Step Functions Integration

Step Functions chain multiple Lambdas into a workflow/state-machine, with built-in error handling and branching — instead of one Lambda calling another directly.

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

---

## Quick interview answers

**Q: When would you choose EC2 over Lambda?**
Long-running processes (>15 min), workloads needing full OS control/custom binaries, predictable steady traffic (cheaper at scale than Lambda), or apps needing persistent local state/connections.

**Q: When would you choose Lambda over EC2?**
Spiky/unpredictable traffic, event-driven work (file uploads, queue messages, scheduled jobs), and when you don't want to manage servers/patching at all.

**Q: What causes a Lambda cold start and how do you reduce it?**
AWS provisioning a fresh execution environment. Reduce it by: keeping the deployment package small, initializing SDK clients outside the handler, or using Provisioned Concurrency.

**Q: Spot vs Reserved vs On-Demand EC2 pricing?**
Spot = up to ~90% cheaper but can be reclaimed with 2 min notice (good for fault-tolerant/batch jobs). Reserved = commit 1-3 years for a discount (good for steady baseline load). On-Demand = pay-as-you-go, no discount, no commitment (good for unpredictable/short-term needs).

**Q: What does an Auto Scaling Group actually guarantee?**
It keeps the number of *healthy* instances between Min and Max, targeting Desired capacity, replacing any instance that fails its health check.

**Q: Max Lambda execution time?**
15 minutes. Anything longer needs Step Functions, ECS/Fargate, or EC2 instead.
