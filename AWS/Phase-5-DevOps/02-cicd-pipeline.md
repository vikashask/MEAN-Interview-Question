# CI/CD Pipeline

## CodePipeline

```bash
# Create pipeline
aws codepipeline create-pipeline --cli-input-json file://pipeline.json

# Start pipeline execution
aws codepipeline start-pipeline-execution --name MyPipeline

# Get pipeline state
aws codepipeline get-pipeline-state --name MyPipeline

# List pipelines
aws codepipeline list-pipelines
```

```json
// pipeline.json
{
  "pipeline": {
    "name": "MyAppPipeline",
    "roleArn": "arn:aws:iam::123456789012:role/CodePipelineRole",
    "artifactStore": {
      "type": "S3",
      "location": "my-pipeline-artifacts"
    },
    "stages": [
      {
        "name": "Source",
        "actions": [
          {
            "name": "SourceAction",
            "actionTypeId": {
              "category": "Source",
              "owner": "AWS",
              "provider": "CodeCommit",
              "version": "1"
            },
            "configuration": {
              "RepositoryName": "my-app",
              "BranchName": "main"
            },
            "outputArtifacts": [
              {
                "name": "SourceOutput"
              }
            ]
          }
        ]
      },
      {
        "name": "Build",
        "actions": [
          {
            "name": "BuildAction",
            "actionTypeId": {
              "category": "Build",
              "owner": "AWS",
              "provider": "CodeBuild",
              "version": "1"
            },
            "configuration": {
              "ProjectName": "MyBuildProject"
            },
            "inputArtifacts": [
              {
                "name": "SourceOutput"
              }
            ],
            "outputArtifacts": [
              {
                "name": "BuildOutput"
              }
            ]
          }
        ]
      },
      {
        "name": "Deploy",
        "actions": [
          {
            "name": "DeployAction",
            "actionTypeId": {
              "category": "Deploy",
              "owner": "AWS",
              "provider": "ECS",
              "version": "1"
            },
            "configuration": {
              "ClusterName": "my-cluster",
              "ServiceName": "my-service",
              "FileName": "imagedefinitions.json"
            },
            "inputArtifacts": [
              {
                "name": "BuildOutput"
              }
            ]
          }
        ]
      }
    ]
  }
}
```

## CodeBuild

```yaml
# buildspec.yml
version: 0.2

env:
  variables:
    NODE_ENV: production
  secrets-manager:
    DB_PASSWORD: prod/db/password

phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
      - REPOSITORY_URI=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME
      - IMAGE_TAG=${CODEBUILD_RESOLVED_SOURCE_VERSION:0:7}

  build:
    commands:
      - echo Build started on `date`
      - echo Installing dependencies...
      - npm ci
      - echo Running tests...
      - npm test
      - echo Building Docker image...
      - docker build -t $REPOSITORY_URI:$IMAGE_TAG .
      - docker tag $REPOSITORY_URI:$IMAGE_TAG $REPOSITORY_URI:latest

  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing Docker image...
      - docker push $REPOSITORY_URI:$IMAGE_TAG
      - docker push $REPOSITORY_URI:latest
      - echo Writing image definitions file...
      - printf '[{"name":"app","imageUri":"%s"}]' $REPOSITORY_URI:$IMAGE_TAG > imagedefinitions.json

artifacts:
  files:
    - imagedefinitions.json
    - "**/*"
  discard-paths: no

cache:
  paths:
    - node_modules/**/*
```

```bash
# Create CodeBuild project
aws codebuild create-project \
  --name MyBuildProject \
  --source type=CODECOMMIT,location=https://git-codecommit.us-east-1.amazonaws.com/v1/repos/my-app \
  --artifacts type=S3,location=my-build-artifacts \
  --environment type=LINUX_CONTAINER,image=aws/codebuild/standard:7.0,computeType=BUILD_GENERAL1_SMALL \
  --service-role arn:aws:iam::123456789012:role/CodeBuildRole

# Start build
aws codebuild start-build --project-name MyBuildProject

# Get build details
aws codebuild batch-get-builds --ids my-build-id
```

## CodeDeploy

```yaml
# appspec.yml (for ECS)
version: 0.0
Resources:
  - TargetService:
      Type: AWS::ECS::Service
      Properties:
        TaskDefinition: <TASK_DEFINITION>
        LoadBalancerInfo:
          ContainerName: "app"
          ContainerPort: 3000
        PlatformVersion: "LATEST"

Hooks:
  - BeforeInstall: "LambdaFunctionToValidateBeforeInstall"
  - AfterInstall: "LambdaFunctionToValidateAfterInstall"
  - AfterAllowTestTraffic: "LambdaFunctionToValidateTestTraffic"
  - BeforeAllowTraffic: "LambdaFunctionToValidateBeforeProduction"
  - AfterAllowTraffic: "LambdaFunctionToValidateAfterProduction"
```

```yaml
# appspec.yml (for EC2/On-premises)
version: 0.0
os: linux
files:
  - source: /
    destination: /var/www/html

permissions:
  - object: /var/www/html
    owner: www-data
    group: www-data
    mode: 755

hooks:
  BeforeInstall:
    - location: scripts/install_dependencies.sh
      timeout: 300
      runas: root
  AfterInstall:
    - location: scripts/start_server.sh
      timeout: 300
      runas: root
  ApplicationStart:
    - location: scripts/start_application.sh
      timeout: 300
      runas: root
  ValidateService:
    - location: scripts/validate_service.sh
      timeout: 300
```

## GitHub Actions with AWS

```yaml
# .github/workflows/deploy.yml
name: Deploy to AWS

on:
  push:
    branches: [main]

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: my-app
  ECS_SERVICE: my-service
  ECS_CLUSTER: my-cluster
  ECS_TASK_DEFINITION: task-definition.json
  CONTAINER_NAME: app

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1

      - name: Build, tag, and push image to Amazon ECR
        id: build-image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

      - name: Fill in the new image ID in the Amazon ECS task definition
        id: task-def
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: ${{ env.ECS_TASK_DEFINITION }}
          container-name: ${{ env.CONTAINER_NAME }}
          image: ${{ steps.build-image.outputs.image }}

      - name: Deploy Amazon ECS task definition
        uses: aws-actions/amazon-ecs-deploy-task-definition@v1
        with:
          task-definition: ${{ steps.task-def.outputs.task-definition }}
          service: ${{ env.ECS_SERVICE }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true

      - name: Run database migrations
        run: |
          aws ecs run-task \
            --cluster ${{ env.ECS_CLUSTER }} \
            --task-definition migration-task \
            --launch-type FARGATE \
            --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
```

## Lambda Deployment

```yaml
# .github/workflows/deploy-lambda.yml
name: Deploy Lambda

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18"
          cache: "npm"

      - name: Install dependencies
        run: npm ci --production

      - name: Create deployment package
        run: zip -r function.zip . -x "*.git*" "node_modules/aws-sdk/*"

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to Lambda
        run: |
          aws lambda update-function-code \
            --function-name my-function \
            --zip-file fileb://function.zip

          aws lambda wait function-updated \
            --function-name my-function

          aws lambda publish-version \
            --function-name my-function

      - name: Update alias
        run: |
          VERSION=$(aws lambda list-versions-by-function \
            --function-name my-function \
            --query 'Versions[-1].Version' \
            --output text)

          aws lambda update-alias \
            --function-name my-function \
            --name production \
            --function-version $VERSION
```

## Blue-Green Deployment

```yaml
# Blue-Green with CodeDeploy
Resources:
  BlueGreenDeploymentConfig:
    Type: AWS::CodeDeploy::DeploymentConfig
    Properties:
      DeploymentConfigName: CustomBlueGreen
      TrafficRoutingConfig:
        Type: TimeBasedLinear
        TimeBasedLinear:
          LinearPercentage: 10
          LinearInterval: 1
```

```javascript
// Lambda hook for validation
export const handler = async (event) => {
  const deploymentId = event.DeploymentId;
  const lifecycleEventHookExecutionId = event.LifecycleEventHookExecutionId;

  try {
    // Validate deployment
    const isHealthy = await checkApplicationHealth();

    if (isHealthy) {
      // Continue deployment
      await codedeploy.putLifecycleEventHookExecutionStatus({
        deploymentId,
        lifecycleEventHookExecutionId,
        status: "Succeeded",
      });
    } else {
      // Rollback deployment
      await codedeploy.putLifecycleEventHookExecutionStatus({
        deploymentId,
        lifecycleEventHookExecutionId,
        status: "Failed",
      });
    }
  } catch (error) {
    console.error("Validation failed:", error);
    throw error;
  }
};
```

## Canary Deployment

```yaml
# API Gateway Canary
Resources:
  ApiDeployment:
    Type: AWS::ApiGateway::Deployment
    Properties:
      RestApiId: !Ref MyApi
      StageDescription:
        CanarySettings:
          PercentTraffic: 10
          UseStageCache: false
```

## Multi-Region Deployment

```yaml
# .github/workflows/multi-region-deploy.yml
name: Multi-Region Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        region: [us-east-1, eu-west-1, ap-southeast-1]

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to ${{ matrix.region }}
        run: |
          aws cloudformation deploy \
            --template-file template.yaml \
            --stack-name my-app \
            --region ${{ matrix.region }} \
            --capabilities CAPABILITY_IAM
```

## Rollback Strategy

```bash
# Rollback ECS service
aws ecs update-service \
  --cluster my-cluster \
  --service my-service \
  --task-definition my-app:10  # Previous version

# Rollback Lambda alias
aws lambda update-alias \
  --function-name my-function \
  --name production \
  --function-version 5  # Previous version

# Rollback CloudFormation
aws cloudformation cancel-update-stack --stack-name my-app
```
