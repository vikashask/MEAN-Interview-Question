# AWS Security Services

> **In plain English:** This file covers the "safe boxes and guards" of AWS — where to store secrets, how to encrypt things, how to detect attacks, and how to prove (audit) what happened. Different from IAM: IAM decides *who can do what*; these services protect *data* and *detect threats*.

## Real-world analogy

- **Secrets Manager** = a bank vault specifically for passwords/API keys, with an auto-rotation feature (the bank changes the vault combination on a schedule automatically).
- **Systems Manager Parameter Store** = a cheaper filing cabinet for config values — some drawers are locked (SecureString/encrypted), some aren't (String).
- **KMS (Key Management Service)** = the master locksmith — makes the encryption keys used everywhere else (S3, EBS, Secrets Manager), and never lets the raw key leave its vault.
- **ACM (Certificate Manager)** = the passport office issuing/renewing HTTPS certificates for free, automatically.
- **WAF (Web Application Firewall)** = a bouncer reading every visitor's ID at the door of your website, blocking known troublemakers (SQL injection attempts, bad IPs, rate-limit abusers).
- **Shield** = riot police specifically for DDoS floods (traffic volume attacks), separate from WAF's "check each visitor" job.
- **GuardDuty** = a security camera system with AI — watches account activity and network traffic for suspicious patterns (like a login from an unusual country) and raises alerts.
- **Inspector** = a home inspector who checks your EC2 instances/containers for known vulnerabilities (like unpatched software).
- **Security Hub** = the security control room — pulls together findings from GuardDuty, Inspector, and others into one dashboard.
- **CloudTrail** = the building's permanent security log — records every single action anyone (or any service) took in your AWS account, who did it, and when.

## Core concepts (memorize these first)

| Service | One-line job |
|---|---|
| **Secrets Manager** | Store + auto-rotate sensitive secrets (DB passwords, API keys). Costs more, but rotation is built-in. |
| **SSM Parameter Store** | Store config values (plain or encrypted). Cheaper than Secrets Manager, no built-in rotation. |
| **KMS** | Create and manage encryption keys; encrypts/decrypts data; backs encryption for almost every other AWS service. |
| **ACM** | Free SSL/TLS certificates for HTTPS, auto-renewed. |
| **WAF** | Blocks malicious *web requests* (SQLi, XSS, rate limiting) at Layer 7, attached to CloudFront/ALB/API Gateway. |
| **Shield** | Protects against DDoS (traffic flood) attacks. Standard = free & automatic. Advanced = paid, more protection + cost protection. |
| **GuardDuty** | Continuous threat detection using ML — watches CloudTrail, VPC Flow Logs, DNS logs for suspicious behavior. |
| **Inspector** | Scans EC2/containers/Lambda for known software vulnerabilities (CVEs). |
| **Security Hub** | Aggregates findings from GuardDuty, Inspector, and compliance checks into one view. |
| **CloudTrail** | Audit log of every API call made in your account — "who did what, when." |

**Interview-favorite distinction:** Secrets Manager vs Parameter Store — both store key/value data, but Secrets Manager costs more and adds automatic rotation (great for DB passwords); Parameter Store is cheaper and simpler (great for config/feature flags, or secrets you rotate manually).

**Another favorite:** WAF vs Shield — WAF inspects individual HTTP requests for malicious *content* (like a bouncer checking IDs); Shield defends against sheer traffic *volume* floods (like riot police against a stampede). They're complementary, not competing.

## Memory hooks

- **"KMS makes the keys. Secrets Manager and Parameter Store store the locked box."**
- **CloudTrail = "what happened." GuardDuty = "was it bad." Security Hub = "show me everything in one screen."**
- WAF = Layer 7 (content of the request). Shield = volume/network layer (DDoS).

---

## AWS Secrets Manager

Best for anything that needs automatic rotation, like database credentials — plug the ARN into your app instead of hardcoding a password anywhere.

```bash
# Create secret
aws secretsmanager create-secret \
  --name prod/db/password \
  --secret-string "MySecretPassword123!"

# Store JSON secret
aws secretsmanager create-secret \
  --name prod/db/credentials \
  --secret-string '{
    "username": "admin",
    "password": "MySecretPassword123!",
    "host": "db.example.com",
    "port": 5432
  }'

# Get secret value
aws secretsmanager get-secret-value --secret-id prod/db/password

# Update secret
aws secretsmanager update-secret \
  --secret-id prod/db/password \
  --secret-string "NewPassword456!"

# Rotate secret
aws secretsmanager rotate-secret \
  --secret-id prod/db/password \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:RotateSecret
```

```javascript
import {
  SecretsManagerClient,
  GetSecretValueCommand,
} from "@aws-sdk/client-secrets-manager";

const secretsManager = new SecretsManagerClient({ region: "us-east-1" });

// Get secret
const getSecret = async (secretId) => {
  const command = new GetSecretValueCommand({ SecretId: secretId });
  const response = await secretsManager.send(command);
  return JSON.parse(response.SecretString);
};

// Usage in application
const dbConfig = await getSecret("prod/db/credentials");
const connection = await connectDB({
  host: dbConfig.host,
  user: dbConfig.username,
  password: dbConfig.password,
  port: dbConfig.port,
});
```

## Systems Manager Parameter Store

Cheaper alternative to Secrets Manager. Use `String` for non-sensitive config, `SecureString` for anything sensitive (encrypted with KMS but no auto-rotation).

```bash
# Create parameter
aws ssm put-parameter \
  --name /myapp/db/host \
  --value "db.example.com" \
  --type String

# Secure string (encrypted)
aws ssm put-parameter \
  --name /myapp/api/key \
  --value "secret-api-key" \
  --type SecureString

# Get parameter
aws ssm get-parameter --name /myapp/db/host

# Get with decryption
aws ssm get-parameter \
  --name /myapp/api/key \
  --with-decryption

# Get multiple parameters
aws ssm get-parameters \
  --names /myapp/db/host /myapp/db/port /myapp/api/key \
  --with-decryption

# Get by path
aws ssm get-parameters-by-path \
  --path /myapp/db \
  --recursive
```

```javascript
import {
  SSMClient,
  GetParameterCommand,
  GetParametersByPathCommand,
} from "@aws-sdk/client-ssm";

const ssm = new SSMClient({ region: "us-east-1" });

// Get single parameter
const getParameter = async (name) => {
  const command = new GetParameterCommand({
    Name: name,
    WithDecryption: true,
  });
  const response = await ssm.send(command);
  return response.Parameter.Value;
};

// Get all parameters by path
const getParametersByPath = async (path) => {
  const command = new GetParametersByPathCommand({
    Path: path,
    Recursive: true,
    WithDecryption: true,
  });
  const response = await ssm.send(command);

  return response.Parameters.reduce((acc, param) => {
    const key = param.Name.split("/").pop();
    acc[key] = param.Value;
    return acc;
  }, {});
};

// Usage
const apiKey = await getParameter("/myapp/api/key");
const dbConfig = await getParametersByPath("/myapp/db");
```

## AWS KMS (Key Management Service)

KMS creates and guards the master encryption keys. The raw key material never leaves KMS — you send data to KMS to encrypt/decrypt, you never download the key itself. Almost every other AWS service (S3, EBS, RDS, Secrets Manager) uses KMS under the hood for "encryption at rest."

```bash
# Create KMS key
aws kms create-key \
  --description "Application encryption key"

# Create alias
aws kms create-alias \
  --alias-name alias/myapp \
  --target-key-id 1234abcd-12ab-34cd-56ef-1234567890ab

# Encrypt data
aws kms encrypt \
  --key-id alias/myapp \
  --plaintext "sensitive data" \
  --output text \
  --query CiphertextBlob

# Decrypt data
aws kms decrypt \
  --ciphertext-blob fileb://encrypted.txt \
  --output text \
  --query Plaintext | base64 --decode
```

```javascript
import { KMSClient, EncryptCommand, DecryptCommand } from "@aws-sdk/client-kms";

const kms = new KMSClient({ region: "us-east-1" });

// Encrypt data
const encryptData = async (keyId, plaintext) => {
  const command = new EncryptCommand({
    KeyId: keyId,
    Plaintext: Buffer.from(plaintext),
  });
  const response = await kms.send(command);
  return Buffer.from(response.CiphertextBlob).toString("base64");
};

// Decrypt data
const decryptData = async (ciphertext) => {
  const command = new DecryptCommand({
    CiphertextBlob: Buffer.from(ciphertext, "base64"),
  });
  const response = await kms.send(command);
  return Buffer.from(response.Plaintext).toString("utf8");
};

// Usage
const encrypted = await encryptData("alias/myapp", "sensitive data");
const decrypted = await decryptData(encrypted);
```

## AWS Certificate Manager (ACM)

Free HTTPS certificates, automatically renewed — used with CloudFront, ALB, and API Gateway. You either prove domain ownership via DNS validation (add a CNAME record) or import your own existing certificate.

```bash
# Request certificate
aws acm request-certificate \
  --domain-name example.com \
  --subject-alternative-names www.example.com api.example.com \
  --validation-method DNS

# Describe certificate
aws acm describe-certificate \
  --certificate-arn arn:aws:acm:us-east-1:123456789012:certificate/abc-123

# List certificates
aws acm list-certificates

# Import certificate
aws acm import-certificate \
  --certificate fileb://certificate.crt \
  --private-key fileb://private-key.pem \
  --certificate-chain fileb://certificate-chain.crt
```

## AWS WAF (Web Application Firewall)

Sits in front of CloudFront/ALB/API Gateway and inspects each HTTP request against rules — block known bad IPs, rate-limit abusive callers, and use AWS Managed Rules to auto-block common attack patterns like SQL injection.

```bash
# Create IP set
aws wafv2 create-ip-set \
  --name BlockedIPs \
  --scope REGIONAL \
  --ip-address-version IPV4 \
  --addresses 192.0.2.0/24 198.51.100.0/24

# Create web ACL
aws wafv2 create-web-acl \
  --name MyWebACL \
  --scope REGIONAL \
  --default-action Allow={} \
  --rules file://waf-rules.json
```

```json
// waf-rules.json
[
  {
    "Name": "RateLimitRule",
    "Priority": 1,
    "Statement": {
      "RateBasedStatement": {
        "Limit": 2000,
        "AggregateKeyType": "IP"
      }
    },
    "Action": {
      "Block": {}
    },
    "VisibilityConfig": {
      "SampledRequestsEnabled": true,
      "CloudWatchMetricsEnabled": true,
      "MetricName": "RateLimitRule"
    }
  },
  {
    "Name": "SQLiProtection",
    "Priority": 2,
    "Statement": {
      "ManagedRuleGroupStatement": {
        "VendorName": "AWS",
        "Name": "AWSManagedRulesSQLiRuleSet"
      }
    },
    "OverrideAction": {
      "None": {}
    },
    "VisibilityConfig": {
      "SampledRequestsEnabled": true,
      "CloudWatchMetricsEnabled": true,
      "MetricName": "SQLiProtection"
    }
  },
  {
    "Name": "BlockSpecificIPs",
    "Priority": 3,
    "Statement": {
      "IPSetReferenceStatement": {
        "Arn": "arn:aws:wafv2:us-east-1:123456789012:regional/ipset/BlockedIPs/abc-123"
      }
    },
    "Action": {
      "Block": {}
    },
    "VisibilityConfig": {
      "SampledRequestsEnabled": true,
      "CloudWatchMetricsEnabled": true,
      "MetricName": "BlockedIPs"
    }
  }
]
```

## AWS Shield

Standard tier is automatic and free for every AWS customer (basic DDoS protection). Advanced is a paid subscription with more protection, 24/7 support during attacks, and cost protection against scaling charges caused by the attack.

```bash
# Shield Standard is automatic and free

# Shield Advanced (subscribe)
aws shield subscribe-to-shield-advanced

# Create protection
aws shield create-protection \
  --name MyALBProtection \
  --resource-arn arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-alb/abc123

# Associate health check
aws shield associate-health-check \
  --protection-id abc-123 \
  --health-check-arn arn:aws:route53:::healthcheck/abc-123
```

## GuardDuty

Turns on and immediately starts analyzing existing account activity, network logs, and DNS logs with machine learning to flag suspicious behavior (e.g. an API call from a Tor exit node, unusual credential usage) — no agents to install.

```bash
# Enable GuardDuty
aws guardduty create-detector --enable

# List findings
aws guardduty list-findings --detector-id abc123

# Get finding details
aws guardduty get-findings \
  --detector-id abc123 \
  --finding-ids finding-id-1 finding-id-2

# Create filter
aws guardduty create-filter \
  --detector-id abc123 \
  --name HighSeverityFindings \
  --finding-criteria '{
    "Criterion": {
      "severity": {
        "Gte": 7
      }
    }
  }' \
  --action ARCHIVE
```

## AWS Inspector

Automatically and continuously scans EC2 instances, container images, and Lambda functions for known vulnerabilities (CVEs) and unintended network exposure.

```bash
# Create assessment target
aws inspector create-assessment-target \
  --assessment-target-name MyServers \
  --resource-group-arn arn:aws:inspector:us-east-1:123456789012:resourcegroup/abc-123

# Create assessment template
aws inspector create-assessment-template \
  --assessment-target-arn arn:aws:inspector:us-east-1:123456789012:target/abc-123 \
  --assessment-template-name SecurityScan \
  --duration-in-seconds 3600 \
  --rules-package-arns arn:aws:inspector:us-east-1:316112463485:rulespackage/0-R01qwB5Q

# Start assessment run
aws inspector start-assessment-run \
  --assessment-template-arn arn:aws:inspector:us-east-1:123456789012:target/abc-123/template/def-456

# List findings
aws inspector list-findings \
  --assessment-run-arns arn:aws:inspector:us-east-1:123456789012:target/abc-123/template/def-456/run/ghi-789
```

## Security Hub

One dashboard aggregating findings from GuardDuty, Inspector, and industry-standard compliance checks (like CIS AWS Foundations Benchmark) — so you're not checking five different consoles.

```bash
# Enable Security Hub
aws securityhub enable-security-hub

# Enable standards
aws securityhub batch-enable-standards \
  --standards-subscription-requests '[
    {"StandardsArn": "arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0"}
  ]'

# Get findings
aws securityhub get-findings \
  --filters '{
    "SeverityLabel": [{"Value": "CRITICAL", "Comparison": "EQUALS"}],
    "RecordState": [{"Value": "ACTIVE", "Comparison": "EQUALS"}]
  }'

# Update findings
aws securityhub batch-update-findings \
  --finding-identifiers Id=finding-id-1,ProductArn=product-arn \
  --note Text="Reviewed and accepted risk",UpdatedBy=john@example.com \
  --workflow Status=RESOLVED
```

## CloudTrail

Records every API call ever made in your account (console, CLI, SDK, or another AWS service) — who made it, when, from where, and what happened. The single most important service for "who deleted that bucket?" style investigations.

```bash
# Create trail
aws cloudtrail create-trail \
  --name MyTrail \
  --s3-bucket-name my-cloudtrail-bucket

# Start logging
aws cloudtrail start-logging --name MyTrail

# Lookup events
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=CreateBucket \
  --max-results 10

# Create event selector
aws cloudtrail put-event-selectors \
  --trail-name MyTrail \
  --event-selectors '[{
    "ReadWriteType": "All",
    "IncludeManagementEvents": true,
    "DataResources": [{
      "Type": "AWS::S3::Object",
      "Values": ["arn:aws:s3:::my-bucket/*"]
    }]
  }]'
```

## Security Best Practices

```yaml
# Security Checklist
✓ Enable MFA for all IAM users
✓ Use IAM roles instead of access keys
✓ Enable CloudTrail in all regions
✓ Enable GuardDuty for threat detection
✓ Use Secrets Manager for sensitive data
✓ Encrypt data at rest (S3, EBS, RDS)
✓ Encrypt data in transit (TLS/SSL)
✓ Use VPC endpoints to keep traffic private
✓ Implement least privilege principle
✓ Enable AWS Config for compliance
✓ Set up Security Hub for centralized view
✓ Use WAF for web application protection
✓ Enable S3 bucket versioning
✓ Block public S3 bucket access
✓ Regular security audits and reviews
```

---

## Quick interview answers

**Q: Secrets Manager vs Parameter Store — when to use which?**
Secrets Manager for anything needing automatic rotation (DB credentials) — costs more per secret. Parameter Store for general config/feature flags/manually-rotated secrets — free or nearly free.

**Q: What does KMS actually do, in one sentence?**
Creates and safeguards encryption keys, and performs encrypt/decrypt operations on your behalf without ever exposing the raw key.

**Q: WAF vs Shield — what's the difference?**
WAF inspects the *content* of individual web requests (blocks SQL injection, bad IPs, rate abuse) — Layer 7. Shield protects against *volume-based* DDoS floods — network/transport layer. They work together, not instead of each other.

**Q: What does GuardDuty analyze to detect threats?**
CloudTrail logs, VPC Flow Logs, and DNS query logs — using machine learning to flag anomalies, no agent installation required.

**Q: Why is CloudTrail critical for security audits?**
It's the definitive record of "who did what, when, from where" for every API call in the account — without it, you can't reconstruct what happened during an incident.

**Q: Security Hub vs GuardDuty?**
GuardDuty is one specific detector (threat detection). Security Hub is a dashboard that aggregates findings from GuardDuty *and* other tools (Inspector, compliance checks) into a single view — they're complementary, not the same thing.
