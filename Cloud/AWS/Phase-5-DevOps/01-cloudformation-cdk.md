# CloudFormation & AWS CDK

## CloudFormation Template

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
