# IAM (Identity & Access Management)

> **In plain English:** IAM controls *who* can do *what* in your AWS account. Every single AWS API call is checked against IAM first — no IAM permission, no action, no matter how simple the request.

## Real-world analogy

Think of an AWS account like an office building.

- **Users** = employees with an ID badge (a person or an app that needs to log in).
- **Groups** = departments (Finance, Engineering) — badge one person into a department and they inherit that department's access.
- **Roles** = a visitor badge that a robot/machine (EC2, Lambda) or an outside company (another AWS account) can borrow temporarily. Nobody "owns" a role permanently — it's put on and taken off.
- **Policies** = the actual rulebook stapled to a badge or a door ("this badge can open Room 5, cannot open the server room").
- **Trust policy** = the sign on the door of a role that says "only these people/services are allowed to borrow me."

## Core concepts (memorize these first)

| Term | What it means |
|---|---|
| **User** | A permanent identity (person or app) with long-term credentials (password / access keys). |
| **Group** | A bucket of users that all share the same policies. You never attach permissions to a person directly — attach to a group instead. |
| **Role** | A temporary identity with no long-term password/keys. Anything can "assume" a role and get short-lived credentials (this is the #1 best practice over hardcoding keys). |
| **Policy** | A JSON document = a list of Allow/Deny rules. Every policy has `Effect`, `Action`, `Resource`, and optionally `Condition`. |
| **Principal** | *Who* the rule applies to (a user, role, account, or service like `ec2.amazonaws.com`). |
| **Assume Role** | The act of "borrowing" a role's permissions temporarily via AWS STS (Security Token Service). |
| **Permission Boundary** | A hard ceiling — even if a policy grants more, the boundary caps what's actually allowed. |
| **SCP (Service Control Policy)** | An org-wide guardrail applied to whole AWS accounts (used with AWS Organizations), not individual users. |

**The golden rule to remember:** *Explicit Deny always wins.* If any policy says Deny, it overrides every Allow, no matter how many Allows exist.

## Memory hooks

- **"Users log in, Roles are borrowed."** — Users have permanent credentials; roles hand out temporary ones.
- **U-G-R-P** = Users → Groups → Roles → Policies, the order you usually set things up in.
- Deny > explicit Allow > default Deny (nothing is allowed unless something explicitly says Allow).

---

## Users, Groups & Roles

Everyday commands to create a user, put them in a group, and hand them keys to use the CLI/SDK.

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

A policy is just JSON: `Effect` (Allow/Deny) + `Action` (which API calls) + `Resource` (which AWS objects) + optional `Condition` (extra restriction, like "only from this IP").

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

A role has no password. Something has to "assume" it — an EC2 instance, a Lambda function, or a user from another account. The **trust policy** decides who is allowed to assume it; the **permission policy** decides what the role can do once assumed.

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

> **Note on "Instance Profile":** EC2 can't wear a role directly — it wears an *instance profile*, which is basically a wrapper/holder around a role. Just remember: role → wrapped in instance profile → attached to EC2.

## Cross-Account Access

One AWS account (A) can let a role in another account (B) be assumed — no shared passwords needed. The `ExternalId` is an extra password-like check to stop the "confused deputy" problem (someone tricking a third party into assuming the role on their behalf).

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

Three ways an app can get AWS credentials, ranked by preference: (1) let EC2/Lambda hand them out automatically via a role — best, (2) use a named profile locally for dev, (3) explicitly assume a role and pass the temporary keys — used for cross-account or elevated access.

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

A permission boundary is a *ceiling*, not a grant. Even if someone attaches `AdministratorAccess` to a user, the boundary still caps them at whatever the boundary allows. Used so junior admins can create IAM users/roles without being able to escalate themselves to full admin.

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

SCPs live one level above IAM — they apply to entire AWS *accounts* inside an AWS Organization, not to individual users. Think of SCPs as "company-wide rules HR enforces on every department," while IAM policies are "what each department decides for its own staff." An SCP can only take away permissions, never grant them.

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

Policy variables let one policy template apply differently per user, without writing one policy per person.

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

---

## Quick interview answers

**Q: Difference between a Role and a User?**
A User has permanent credentials (password/access keys) for a specific person or app. A Role has no credentials of its own — anything trusted can "assume" it and get temporary credentials that auto-expire.

**Q: Why prefer roles over access keys on EC2/Lambda?**
No secrets to leak, rotate, or store. AWS auto-rotates the temporary credentials behind the scenes.

**Q: What decides who can assume a role?**
The role's **trust policy** (a policy attached to the role itself, separate from its permission policy).

**Q: Explicit Deny vs explicit Allow — which wins?**
Deny always wins, everywhere, no exceptions.

**Q: What's a permission boundary for?**
Capping the maximum permissions a user/role can ever have, even if a more permissive policy gets attached later — used to safely delegate IAM admin work.

**Q: SCP vs IAM policy?**
SCP = account-wide guardrail (Organizations level, can only restrict). IAM policy = grants/denies specific actions to a specific user/role/group inside one account.
