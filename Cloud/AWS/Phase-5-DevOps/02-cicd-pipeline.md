# CI/CD Pipeline

> **In plain English:** CI/CD automates "code gets pushed → tested → built → deployed" so nobody manually copies files to a server. On AWS, CodePipeline is the conductor, CodeBuild does the building/testing, and CodeDeploy (or ECS/Lambda deploy actions) actually ships the new version.

## Real-world analogy

Think of a car factory assembly line:

- **CodePipeline** = the conveyor belt moving the car through each station in order (Source → Build → Deploy).
- **CodeBuild** = the assembly station that actually puts pieces together and runs quality checks (compiles code, runs tests, builds a Docker image).
- **CodeDeploy** = the delivery team that installs the finished car at the customer's location (deploys the built artifact to EC2/ECS/Lambda), and can do it carefully in stages.
- **Blue-Green Deployment** = building the new car in a separate garage while the old one keeps running, then swapping the customer over to the new one instantly once it's verified — old car (blue) stays available as an instant fallback.
- **Canary Deployment** = letting only 10% of customers test-drive the new car model first, and only rolling it out to everyone if nothing goes wrong.
- **Rollback** = returning to the previous car model immediately if the new one turns out to be broken.

## Core concepts (memorize these first)

| Term | What it means |
|---|---|
| **CI (Continuous Integration)** | Automatically build + test every code change, so bugs are caught immediately instead of at release time. |
| **CD (Continuous Delivery/Deployment)** | Automatically ship the tested build to an environment — Delivery = a human clicks "go," Deployment = fully automatic with no human step. |
| **CodePipeline** | Orchestrates the whole flow: Source → Build → Test → Deploy, in stages. |
| **CodeBuild** | Runs your build/test commands in a temporary container, defined by a `buildspec.yml`. |
| **CodeDeploy** | Handles the actual deployment to EC2, ECS, or Lambda, including rolling/blue-green strategies. |
| **buildspec.yml** | CodeBuild's instructions: what to do in `pre_build`, `build`, and `post_build` phases. |
| **appspec.yml** | CodeDeploy's instructions: what to deploy and which lifecycle hooks (scripts) to run at each stage. |
| **Artifact** | The output of one pipeline stage, passed as input to the next (e.g. Build stage outputs a Docker image reference, Deploy stage consumes it). |
| **Blue-Green Deployment** | Old version stays fully live while new version deploys separately; traffic switches over only once the new version is verified healthy. Instant rollback = just switch back. |
| **Canary Deployment** | Gradually shift a small % of traffic to the new version first, increasing over time, watching for errors before going 100%. |
| **Rolling Deployment** | Replace instances/tasks a few at a time, rather than all at once — some capacity always available, but old and new versions briefly coexist. |

**Interview-favorite distinction:** Blue-Green vs Canary vs Rolling — all three avoid downtime, but differ in *how fast* and *how much* traffic shifts. Blue-Green = instant full cutover (with instant rollback). Canary = gradual % ramp-up (catches issues early with minimal blast radius). Rolling = replace a few instances at a time (simplest, but old/new versions coexist briefly and rollback is slower).

## Memory hooks

- **"Pipeline = the conveyor belt. Build = the workstation. Deploy = the delivery truck."**
- **buildspec = how to build it. appspec = how to deploy it.** Easy to mix up the two YAML files — remember "build" and "app(deploy)" in the names.
- Canary = "small test group first." Blue-Green = "flip the switch, keep the old one on standby." Rolling = "replace a few at a time."

---

## CodePipeline

The orchestrator — defines the ordered stages (Source, Build, Deploy) and which artifact flows between them.

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

`buildspec.yml` has three phases you should remember: `pre_build` (login/setup), `build` (compile/test/build image), `post_build` (push image, produce artifact). Secrets can be pulled directly from Secrets Manager into env vars.

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

`appspec.yml` tells CodeDeploy what to deploy and which lifecycle hooks to fire — the ECS version wires in a new task definition; the EC2 version copies files and runs shell scripts at each stage.

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

If your source lives in GitHub rather than CodeCommit, GitHub Actions can do the whole build+deploy pipeline itself, authenticating to AWS via access keys (or better, OIDC federation) stored as repo secrets.

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

Same idea but simpler — zip the code, upload it, publish a numbered version, then move a named alias (e.g. `production`) to point at the new version. Aliases are what makes instant rollback possible (just repoint the alias to the old version number).

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

The new version deploys fully alongside the old one; traffic only cuts over after validation hooks pass — meaning rollback is just "route traffic back to the old, still-running version."

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

Send a small percentage of traffic (10% here) to the new version first, and only shift everyone over once it's proven stable — limits the "blast radius" if something's wrong.

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

Deploy the exact same template to multiple regions in parallel — common for disaster recovery or reducing latency for a global user base.

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

Every deploy target has a "go back to the previous known-good version" command — good to know these off the top of your head for incident response.

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

---

## Quick interview answers

**Q: Continuous Delivery vs Continuous Deployment — what's the actual difference?**
Delivery: every change is automatically built/tested and made ready to deploy, but a human clicks "go" for production. Deployment: no human step at all — passing all checks means it ships automatically.

**Q: Blue-Green vs Canary vs Rolling deployment?**
Blue-Green: full new environment stood up alongside the old, instant cutover, instant rollback. Canary: small % of traffic shifted first, gradually increased — limits blast radius of a bad release. Rolling: replace instances/tasks a few at a time — simplest, but old and new versions briefly coexist and rollback takes longer.

**Q: buildspec.yml vs appspec.yml?**
buildspec.yml = CodeBuild's instructions (how to build/test/package). appspec.yml = CodeDeploy's instructions (how/where to deploy the built artifact, plus lifecycle hook scripts).

**Q: How do you achieve safe, instant Lambda rollback?**
Publish immutable numbered versions on every deploy, and point an alias (like `production`) at the desired version — rollback is just repointing the alias to the previous version number.

**Q: Why validate a deployment with lifecycle hooks instead of just deploying and hoping?**
Hooks (BeforeInstall, AfterInstall, AfterAllowTestTraffic, etc) let you run automated health checks at each stage of the deployment and automatically halt/rollback if something's wrong, before real users are affected.
