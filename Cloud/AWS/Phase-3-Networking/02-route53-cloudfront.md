# Route53 & CloudFront

## Route53 Hosted Zones

```bash
# Create hosted zone
aws route53 create-hosted-zone \
  --name example.com \
  --caller-reference $(date +%s)

# List hosted zones
aws route53 list-hosted-zones

# Get nameservers
aws route53 get-hosted-zone --id Z1234567890ABC
```

## DNS Records

```bash
# Create A record
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "www.example.com",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [{"Value": "192.0.2.1"}]
      }
    }]
  }'

# Create CNAME record
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "blog.example.com",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "www.example.com"}]
      }
    }]
  }'

# Create Alias record (ALB)
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "api.example.com",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "Z35SXDOTRQ7X7K",
          "DNSName": "my-alb-123456.us-east-1.elb.amazonaws.com",
          "EvaluateTargetHealth": true
        }
      }
    }]
  }'
```

## Routing Policies

```javascript
import {
  Route53Client,
  ChangeResourceRecordSetsCommand,
} from "@aws-sdk/client-route-53";

const route53 = new Route53Client({ region: "us-east-1" });

// Weighted routing (50-50 split)
const createWeightedRecords = async () => {
  const command = new ChangeResourceRecordSetsCommand({
    HostedZoneId: "Z1234567890ABC",
    ChangeBatch: {
      Changes: [
        {
          Action: "CREATE",
          ResourceRecordSet: {
            Name: "app.example.com",
            Type: "A",
            SetIdentifier: "Server-1",
            Weight: 50,
            TTL: 60,
            ResourceRecords: [{ Value: "192.0.2.1" }],
          },
        },
        {
          Action: "CREATE",
          ResourceRecordSet: {
            Name: "app.example.com",
            Type: "A",
            SetIdentifier: "Server-2",
            Weight: 50,
            TTL: 60,
            ResourceRecords: [{ Value: "192.0.2.2" }],
          },
        },
      ],
    },
  });

  await route53.send(command);
};

// Latency-based routing
const createLatencyRecords = async () => {
  const command = new ChangeResourceRecordSetsCommand({
    HostedZoneId: "Z1234567890ABC",
    ChangeBatch: {
      Changes: [
        {
          Action: "CREATE",
          ResourceRecordSet: {
            Name: "app.example.com",
            Type: "A",
            SetIdentifier: "US-East",
            Region: "us-east-1",
            TTL: 60,
            ResourceRecords: [{ Value: "192.0.2.1" }],
          },
        },
        {
          Action: "CREATE",
          ResourceRecordSet: {
            Name: "app.example.com",
            Type: "A",
            SetIdentifier: "EU-West",
            Region: "eu-west-1",
            TTL: 60,
            ResourceRecords: [{ Value: "198.51.100.1" }],
          },
        },
      ],
    },
  });

  await route53.send(command);
};

// Failover routing
const createFailoverRecords = async () => {
  const command = new ChangeResourceRecordSetsCommand({
    HostedZoneId: "Z1234567890ABC",
    ChangeBatch: {
      Changes: [
        {
          Action: "CREATE",
          ResourceRecordSet: {
            Name: "app.example.com",
            Type: "A",
            SetIdentifier: "Primary",
            Failover: "PRIMARY",
            TTL: 60,
            ResourceRecords: [{ Value: "192.0.2.1" }],
            HealthCheckId: "abc123",
          },
        },
        {
          Action: "CREATE",
          ResourceRecordSet: {
            Name: "app.example.com",
            Type: "A",
            SetIdentifier: "Secondary",
            Failover: "SECONDARY",
            TTL: 60,
            ResourceRecords: [{ Value: "192.0.2.2" }],
          },
        },
      ],
    },
  });

  await route53.send(command);
};
```

## Health Checks

```bash
# Create health check
aws route53 create-health-check \
  --health-check-config '{
    "Type": "HTTPS",
    "ResourcePath": "/health",
    "FullyQualifiedDomainName": "api.example.com",
    "Port": 443,
    "RequestInterval": 30,
    "FailureThreshold": 3
  }'

# Associate with alarm
aws route53 update-health-check \
  --health-check-id abc123 \
  --alarm-identifier Region=us-east-1,Name=HealthCheckAlarm
```

## CloudFront Distribution

```bash
# Create distribution
aws cloudfront create-distribution \
  --origin-domain-name my-bucket.s3.amazonaws.com \
  --default-root-object index.html
```

```javascript
import {
  CloudFrontClient,
  CreateDistributionCommand,
} from "@aws-sdk/client-cloudfront";

const cloudfront = new CloudFrontClient({ region: "us-east-1" });

// Create CloudFront distribution
const createDistribution = async () => {
  const command = new CreateDistributionCommand({
    DistributionConfig: {
      CallerReference: Date.now().toString(),
      Comment: "My CDN distribution",
      Enabled: true,
      Origins: {
        Quantity: 1,
        Items: [
          {
            Id: "S3-my-bucket",
            DomainName: "my-bucket.s3.amazonaws.com",
            S3OriginConfig: {
              OriginAccessIdentity: "origin-access-identity/cloudfront/ABCDEFG",
            },
          },
        ],
      },
      DefaultCacheBehavior: {
        TargetOriginId: "S3-my-bucket",
        ViewerProtocolPolicy: "redirect-to-https",
        AllowedMethods: {
          Quantity: 2,
          Items: ["GET", "HEAD"],
        },
        ForwardedValues: {
          QueryString: false,
          Cookies: { Forward: "none" },
        },
        MinTTL: 0,
        DefaultTTL: 86400,
        MaxTTL: 31536000,
        Compress: true,
      },
      Aliases: {
        Quantity: 1,
        Items: ["cdn.example.com"],
      },
      ViewerCertificate: {
        ACMCertificateArn:
          "arn:aws:acm:us-east-1:123456789012:certificate/abc-123",
        SSLSupportMethod: "sni-only",
        MinimumProtocolVersion: "TLSv1.2_2021",
      },
    },
  });

  const response = await cloudfront.send(command);
  return response.Distribution.Id;
};
```

## CloudFront Cache Behaviors

```javascript
// Multiple cache behaviors for different paths
const distributionConfig = {
  CallerReference: Date.now().toString(),
  Enabled: true,
  Origins: {
    Quantity: 2,
    Items: [
      {
        Id: "S3-Static",
        DomainName: "static.s3.amazonaws.com",
        S3OriginConfig: {
          OriginAccessIdentity: "origin-access-identity/cloudfront/ABCDEFG",
        },
      },
      {
        Id: "ALB-API",
        DomainName: "api-alb.us-east-1.elb.amazonaws.com",
        CustomOriginConfig: {
          HTTPPort: 80,
          HTTPSPort: 443,
          OriginProtocolPolicy: "https-only",
        },
      },
    ],
  },
  DefaultCacheBehavior: {
    TargetOriginId: "S3-Static",
    ViewerProtocolPolicy: "redirect-to-https",
    CachePolicyId: "658327ea-f89d-4fab-a63d-7e88639e58f6", // Managed-CachingOptimized
    Compress: true,
  },
  CacheBehaviors: {
    Quantity: 1,
    Items: [
      {
        PathPattern: "/api/*",
        TargetOriginId: "ALB-API",
        ViewerProtocolPolicy: "https-only",
        AllowedMethods: {
          Quantity: 7,
          Items: ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"],
        },
        CachePolicyId: "4135ea2d-6df8-44a3-9df3-4b5a84be39ad", // Managed-CachingDisabled
        OriginRequestPolicyId: "216adef6-5c7f-47e4-b989-5492eafa07d3", // Managed-AllViewer
      },
    ],
  },
};
```

## CloudFront Invalidation

```bash
# Create invalidation
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"

# Invalidate specific paths
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/images/*" "/css/*" "/index.html"
```

```javascript
import { CreateInvalidationCommand } from "@aws-sdk/client-cloudfront";

const invalidateCache = async (distributionId, paths) => {
  const command = new CreateInvalidationCommand({
    DistributionId: distributionId,
    InvalidationBatch: {
      CallerReference: Date.now().toString(),
      Paths: {
        Quantity: paths.length,
        Items: paths,
      },
    },
  });

  await cloudfront.send(command);
};

// Usage
await invalidateCache("E1234567890ABC", ["/images/*", "/index.html"]);
```

## Signed URLs

```javascript
import { getSignedUrl } from "@aws-sdk/cloudfront-signer";
import { readFileSync } from "fs";

// Generate signed URL
const generateSignedUrl = (url, expiresInSeconds = 3600) => {
  const privateKey = readFileSync("./private-key.pem", "utf8");
  const keyPairId = "APKAEXAMPLE";
  const dateLessThan = new Date(Date.now() + expiresInSeconds * 1000);

  return getSignedUrl({
    url,
    keyPairId,
    dateLessThan,
    privateKey,
  });
};

// Usage
const signedUrl = generateSignedUrl(
  "https://cdn.example.com/private/video.mp4",
  3600
);
console.log(signedUrl);
```

## Lambda@Edge

```javascript
// Viewer request function (modify headers)
export const handler = async (event) => {
  const request = event.Records[0].cf.request;
  const headers = request.headers;

  // Add security headers
  headers["strict-transport-security"] = [
    {
      key: "Strict-Transport-Security",
      value: "max-age=63072000; includeSubdomains; preload",
    },
  ];

  return request;
};

// Origin response function (customize caching)
export const handler = async (event) => {
  const response = event.Records[0].cf.response;
  const headers = response.headers;

  // Set cache control
  headers["cache-control"] = [
    {
      key: "Cache-Control",
      value: "max-age=3600",
    },
  ];

  return response;
};
```
