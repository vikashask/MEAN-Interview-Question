# CloudFormation & AWS CDK

> **In plain English:** Instead of clicking around the AWS Console to create resources by hand, you write down what you want in a file, and AWS builds it for you automatically — this is "Infrastructure as Code" (IaC). CloudFormation is the raw YAML/JSON way. CDK lets you write the same thing using real programming languages (TypeScript, Python), which then compiles down into CloudFormation underneath.

## Real-world analogy

- **CloudFormation template** = a full architectural blueprint handed to a construction crew — every wall, pipe, and wire spelled out explicitly in a fixed format (YAML/JSON).
- **Stack** = one building constructed from that blueprint — if you update the blueprint, CloudFormation figures out what changed and only rebuilds those parts.
- **Change Set** = a "preview of changes" the contractor shows you before touching anything — "here's exactly what will be added/changed/destroyed if you approve this."
- **AWS CDK** = instead of drawing the raw blueprint by hand, you describe the building in a familiar programming language and a translator (the CDK "synth" step) generates the official blueprint (CloudFormation template) for you.
- **CDK Construct** = a pre-fabricated wall unit — someone already figured out the wiring/plumbing best practices, you just say "put one here."

## Core concepts (memorize these first)

| Term | What it means |
|---|---|
| **Template** | The file (YAML/JSON) describing every AWS resource to create. |
| **Stack** | One deployed collection of resources from a template — the unit of deploy/update/delete. |
| **Resource** | One thing being created (`AWS::EC2::VPC`, `AWS::Lambda::Function`, etc). |
| **Parameters** | Inputs you can pass in at deploy time (e.g. environment name) without hardcoding them into the template. |
| **Outputs** | Values exported from a stack (e.g. a VPC ID) so other stacks can reference them. |
| **Intrinsic functions** | Built-in template helpers like `!Ref` (reference a resource/parameter), `!GetAtt` (get an attribute of a resource), `!Sub` (string substitution). |
| **Change Set** | A preview of what an update would actually do, before it's applied — avoids surprise deletions. |
| **Drift Detection** | Finds resources that were manually changed outside of CloudFormation (so the real world no longer matches the template). |
| **Nested Stack** | A stack referenced inside another stack — used to break huge templates into reusable pieces. |
| **CDK Construct** | A reusable, higher-level building block (L1 = raw CloudFormation resource, L2 = AWS-curated with sane defaults, L3/Patterns = whole common architectures like "load-balanced Fargate service"). |
| **`cdk synth`** | Compiles your CDK code into the actual CloudFormation template (without deploying). |
| **`cdk diff`** | Shows what would change if you deployed right now — the CDK equivalent of reviewing a Change Set. |

**Interview-favorite distinction:** CloudFormation = declarative infrastructure directly in YAML/JSON. CDK = the same underlying engine, but you write in TypeScript/Python/etc and get real programming features (loops, conditionals, reusable classes) — CDK always ends up generating a CloudFormation template behind the scenes; it doesn't replace CloudFormation, it generates it.

## Memory hooks

- **"CDK writes the blueprint for you; CloudFormation is the blueprint itself."**
- Update flow to remember: change template → CloudFormation computes a diff → Change Set (preview) → apply → only the changed resources are touched.
- **L1 = raw resource. L2 = smart defaults. L3/Pattern = whole pre-built architecture.** Higher number = more abstraction, less to write.

---

## CloudFormation Template

The typical structure: `Parameters` (inputs) → `Resources` (what to build) → `Outputs` (what to expose to other stacks).

```yaml
# template.yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: "VPC with Public and Private Subnets"

Parameters:
  EnvironmentName:
    Type: String
    Default: production
    AllowedValues:
      - development
      - staging
      - production

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub "${EnvironmentName}-vpc"

  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Sub "${EnvironmentName}-igw"

  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway

  PublicSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs ""]
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub "${EnvironmentName}-public-subnet"

  PrivateSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.2.0/24
      AvailabilityZone: !Select [1, !GetAZs ""]
      Tags:
        - Key: Name
          Value: !Sub "${EnvironmentName}-private-subnet"

Outputs:
  VPCId:
    Description: VPC ID
    Value: !Ref VPC
    Export:
      Name: !Sub "${EnvironmentName}-VPCId"

  PublicSubnetId:
    Description: Public Subnet ID
    Value: !Ref PublicSubnet
    Export:
      Name: !Sub "${EnvironmentName}-PublicSubnetId"
```

## Deploy CloudFormation

`create-stack` for the first deploy, `update-stack` for every change after — CloudFormation compares the new template against what's currently running and only touches what changed.

```bash
# Create stack
aws cloudformation create-stack \
  --stack-name my-vpc-stack \
  --template-body file://template.yaml \
  --parameters ParameterKey=EnvironmentName,ParameterValue=production

# Update stack
aws cloudformation update-stack \
  --stack-name my-vpc-stack \
  --template-body file://template.yaml \
  --parameters ParameterKey=EnvironmentName,ParameterValue=production

# Delete stack
aws cloudformation delete-stack --stack-name my-vpc-stack

# Describe stack
aws cloudformation describe-stacks --stack-name my-vpc-stack

# List stacks
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE
```

## Lambda Function Template

A common real-world pattern: an IAM role, a Lambda function, and a DynamoDB table all defined together in one template, wired together with `!Ref`/`!GetAtt`.

```yaml
Resources:
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: DynamoDBAccess
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - dynamodb:GetItem
                  - dynamodb:PutItem
                  - dynamodb:Query
                Resource: !GetAtt UsersTable.Arn

  MyFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: my-function
      Runtime: nodejs18.x
      Handler: index.handler
      Code:
        ZipFile: |
          exports.handler = async (event) => {
            return {
              statusCode: 200,
              body: JSON.stringify({ message: 'Hello World' })
            };
          };
      Role: !GetAtt LambdaExecutionRole.Arn
      Environment:
        Variables:
          TABLE_NAME: !Ref UsersTable
      Timeout: 30
      MemorySize: 512

  UsersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: Users
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
```

## AWS CDK Setup

```bash
# Install CDK
npm install -g aws-cdk

# Initialize CDK project
mkdir my-cdk-app
cd my-cdk-app
cdk init app --language typescript

# Install dependencies
npm install @aws-cdk/aws-s3 @aws-cdk/aws-lambda @aws-cdk/aws-dynamodb
```

## CDK Stack Example

The same "S3 + DynamoDB + Lambda + API Gateway" setup as a raw CloudFormation template would take much more YAML — here, `table.grantReadWriteData(fn)` auto-generates the correct IAM policy for you, instead of you writing it by hand.

```typescript
// lib/my-stack.ts
import * as cdk from "aws-cdk-lib";
import * as s3 from "aws-cdk-lib/aws-s3";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import { Construct } from "constructs";

export class MyStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // S3 Bucket
    const bucket = new s3.Bucket(this, "MyBucket", {
      versioned: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      encryption: s3.BucketEncryption.S3_MANAGED,
      lifecycleRules: [
        {
          transitions: [
            {
              storageClass: s3.StorageClass.INTELLIGENT_TIERING,
              transitionAfter: cdk.Duration.days(30),
            },
          ],
        },
      ],
    });

    // DynamoDB Table
    const table = new dynamodb.Table(this, "UsersTable", {
      partitionKey: { name: "id", type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      pointInTimeRecovery: true,
      encryption: dynamodb.TableEncryption.AWS_MANAGED,
    });

    // Lambda Function
    const fn = new lambda.Function(this, "MyFunction", {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: "index.handler",
      code: lambda.Code.fromAsset("lambda"),
      environment: {
        TABLE_NAME: table.tableName,
        BUCKET_NAME: bucket.bucketName,
      },
      timeout: cdk.Duration.seconds(30),
      memorySize: 512,
    });

    // Grant permissions
    table.grantReadWriteData(fn);
    bucket.grantReadWrite(fn);

    // API Gateway
    const api = new apigateway.RestApi(this, "MyApi", {
      restApiName: "My Service",
      description: "API Gateway for Lambda",
      deployOptions: {
        stageName: "prod",
        throttlingBurstLimit: 100,
        throttlingRateLimit: 50,
      },
    });

    const integration = new apigateway.LambdaIntegration(fn);
    api.root.addMethod("GET", integration);

    const users = api.root.addResource("users");
    users.addMethod("GET", integration);
    users.addMethod("POST", integration);

    // Outputs
    new cdk.CfnOutput(this, "BucketName", {
      value: bucket.bucketName,
      description: "S3 Bucket Name",
    });

    new cdk.CfnOutput(this, "ApiUrl", {
      value: api.url,
      description: "API Gateway URL",
    });
  }
}
```

## VPC Stack with CDK

CDK's `ec2.Vpc` L2 construct creates an entire multi-AZ VPC (public/private subnets, route tables, NAT gateway) with sensible defaults from just a few lines — this would be 100+ lines of raw CloudFormation.

```typescript
import * as ec2 from "aws-cdk-lib/aws-ec2";

export class VpcStack extends cdk.Stack {
  public readonly vpc: ec2.Vpc;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create VPC with public and private subnets
    this.vpc = new ec2.Vpc(this, "MyVPC", {
      maxAzs: 2,
      natGateways: 1,
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: "Public",
          subnetType: ec2.SubnetType.PUBLIC,
        },
        {
          cidrMask: 24,
          name: "Private",
          subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
        },
      ],
    });

    // Security Group
    const sg = new ec2.SecurityGroup(this, "WebSG", {
      vpc: this.vpc,
      description: "Security group for web servers",
      allowAllOutbound: true,
    });

    sg.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(80),
      "Allow HTTP traffic"
    );

    sg.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(443),
      "Allow HTTPS traffic"
    );
  }
}
```

## ECS Fargate with CDK

`ApplicationLoadBalancedFargateService` is an L3 "pattern" construct — it stands up an entire ALB + Fargate service + target group + auto scaling in one call, instead of wiring each piece manually.

```typescript
import * as ecs from "aws-cdk-lib/aws-ecs";
import * as ecsPatterns from "aws-cdk-lib/aws-ecs-patterns";

export class EcsStack extends cdk.Stack {
  constructor(
    scope: Construct,
    id: string,
    vpc: ec2.Vpc,
    props?: cdk.StackProps
  ) {
    super(scope, id, props);

    // ECS Cluster
    const cluster = new ecs.Cluster(this, "MyCluster", {
      vpc,
      containerInsights: true,
    });

    // Fargate Service with ALB
    const fargateService =
      new ecsPatterns.ApplicationLoadBalancedFargateService(this, "MyService", {
        cluster,
        cpu: 256,
        desiredCount: 2,
        taskImageOptions: {
          image: ecs.ContainerImage.fromRegistry("amazon/amazon-ecs-sample"),
          containerPort: 80,
          environment: {
            NODE_ENV: "production",
          },
        },
        memoryLimitMiB: 512,
        publicLoadBalancer: true,
      });

    // Auto Scaling
    const scaling = fargateService.service.autoScaleTaskCount({
      minCapacity: 2,
      maxCapacity: 10,
    });

    scaling.scaleOnCpuUtilization("CpuScaling", {
      targetUtilizationPercent: 70,
      scaleInCooldown: cdk.Duration.seconds(60),
      scaleOutCooldown: cdk.Duration.seconds(60),
    });

    // Output
    new cdk.CfnOutput(this, "LoadBalancerDNS", {
      value: fargateService.loadBalancer.loadBalancerDnsName,
    });
  }
}
```

## CDK Deploy Commands

`synth` shows you the generated CloudFormation without deploying; `diff` shows what would change; `deploy` actually applies it; `bootstrap` is a one-time setup CDK needs per account/region before its first deploy.

```bash
# Synthesize CloudFormation template
cdk synth

# Deploy stack
cdk deploy

# Deploy multiple stacks
cdk deploy VpcStack EcsStack

# Deploy with parameters
cdk deploy --parameters EnvironmentName=production

# Destroy stack
cdk destroy

# List stacks
cdk list

# Diff changes
cdk diff

# Bootstrap CDK (first time only)
cdk bootstrap aws://ACCOUNT-ID/REGION
```

## CDK Pipelines

A CI/CD pipeline defined *as CDK code itself* — it can deploy to multiple environments/accounts (dev, then prod with a manual approval gate) directly from a `cdk synth`.

```typescript
import * as pipelines from "aws-cdk-lib/pipelines";
import * as codepipeline from "aws-cdk-lib/aws-codepipeline";

export class PipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const pipeline = new pipelines.CodePipeline(this, "Pipeline", {
      pipelineName: "MyPipeline",
      synth: new pipelines.ShellStep("Synth", {
        input: pipelines.CodePipelineSource.gitHub("owner/repo", "main"),
        commands: ["npm ci", "npm run build", "npx cdk synth"],
      }),
    });

    // Add stages
    const devStage = new MyApplicationStage(this, "Dev", {
      env: { account: "111111111111", region: "us-east-1" },
    });
    pipeline.addStage(devStage);

    const prodStage = new MyApplicationStage(this, "Prod", {
      env: { account: "222222222222", region: "us-east-1" },
    });
    pipeline.addStage(prodStage, {
      pre: [new pipelines.ManualApprovalStep("PromoteToProd")],
    });
  }
}
```

---

## Quick interview answers

**Q: CloudFormation vs CDK — what's actually different under the hood?**
Nothing at the deployment layer — CDK compiles (`synth`) down to a regular CloudFormation template, then CloudFormation deploys it exactly like a hand-written template would. CDK just gives you a real programming language (loops, conditionals, reusable constructs) to *generate* that template.

**Q: What's a Change Set and why does it matter?**
A preview of exactly what an update would create/modify/delete, shown before you actually apply it — prevents accidentally destroying a resource because of an unintended template change.

**Q: What is CDK "drift"?**
Not a CDK-specific term — it's a CloudFormation concept: drift means someone changed a resource manually (outside CloudFormation/CDK), so the real infrastructure no longer matches what the template says. Drift detection finds these mismatches.

**Q: L1 vs L2 vs L3 CDK constructs?**
L1 = direct 1-to-1 mapping to a raw CloudFormation resource (`CfnBucket`). L2 = AWS-curated wrapper with sane defaults and helper methods (`s3.Bucket`). L3/Patterns = a whole pre-built architecture combining multiple resources (`ApplicationLoadBalancedFargateService`).

**Q: Why use Nested Stacks?**
To break a huge template into smaller, reusable, independently manageable pieces (e.g. a shared "networking" stack referenced by multiple app stacks) instead of one giant unmaintainable file.
