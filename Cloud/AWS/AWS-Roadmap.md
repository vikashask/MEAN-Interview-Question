# AWS Roadmap - Advanced Track

> **For experienced developers (3+ years AWS experience)** - Focus on production architectures and best practices

## 🔹 Phase 1: AWS Fundamentals & Core Services (1–2 weeks)

Master the AWS foundation and global infrastructure.

### AWS Global Infrastructure

- Regions, Availability Zones, and Edge Locations
- High availability and fault tolerance
- Disaster recovery strategies
- Global service vs regional services
- AWS Well-Architected Framework

### IAM (Identity & Access Management)

- Users, Groups, Roles, and Policies
- Policy types (managed, inline, resource-based)
- Permission boundaries and SCPs
- Cross-account access and assume role
- Identity Federation (SAML, OIDC)
- AWS Organizations and multi-account strategy
- IAM best practices and least privilege

### AWS CLI & SDKs

- AWS CLI v2 configuration and profiles
- AWS SDK for JavaScript/Node.js
- Boto3 for Python
- Credential management and environment variables
- Pagination and error handling
- Exponential backoff and retries

### CloudWatch

- Metrics and custom metrics
- Alarms and notifications
- CloudWatch Logs and Log Groups
- Log Insights queries
- CloudWatch Dashboards
- Unified CloudWatch Agent

---

## 🔹 Phase 2: Compute Services (2–3 weeks)

Deep dive into compute options and containerization.

### EC2 (Elastic Compute Cloud)

- Instance types and families (General, Compute, Memory, Storage)
- AMIs (Amazon Machine Images)
- User Data and metadata service
- Instance storage vs EBS
- Placement groups
- Auto Scaling Groups and launch templates
- Spot Instances, Reserved Instances, Savings Plans
- EC2 best practices and cost optimization

### Elastic Load Balancing

- Application Load Balancer (ALB) - Layer 7
- Network Load Balancer (NLB) - Layer 4
- Gateway Load Balancer
- Target groups and health checks
- Sticky sessions and connection draining
- Cross-zone load balancing
- SSL/TLS termination

### Lambda (Serverless)

- Function configuration and runtimes
- Event sources and triggers
- Lambda layers and dependencies
- Environment variables and configuration
- Concurrency and throttling
- Cold starts and optimization
- Lambda@Edge and CloudFront integration
- Step Functions for orchestration

### ECS & Fargate

- ECS clusters and task definitions
- Fargate serverless containers
- ECR (Elastic Container Registry)
- Service auto-scaling
- Load balancer integration
- Task IAM roles
- ECS vs EKS comparison

### EKS (Elastic Kubernetes Service)

- Kubernetes fundamentals
- EKS cluster setup and node groups
- Fargate for EKS
- Helm charts
- kubectl and eksctl
- IRSA (IAM Roles for Service Accounts)
- EKS add-ons and CNI

---

## 🔹 Phase 3: Networking & Security (2–3 weeks)

Build secure and scalable network architectures.

### VPC (Virtual Private Cloud)

- CIDR blocks and subnets
- Public vs private subnets
- Route tables and internet gateway
- NAT Gateway vs NAT Instance
- VPC Peering and Transit Gateway
- VPC Endpoints (Gateway, Interface)
- Network ACLs vs Security Groups
- VPC Flow Logs

### Route 53

- DNS record types (A, AAAA, CNAME, MX, TXT)
- Routing policies (Simple, Weighted, Latency, Failover, Geolocation)
- Health checks and failover
- Private hosted zones
- Domain registration and transfer
- Traffic flow and geoproximity routing

### CloudFront

- CDN distribution setup
- Origin types (S3, ALB, custom)
- Cache behaviors and TTL
- Invalidations and versioning
- Signed URLs and cookies
- Lambda@Edge and CloudFront Functions
- OAI (Origin Access Identity)
- Security headers and WAF integration

### Security Services

- AWS WAF (Web Application Firewall)
- AWS Shield (DDoS protection)
- AWS GuardDuty (threat detection)
- AWS Inspector (vulnerability assessment)
- AWS Secrets Manager
- AWS Systems Manager Parameter Store
- AWS Certificate Manager (ACM)
- AWS KMS (Key Management Service)

---

## 🔹 Phase 4: Storage & Databases (2–3 weeks)

Master data persistence and storage solutions.

### S3 (Simple Storage Service)

- Bucket policies and ACLs
- Storage classes (Standard, IA, Glacier, Deep Archive)
- Lifecycle policies
- Versioning and MFA delete
- Cross-region replication (CRR)
- S3 Transfer Acceleration
- S3 Select and Glacier Select
- Static website hosting
- S3 Event Notifications

### EBS (Elastic Block Store)

- Volume types (gp3, io2, st1, sc1)
- Snapshots and AMIs
- Encryption at rest
- RAID configurations
- EBS-optimized instances
- Multi-attach and provisioned IOPS

### EFS (Elastic File System)

- NFS file system for Linux
- Performance modes (General, Max I/O)
- Throughput modes (Bursting, Provisioned)
- Storage classes and lifecycle management
- Mount targets and security groups

### RDS (Relational Database Service)

- Supported engines (MySQL, PostgreSQL, Aurora, Oracle, SQL Server)
- Multi-AZ deployments
- Read replicas and cross-region replication
- Automated backups and point-in-time recovery
- Parameter groups and option groups
- Enhanced monitoring and Performance Insights
- RDS Proxy for connection pooling

### DynamoDB

- NoSQL key-value and document database
- Partition keys and sort keys
- Indexes (GSI, LSI)
- Provisioned vs on-demand capacity
- DynamoDB Streams
- DAX (DynamoDB Accelerator)
- Global tables for multi-region
- Transaction support

### ElastiCache

- Redis vs Memcached
- Cluster modes and sharding
- Replication and Multi-AZ
- Backup and restore
- Redis AUTH and encryption

### Aurora

- MySQL and PostgreSQL compatible
- Aurora Serverless v2
- Global databases
- Aurora Replicas and cross-region
- Backtrack and clone
- Performance optimization

---

## 🔹 Phase 5: DevOps & CI/CD (2–3 weeks)

Implement automation and continuous delivery.

### Infrastructure as Code

- CloudFormation templates (JSON, YAML)
- Stack creation and updates
- Change sets and drift detection
- Nested stacks and StackSets
- Custom resources and macros
- Terraform on AWS
- AWS CDK (Cloud Development Kit)
- Pulumi for infrastructure

### CI/CD Pipelines

- CodeCommit (Git repositories)
- CodeBuild (build and test)
- CodeDeploy (deployment automation)
- CodePipeline (orchestration)
- Blue-green deployments
- Canary deployments
- Integration with GitHub Actions
- Jenkins on AWS

### Elastic Beanstalk

- Application deployment platform
- Supported platforms (Node.js, Python, Docker)
- Environment tiers (Web, Worker)
- Configuration files (.ebextensions)
- Rolling updates and immutable deployments
- Custom platform images

### Systems Manager

- Session Manager (SSH alternative)
- Parameter Store
- Patch Manager
- Run Command
- State Manager
- Automation documents

### Monitoring & Logging

- CloudWatch Logs aggregation
- X-Ray distributed tracing
- CloudTrail for API auditing
- Config for resource compliance
- EventBridge for event-driven architecture

---

## 🔹 Phase 6: Advanced Services & Architecture (3–4 weeks)

Master advanced AWS services and patterns.

### Messaging & Queues

- SQS (Simple Queue Service)
- SNS (Simple Notification Service)
- SQS FIFO queues
- Dead letter queues
- Message visibility timeout
- Long polling vs short polling
- Fan-out pattern with SNS+SQS
- EventBridge for event routing

### API Gateway

- REST APIs and HTTP APIs
- WebSocket APIs
- Request validation and transformation
- API keys and usage plans
- Lambda authorizers
- VPC Link for private APIs
- API caching
- Throttling and rate limiting

### AppSync

- GraphQL APIs
- Resolvers and data sources
- Real-time subscriptions
- Caching and batching
- Authorization modes

### Step Functions

- State machine workflows
- Task states and parallel execution
- Error handling and retries
- Express vs Standard workflows
- Service integrations

### Cognito

- User pools for authentication
- Identity pools for authorization
- Social identity providers
- Custom authentication flows
- MFA and advanced security
- User migration

### Data Analytics

- Kinesis Data Streams
- Kinesis Data Firehose
- Kinesis Data Analytics
- Athena (SQL on S3)
- Glue (ETL service)
- EMR (Hadoop/Spark)
- Redshift (data warehouse)
- QuickSight (BI and dashboards)

### Machine Learning

- SageMaker for ML model training
- Rekognition for image/video analysis
- Comprehend for NLP
- Translate and Transcribe
- Forecast and Personalize

---

## 🔹 Phase 7: Cost Optimization & Governance (1–2 weeks)

Manage costs and implement best practices.

### Cost Management

- Cost Explorer and reports
- Budgets and alerts
- Savings Plans and Reserved Instances
- Spot Instances strategies
- S3 Intelligent-Tiering
- RDS cost optimization
- Lambda cost optimization
- Trusted Advisor recommendations

### Governance & Compliance

- AWS Organizations and OUs
- Service Control Policies (SCPs)
- AWS Control Tower
- AWS Config rules
- Compliance frameworks (HIPAA, PCI-DSS, SOC 2)
- Audit Manager
- Resource tagging strategies

### Disaster Recovery

- Backup and restore
- Pilot light
- Warm standby
- Multi-site active-active
- RTO and RPO planning
- Cross-region disaster recovery

---

## 🎯 AWS Architecture Patterns

### Common Patterns to Master

1. **Three-Tier Web Application**

   - ALB → EC2/ECS → RDS
   - Auto Scaling and Multi-AZ
   - CloudFront and S3 for static assets

2. **Serverless Web Application**

   - CloudFront → API Gateway → Lambda → DynamoDB
   - Cognito for authentication
   - S3 for static hosting

3. **Microservices on ECS/EKS**

   - Application Load Balancer
   - Service discovery
   - Centralized logging and monitoring

4. **Event-Driven Architecture**

   - EventBridge → Lambda
   - SQS/SNS for decoupling
   - Step Functions for orchestration

5. **Data Lake Architecture**
   - S3 data lake
   - Glue for ETL
   - Athena for querying
   - QuickSight for visualization

---

## 📚 AWS Certifications Path

- **AWS Certified Solutions Architect - Associate**
- **AWS Certified Developer - Associate**
- **AWS Certified Solutions Architect - Professional**
- **AWS Certified DevOps Engineer - Professional**
- **Specialty: Security, Networking, Database**

---

## 🚀 Best Practices Checklist

- [ ] Enable MFA for root and IAM users
- [ ] Use IAM roles instead of access keys
- [ ] Enable CloudTrail in all regions
- [ ] Implement least privilege principle
- [ ] Use encryption at rest and in transit
- [ ] Set up billing alerts and budgets
- [ ] Tag all resources consistently
- [ ] Enable VPC Flow Logs
- [ ] Use Auto Scaling for high availability
- [ ] Implement Multi-AZ for databases
- [ ] Set up CloudWatch alarms
- [ ] Use Secrets Manager for credentials
- [ ] Enable S3 versioning for critical data
- [ ] Implement backup strategies
- [ ] Document architecture with diagrams

---

## 📖 Essential Resources

### Official Documentation

- AWS Well-Architected Framework
- AWS Whitepapers and guides
- AWS re:Invent videos
- AWS Architecture Center

### Tools

- AWS CLI and SDKs
- Terraform/CloudFormation
- AWS CDK
- LocalStack (local AWS emulation)
- CloudMapper (visualization)

### Learning Platforms

- AWS Skill Builder
- A Cloud Guru / Pluralsight
- AWS Solutions Library
- AWS Samples on GitHub
