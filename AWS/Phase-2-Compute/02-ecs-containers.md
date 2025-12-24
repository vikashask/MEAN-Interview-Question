# ECS, Fargate & Containers

## ECS Task Definition

```json
{
  "family": "my-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::123456789012:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest",
      "portMappings": [
        {
          "containerPort": 3000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        { "name": "NODE_ENV", "value": "production" },
        { "name": "PORT", "value": "3000" }
      ],
      "secrets": [
        {
          "name": "DB_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:db-password"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/my-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": [
          "CMD-SHELL",
          "curl -f http://localhost:3000/health || exit 1"
        ],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      }
    }
  ]
}
```

## ECS Service

```bash
# Create cluster
aws ecs create-cluster --cluster-name production

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster production \
  --service-name my-app-service \
  --task-definition my-app:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-12345,subnet-67890],securityGroups=[sg-12345],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=app,containerPort=3000" \
  --deployment-configuration "maximumPercent=200,minimumHealthyPercent=100"

# Update service
aws ecs update-service \
  --cluster production \
  --service my-app-service \
  --task-definition my-app:2 \
  --desired-count 4

# Scale service
aws ecs update-service \
  --cluster production \
  --service my-app-service \
  --desired-count 10
```

## ECR (Container Registry)

```bash
# Create repository
aws ecr create-repository --repository-name my-app

# Get login token
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t my-app .
docker tag my-app:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest

# List images
aws ecr list-images --repository-name my-app

# Delete image
aws ecr batch-delete-image \
  --repository-name my-app \
  --image-ids imageTag=old-tag
```

## Dockerfile for ECS

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application
COPY . .

# Non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD node healthcheck.js

CMD ["node", "index.js"]
```

## ECS with Application Load Balancer

```bash
# Create target group
aws elbv2 create-target-group \
  --name my-app-tg \
  --protocol HTTP \
  --port 3000 \
  --vpc-id vpc-12345 \
  --target-type ip \
  --health-check-path /health \
  --health-check-interval-seconds 30

# Create load balancer
aws elbv2 create-load-balancer \
  --name my-app-alb \
  --subnets subnet-12345 subnet-67890 \
  --security-groups sg-12345

# Create listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...
```

## ECS Auto Scaling

```bash
# Register scalable target
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/production/my-app-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 10

# Create scaling policy
aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/production/my-app-service \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-name cpu-scaling-policy \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

```json
// scaling-policy.json
{
  "TargetValue": 70.0,
  "PredefinedMetricSpecification": {
    "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
  },
  "ScaleOutCooldown": 60,
  "ScaleInCooldown": 60
}
```

## ECS Service Discovery

```bash
# Create service discovery namespace
aws servicediscovery create-private-dns-namespace \
  --name local \
  --vpc vpc-12345

# Create service discovery service
aws servicediscovery create-service \
  --name my-app \
  --dns-config "NamespaceId=ns-12345,DnsRecords=[{Type=A,TTL=60}]" \
  --health-check-custom-config FailureThreshold=1

# Update ECS service with service registry
aws ecs create-service \
  --cluster production \
  --service-name my-app-service \
  --task-definition my-app:1 \
  --service-registries "registryArn=arn:aws:servicediscovery:..."
```

## ECS with SDK

```javascript
import {
  ECSClient,
  RunTaskCommand,
  UpdateServiceCommand,
  DescribeTasksCommand,
} from "@aws-sdk/client-ecs";

const ecs = new ECSClient({ region: "us-east-1" });

// Run task
const runTask = async () => {
  const command = new RunTaskCommand({
    cluster: "production",
    taskDefinition: "my-app:1",
    launchType: "FARGATE",
    networkConfiguration: {
      awsvpcConfiguration: {
        subnets: ["subnet-12345", "subnet-67890"],
        securityGroups: ["sg-12345"],
        assignPublicIp: "ENABLED",
      },
    },
    count: 1,
  });

  const response = await ecs.send(command);
  return response.tasks;
};

// Update service
const updateService = async (desiredCount) => {
  const command = new UpdateServiceCommand({
    cluster: "production",
    service: "my-app-service",
    desiredCount,
  });

  await ecs.send(command);
};

// Get task details
const getTaskDetails = async (taskArn) => {
  const command = new DescribeTasksCommand({
    cluster: "production",
    tasks: [taskArn],
  });

  const response = await ecs.send(command);
  return response.tasks[0];
};
```

## Blue-Green Deployment

```javascript
// CodeDeploy appspec.yml for ECS
{
  "version": 0.0,
  "Resources": [
    {
      "TargetService": {
        "Type": "AWS::ECS::Service",
        "Properties": {
          "TaskDefinition": "arn:aws:ecs:us-east-1:123456789012:task-definition/my-app:2",
          "LoadBalancerInfo": {
            "ContainerName": "app",
            "ContainerPort": 3000
          }
        }
      }
    }
  ],
  "Hooks": [
    {
      "BeforeInstall": "LambdaFunctionToValidateBeforeInstall"
    },
    {
      "AfterInstall": "LambdaFunctionToValidateAfterInstall"
    },
    {
      "AfterAllowTestTraffic": "LambdaFunctionToValidateAfterTestTrafficStarts"
    },
    {
      "BeforeAllowTraffic": "LambdaFunctionToValidateBeforeAllowingProductionTraffic"
    },
    {
      "AfterAllowTraffic": "LambdaFunctionToValidateAfterAllowingProductionTraffic"
    }
  ]
}
```
