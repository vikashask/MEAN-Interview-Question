# IAM (Identity & Access Management)

## Users, Groups & Roles

```bash
# Create IAM user
aws iam create-user --user-name john-doe

# Add user to group
aws iam add-user-to-group --user-name john-doe --group-name developers

# Create access key
aws iam create-access-key --user-name john-doe

# List users
aws iam list-users

# Delete user
aws iam delete-user --user-name john-doe
```

## IAM Policies

```json
// Inline policy example
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}

// Deny specific actions
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "ec2:TerminateInstances",
      "Resource": "*"
    }
  ]
}

// Condition-based policy
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": "*",
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": "203.0.113.0/24"
        }
      }
    }
  ]
}
```

## IAM Roles

```bash
# Create role
aws iam create-role \
  --role-name MyEC2Role \
  --assume-role-policy-document file://trust-policy.json

# Attach policy to role
aws iam attach-role-policy \
  --role-name MyEC2Role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Create instance profile
aws iam create-instance-profile --instance-profile-name MyEC2Profile

# Add role to instance profile
aws iam add-role-to-instance-profile \
  --instance-profile-name MyEC2Profile \
  --role-name MyEC2Role
```

```json
// trust-policy.json (EC2 assume role)
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}

// Lambda assume role
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

## Cross-Account Access

```json
// Role in Account B (123456789012) trusted by Account A
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111111111111:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "unique-external-id"
        }
      }
    }
  ]
}
```

```bash
# Assume role from Account A
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/CrossAccountRole \
  --role-session-name my-session \
  --external-id unique-external-id
```

## AWS SDK with IAM

```javascript
// Node.js SDK v3
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { fromIni } from "@aws-sdk/credential-providers";

// Use credentials from profile
const s3Client = new S3Client({
  region: "us-east-1",
  credentials: fromIni({ profile: "my-profile" }),
});

// Use EC2 instance role (automatic)
const s3Client = new S3Client({ region: "us-east-1" });

// Assume role
import { STSClient, AssumeRoleCommand } from "@aws-sdk/client-sts";

const stsClient = new STSClient({ region: "us-east-1" });
const command = new AssumeRoleCommand({
  RoleArn: "arn:aws:iam::123456789012:role/MyRole",
  RoleSessionName: "my-session",
});

const response = await stsClient.send(command);
const credentials = response.Credentials;

// Use assumed role credentials
const s3Client = new S3Client({
  region: "us-east-1",
  credentials: {
    accessKeyId: credentials.AccessKeyId,
    secretAccessKey: credentials.SecretAccessKey,
    sessionToken: credentials.SessionToken,
  },
});
```

## Permission Boundaries

```json
// Permission boundary limits maximum permissions
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:*", "dynamodb:*"],
      "Resource": "*"
    }
  ]
}
```

```bash
# Create user with permission boundary
aws iam create-user \
  --user-name limited-user \
  --permissions-boundary arn:aws:iam::123456789012:policy/BoundaryPolicy
```

## IAM Best Practices

```bash
# Enable MFA for root account
aws iam enable-mfa-device \
  --user-name root \
  --serial-number arn:aws:iam::123456789012:mfa/root-account-mfa-device \
  --authentication-code1 123456 \
  --authentication-code2 789012

# Rotate access keys
aws iam create-access-key --user-name john-doe
# Update application with new keys
aws iam delete-access-key --user-name john-doe --access-key-id OLD_KEY_ID

# Use STS temporary credentials
aws sts get-session-token --duration-seconds 3600
```

## Service Control Policies (SCPs)

```json
// Deny root account usage
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringLike": {
          "aws:PrincipalArn": "arn:aws:iam::*:root"
        }
      }
    }
  ]
}

// Restrict regions
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": ["us-east-1", "us-west-2"]
        }
      }
    }
  ]
}
```

## IAM Policy Variables

```json
// User-specific S3 bucket access
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": "arn:aws:s3:::my-bucket/${aws:username}/*"
    }
  ]
}

// Time-based access
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:*",
      "Resource": "*",
      "Condition": {
        "DateGreaterThan": {
          "aws:CurrentTime": "2024-01-01T00:00:00Z"
        },
        "DateLessThan": {
          "aws:CurrentTime": "2024-12-31T23:59:59Z"
        }
      }
    }
  ]
}
```
