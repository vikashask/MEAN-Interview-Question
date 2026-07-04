# Route53 & CloudFront

> **In plain English:** Route53 is AWS's DNS service — it turns domain names (`example.com`) into IP addresses and decides *which* server should answer based on rules you set. CloudFront is AWS's CDN (Content Delivery Network) — it caches your content at edge locations around the world so users get it fast, from nearby, instead of from one far-away origin server.

## Real-world analogy

- **Route53** = a phone book plus a smart receptionist. Someone asks "where's example.com?" and Route53 doesn't just give one answer — it can say "if you're in Europe, call this branch; if that branch is down, call the backup" (routing policies).
- **Hosted Zone** = the specific page in the phone book for your domain.
- **CloudFront** = a chain of local warehouses (edge locations) that keep a cached copy of your product close to every customer, so nobody has to wait for a shipment from the single factory (your origin server, e.g. S3 or your ALB).
- **Cache invalidation** = telling every local warehouse "throw out the old stock, the factory has an update."
- **Signed URL** = a time-limited VIP ticket — only someone holding it can get the item from the warehouse, and it expires.
- **Lambda@Edge** = a small worker stationed at each local warehouse who can inspect/modify orders on the way in or out, without going back to the factory.

## Core concepts (memorize these first)

| Term | What it means |
|---|---|
| **Hosted Zone** | A container for all DNS records of one domain. |
| **Record types** | `A` = domain → IPv4. `AAAA` = domain → IPv6. `CNAME` = domain → another domain name. `Alias` = AWS-specific "smart CNAME" that can point at the root domain and AWS resources (ALB, CloudFront) for free. |
| **Routing policy** | The *rule* for which answer to give: Simple (one answer), Weighted (split traffic by %), Latency-based (send to the closest/fastest region), Failover (primary/secondary), Geolocation (route by visitor's location). |
| **Health Check** | Route53 actively pings an endpoint; used to power Failover routing (stop sending traffic to a dead primary). |
| **Distribution** | A CloudFront "instance" — the configuration tying an origin (S3/ALB/custom) to cache behavior and a domain. |
| **Origin** | The real backend CloudFront fetches content from when it's not already cached. |
| **Cache Behavior** | Per-path rules (e.g. `/api/*` never cached, `/static/*` cached for a day). |
| **TTL (Time To Live)** | How long a DNS record or cached CloudFront object is considered valid before re-checking. |
| **Invalidation** | Force CloudFront to drop cached copies early (before TTL expires) so it re-fetches fresh content. |
| **OAI / OAC (Origin Access Identity/Control)** | Lets CloudFront be the *only* way to reach a private S3 bucket — the bucket itself stays locked to direct public access. |
| **Signed URL/Cookie** | A URL with a cryptographic signature + expiry, used to serve private/paid content only to authorized users. |

## Memory hooks

- **"Route53 finds the right door. CloudFront makes sure the door is close by."** DNS routing vs content caching — different jobs, often used together.
- Routing policy pick: **need a backup? → Failover. Need speed? → Latency. Need A/B split? → Weighted. Need country rules? → Geolocation.**
- **Alias record = CNAME's smarter AWS-only cousin** — works at the root domain (`example.com`), which plain CNAME can't do.

---

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

`A` record points straight to an IP. `CNAME` points to another domain name (can't be used on the root/apex domain). `Alias` is AWS's special record type that works like a CNAME but is allowed on the root domain and can point directly at AWS resources like an ALB.

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

Same domain name, different backend answer depending on the rule: split traffic (Weighted), route to the nearest/fastest region (Latency), or route to a backup if primary fails (Failover).

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

Route53 actively probes an endpoint on a schedule; if it fails enough times in a row, DNS answers stop pointing there (used by Failover routing).

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

A distribution ties an origin (where the real content lives) to caching rules and a public CloudFront domain (or your custom domain via a certificate).

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

You can point different URL paths at different origins with different caching rules from the same distribution — e.g. `/api/*` always goes live to your backend (no caching), everything else is served from cached S3 static files.

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

Forces edge locations to drop their cached copy immediately instead of waiting for the TTL to expire — use sparingly, it costs money per path invalidated at scale.

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

A time-limited, cryptographically signed link — used to serve private content (paid videos, private files) only to people who were actually granted access, without making the whole distribution public.

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

A Lambda function that runs *at the CDN edge location itself* (close to the user), not in one central region — used to tweak requests/responses on the fly (add security headers, rewrite URLs) without a round trip to your origin server.

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

---

## Quick interview answers

**Q: A record vs CNAME vs Alias?**
A = domain to IPv4 directly. CNAME = domain to another domain name (can't be used at the zone apex/root). Alias = AWS-only "smart CNAME" that works at the root domain and is free to query, typically used to point at ALB/CloudFront/S3.

**Q: How does Route53 Failover routing know when to switch?**
It relies on a Health Check continuously probing the primary endpoint; once it fails the threshold, Route53 stops returning the primary's IP and returns the secondary's instead.

**Q: What does a CloudFront cache behavior actually control?**
Per-URL-path rules: which origin serves that path, whether/how long to cache, which HTTP methods are allowed, and which headers/cookies/query strings vary the cache.

**Q: Why use OAI/OAC with an S3 origin instead of making the bucket public?**
So the S3 bucket stays completely private — only CloudFront (using the OAI/OAC identity) can fetch objects from it, preventing people from bypassing the CDN and hitting S3 directly.

**Q: Signed URL vs Signed Cookie?**
Signed URL grants access to a single file. Signed Cookie grants access to multiple files/paths at once (e.g. an entire video course) without needing a signed link per asset.
