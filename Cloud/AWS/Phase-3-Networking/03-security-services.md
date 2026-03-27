# AWS Security Services

## AWS Secrets Manager

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
