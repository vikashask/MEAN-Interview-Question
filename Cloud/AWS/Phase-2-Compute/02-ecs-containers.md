# ECS, Fargate & Containers

> **In plain English:** ECS runs your Docker containers on AWS. Fargate is a mode of ECS where you don't even manage the underlying servers — you just say "run this container" and AWS finds the hardware. ECR is where your container images live (like a private Docker Hub).

## Real-world analogy

- **Docker container** = a sealed shipping container with your app and everything it needs pre-packed inside — runs the same anywhere.
- **ECS Cluster** = the shipping yard where containers get placed.
- **Task Definition** = the packing list/blueprint for one container (or group of containers) — image, CPU, memory, ports, env vars.
- **Task** = one running instance of that packing list — an actual container running right now.
- **Service** = a foreman ensuring "N copies of this task are always running," restarting failed ones and load balancing traffic to them.
- **Fargate vs EC2 launch type** = Fargate is "the shipping yard has invisible cranes you never see or maintain"; EC2 launch type is "you own and maintain the cranes (servers) yourself, ECS just tells them what to lift."
- **ECR** = the private warehouse that stores your container images before they're shipped out.

## Core concepts (memorize these first)

| Term | What it means |
|---|---|
| **Task Definition** | JSON blueprint: which image, how much CPU/memory, ports, env vars, secrets, logging config. |
| **Task** | One running instance launched from a task definition. |
| **Service** | Keeps a desired number of tasks running, integrates with a load balancer, handles rolling deployments. |
| **Cluster** | A logical grouping of tasks/services (and, for EC2 launch type, the underlying EC2 instances). |
| **Fargate** | Serverless launch type — no EC2 instances to manage, pay per task's CPU/memory. |
| **EC2 launch type** | You provision and manage the EC2 instances that host the containers yourself — cheaper at scale, more control, more ops work. |
| **ECR** | AWS's private Docker image registry. |
| **Task Role vs Execution Role** | Execution Role = permissions ECS itself needs (pull image, write logs). Task Role = permissions *your application code* needs (e.g. read S3). Easy to mix these up in interviews! |
| **Service Discovery** | Lets tasks find each other by DNS name instead of hardcoded IPs (containers get new IPs each time they restart). |

**ECS vs EKS (common interview question):** ECS is AWS's own simpler container orchestrator. EKS is managed Kubernetes — more powerful/portable/complex, useful if you need Kubernetes specifically (e.g. multi-cloud, existing k8s expertise).

## Memory hooks

- **"Fargate = no servers to babysit. EC2 launch type = you babysit the servers."**
- **Execution Role = ECS's own permissions. Task Role = your app's permissions.** ("Execution gets you started, Task is what you actually do.")
- Task Definition is a *template*; a Task is a *running instance* of that template — same relationship as a class and an object.

---

## ECS Task Definition

The blueprint: image location, resource sizing, ports, env vars/secrets, logging, and health check — all in one JSON file.

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

A service keeps `desired-count` tasks running at all times, wires them to a load balancer, and handles rolling updates when you push a new task definition version.

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

Your private Docker registry. The pattern is always: build locally → tag with the ECR URL → push.

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

Standard practices baked in: small base image (`alpine`), only production deps, non-root user for security, and a health check the ECS task definition can also point to.

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

The ALB routes traffic to a target group; ECS registers/deregisters tasks in that target group automatically as they start/stop/fail health checks.

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

Same target-tracking idea as EC2 Auto Scaling, but scaling the *number of tasks* instead of instances — based on average CPU here.

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

Since container IPs change every restart, service discovery gives them a stable DNS name (e.g. `my-app.local`) so other services can find them reliably.

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

Blue-green means: keep the old version ("blue") fully running while the new version ("green") gets deployed and tested, then flip traffic over — zero downtime, instant rollback if something's wrong.

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

---

## Quick interview answers

**Q: Fargate vs EC2 launch type for ECS?**
Fargate = no server management, pay per task's CPU/memory, simpler but pricier at scale. EC2 launch type = you manage the underlying instances, cheaper at high/steady scale, more control (e.g. GPU instances, custom AMIs).

**Q: ECS vs EKS?**
ECS = AWS-proprietary, simpler to learn, tightly integrated with other AWS services. EKS = managed Kubernetes, steeper learning curve, portable across clouds, needed if you require k8s-specific tooling/ecosystem.

**Q: Execution Role vs Task Role?**
Execution Role: what ECS itself needs to start the task (pull image from ECR, write to CloudWatch, read secrets). Task Role: what your application code needs while running (e.g. call S3, DynamoDB).

**Q: How does an ECS Service handle a failed task?**
It detects the task is unhealthy (via health checks) or stopped, and automatically launches a replacement to maintain the desired count.

**Q: What problem does Service Discovery solve?**
Containers get new IPs every time they restart; service discovery gives them a stable DNS name so dependent services don't break on restart.
