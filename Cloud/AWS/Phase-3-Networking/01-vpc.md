# VPC (Virtual Private Cloud)

> **In plain English:** A VPC is your own private, isolated network inside AWS — like having your own fenced plot of land in a shared city. Everything else (EC2, RDS, Lambda-in-VPC) lives inside subnets carved out of that plot.

## Real-world analogy

Think of a VPC as a gated housing complex:

- **VPC** = the whole complex, with its own address range (CIDR block).
- **Subnet** = one street inside the complex. **Public subnet** = a street with a direct gate to the outside world (Internet Gateway attached). **Private subnet** = an inner street with no direct gate — residents can go out via a supervised exit (NAT Gateway) but nobody outside can walk straight in.
- **Route table** = the complex's signage telling traffic "to reach outside, go through this gate."
- **Internet Gateway (IGW)** = the complex's main public gate — two-way traffic to the internet.
- **NAT Gateway** = a one-way turnstile in a private street — residents (private subnet) can go out to fetch something (e.g. software updates), but strangers from outside can't come in through it.
- **Security Group** = a bouncer standing at *each house's door* (attached to individual EC2 instances), checking every visitor.
- **Network ACL (NACL)** = a checkpoint at the *street entrance* (attached to the whole subnet), checking everyone entering/leaving that street.
- **VPC Peering / Transit Gateway** = a private tunnel connecting two separate complexes (VPCs) so residents can visit each other without going through the public internet.
- **VPC Endpoint** = a private back-door directly into an AWS service (like S3) so traffic never has to leave the complex to reach it.

## Core concepts (memorize these first)

| Term | What it means |
|---|---|
| **CIDR block** | The IP address range for the VPC/subnet, e.g. `10.0.0.0/16` (~65k IPs) or `10.0.1.0/24` (256 IPs). |
| **Subnet** | A slice of the VPC's IP range, tied to one Availability Zone. |
| **Public subnet** | Has a route to an Internet Gateway → resources can have public IPs and be reached from the internet. |
| **Private subnet** | No direct route to an Internet Gateway → not reachable from the internet directly. |
| **Internet Gateway (IGW)** | Lets a VPC talk to the public internet — two-way. |
| **NAT Gateway** | Lets private-subnet resources *initiate* outbound internet traffic (e.g. download updates), but nothing from outside can initiate a connection in — one-way. |
| **Security Group (SG)** | Firewall at the instance level. Stateful (if you allow inbound, the matching outbound reply is automatically allowed). |
| **Network ACL (NACL)** | Firewall at the subnet level. Stateless (you must explicitly allow both inbound AND outbound, even for replies). |
| **VPC Peering** | 1-to-1 private connection between two VPCs. |
| **Transit Gateway** | A central hub connecting many VPCs together (better than peering when you have many VPCs — peering doesn't scale well past a handful). |
| **VPC Endpoint** | A private connection from your VPC directly to an AWS service (S3, DynamoDB...) without going over the public internet. |
| **VPC Flow Logs** | Records of all IP traffic going in/out of network interfaces — used for troubleshooting/auditing. |

**The #1 interview trap:** Security Group vs NACL. SG = stateful, applies per-instance, only supports "Allow" rules. NACL = stateless, applies per-subnet, supports both "Allow" and explicit "Deny" rules.

## Memory hooks

- **"Public subnet has a gate (IGW). Private subnet has a one-way turnstile (NAT)."**
- **SG = bodyguard for a person (stateful, remembers the conversation). NACL = checkpoint for a street (stateless, checks every single packet both ways).**
- CIDR sizing to remember: `/16` = big VPC (~65k IPs), `/24` = normal subnet (256 IPs, 251 usable — AWS reserves 5).

---

## Create VPC

```bash
# Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# Add name tag
aws ec2 create-tags \
  --resources vpc-12345 \
  --tags Key=Name,Value=MyVPC

# Enable DNS hostnames
aws ec2 modify-vpc-attribute \
  --vpc-id vpc-12345 \
  --enable-dns-hostnames
```

## Subnets

Public subnet gets `map-public-ip-on-launch` so instances auto-receive a public IP. Private subnet doesn't.

```bash
# Create public subnet
aws ec2 create-subnet \
  --vpc-id vpc-12345 \
  --cidr-block 10.0.1.0/24 \
  --availability-zone us-east-1a

# Create private subnet
aws ec2 create-subnet \
  --vpc-id vpc-12345 \
  --cidr-block 10.0.2.0/24 \
  --availability-zone us-east-1b

# Enable auto-assign public IP
aws ec2 modify-subnet-attribute \
  --subnet-id subnet-12345 \
  --map-public-ip-on-launch
```

## Internet Gateway

A subnet only becomes "public" once its route table sends `0.0.0.0/0` (all internet-bound traffic) to an Internet Gateway.

```bash
# Create IGW
aws ec2 create-internet-gateway

# Attach to VPC
aws ec2 attach-internet-gateway \
  --internet-gateway-id igw-12345 \
  --vpc-id vpc-12345

# Create route table
aws ec2 create-route-table --vpc-id vpc-12345

# Add route to IGW
aws ec2 create-route \
  --route-table-id rtb-12345 \
  --destination-cidr-block 0.0.0.0/0 \
  --gateway-id igw-12345

# Associate with subnet
aws ec2 associate-route-table \
  --route-table-id rtb-12345 \
  --subnet-id subnet-12345
```

## NAT Gateway

Lives *inside a public subnet* but serves *private subnet* traffic — private resources route their outbound internet traffic through it. It needs an Elastic IP to have a stable public-facing address.

```bash
# Allocate Elastic IP
aws ec2 allocate-address --domain vpc

# Create NAT Gateway in public subnet
aws ec2 create-nat-gateway \
  --subnet-id subnet-public-12345 \
  --allocation-id eipalloc-12345

# Add route to NAT Gateway for private subnet
aws ec2 create-route \
  --route-table-id rtb-private-12345 \
  --destination-cidr-block 0.0.0.0/0 \
  --nat-gateway-id nat-12345
```

## Security Groups

Stateful, per-instance firewall — only "Allow" rules exist (no explicit deny needed; anything not allowed is blocked by default). You can even reference another security group as the source, instead of an IP range (common pattern: "only let the ALB's security group talk to the app's security group").

```bash
# Create security group
aws ec2 create-security-group \
  --group-name web-sg \
  --description "Web servers" \
  --vpc-id vpc-12345

# Add inbound rule
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345 \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

# Add HTTPS rule
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345 \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

# Add SSH rule (restricted)
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345 \
  --protocol tcp \
  --port 22 \
  --cidr 203.0.113.0/24

# Reference another security group
aws ec2 authorize-security-group-ingress \
  --group-id sg-app-12345 \
  --protocol tcp \
  --port 3000 \
  --source-group sg-alb-12345
```

## Network ACLs

Stateless, per-subnet firewall — you must explicitly allow both directions (inbound rule for the request, outbound rule for the reply), and rules are evaluated in order by `rule-number` (lowest first).

```bash
# Create network ACL
aws ec2 create-network-acl --vpc-id vpc-12345

# Add inbound rule (allow HTTP)
aws ec2 create-network-acl-entry \
  --network-acl-id acl-12345 \
  --rule-number 100 \
  --protocol tcp \
  --port-range From=80,To=80 \
  --cidr-block 0.0.0.0/0 \
  --egress false \
  --rule-action allow

# Add outbound rule
aws ec2 create-network-acl-entry \
  --network-acl-id acl-12345 \
  --rule-number 100 \
  --protocol tcp \
  --port-range From=1024,To=65535 \
  --cidr-block 0.0.0.0/0 \
  --egress true \
  --rule-action allow
```

## VPC Peering

A private, direct link between two VPCs (even across regions) — but it's 1-to-1 and doesn't transitively connect a third VPC (if A peers with B, and B peers with C, A still can't reach C through B).

```bash
# Create peering connection
aws ec2 create-vpc-peering-connection \
  --vpc-id vpc-12345 \
  --peer-vpc-id vpc-67890 \
  --peer-region us-west-2

# Accept peering connection
aws ec2 accept-vpc-peering-connection \
  --vpc-peering-connection-id pcx-12345

# Add route to peer VPC
aws ec2 create-route \
  --route-table-id rtb-12345 \
  --destination-cidr-block 10.1.0.0/16 \
  --vpc-peering-connection-id pcx-12345
```

## VPC Endpoints

Lets resources inside your VPC reach S3/DynamoDB/etc *without* going over the public internet or through a NAT Gateway — cheaper and more secure. Gateway endpoints (S3, DynamoDB) are free; Interface endpoints (most other services) cost a bit but work the same way.

```bash
# S3 Gateway endpoint
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-12345 \
  --service-name com.amazonaws.us-east-1.s3 \
  --route-table-ids rtb-12345

# Interface endpoint (DynamoDB)
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-12345 \
  --service-name com.amazonaws.us-east-1.dynamodb \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-12345 \
  --security-group-ids sg-12345
```

## VPC Flow Logs

Captures metadata about every packet in/out of your VPC (source, destination, port, accept/reject) — essential for debugging "why can't X reach Y" and for security audits.

```bash
# Create flow log
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-12345 \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name /aws/vpc/flowlogs \
  --deliver-logs-permission-arn arn:aws:iam::123456789012:role/flowlogsRole

# Query flow logs
aws logs filter-log-events \
  --log-group-name /aws/vpc/flowlogs \
  --filter-pattern "[version, account, eni, source, destination, srcport, destport, protocol, packets, bytes, start, end, action=REJECT, status]"
```

## VPC with SDK

```javascript
import {
  EC2Client,
  CreateVpcCommand,
  CreateSubnetCommand,
} from "@aws-sdk/client-ec2";

const ec2 = new EC2Client({ region: "us-east-1" });

// Create VPC
const createVPC = async () => {
  const vpcCommand = new CreateVpcCommand({
    CidrBlock: "10.0.0.0/16",
    TagSpecifications: [
      {
        ResourceType: "vpc",
        Tags: [{ Key: "Name", Value: "MyVPC" }],
      },
    ],
  });

  const { Vpc } = await ec2.send(vpcCommand);
  return Vpc.VpcId;
};

// Create subnets
const createSubnets = async (vpcId) => {
  const publicSubnet = new CreateSubnetCommand({
    VpcId: vpcId,
    CidrBlock: "10.0.1.0/24",
    AvailabilityZone: "us-east-1a",
    TagSpecifications: [
      {
        ResourceType: "subnet",
        Tags: [{ Key: "Name", Value: "Public-Subnet" }],
      },
    ],
  });

  const privateSubnet = new CreateSubnetCommand({
    VpcId: vpcId,
    CidrBlock: "10.0.2.0/24",
    AvailabilityZone: "us-east-1b",
    TagSpecifications: [
      {
        ResourceType: "subnet",
        Tags: [{ Key: "Name", Value: "Private-Subnet" }],
      },
    ],
  });

  const [publicResult, privateResult] = await Promise.all([
    ec2.send(publicSubnet),
    ec2.send(privateSubnet),
  ]);

  return {
    publicSubnetId: publicResult.Subnet.SubnetId,
    privateSubnetId: privateResult.Subnet.SubnetId,
  };
};
```

## Transit Gateway

When you have more than a handful of VPCs, peering every pair becomes unmanageable (N VPCs need up to N×(N-1)/2 peering connections). Transit Gateway is a central hub — every VPC connects once to the hub instead.

```bash
# Create transit gateway
aws ec2 create-transit-gateway \
  --description "Central TGW" \
  --options "AmazonSideAsn=64512,AutoAcceptSharedAttachments=enable"

# Attach VPC
aws ec2 create-transit-gateway-vpc-attachment \
  --transit-gateway-id tgw-12345 \
  --vpc-id vpc-12345 \
  --subnet-ids subnet-12345 subnet-67890

# Create TGW route table
aws ec2 create-transit-gateway-route-table \
  --transit-gateway-id tgw-12345

# Add route
aws ec2 create-transit-gateway-route \
  --transit-gateway-route-table-id tgw-rtb-12345 \
  --destination-cidr-block 10.1.0.0/16 \
  --transit-gateway-attachment-id tgw-attach-12345
```

## Best Practices

```yaml
# VPC Design Best Practices
- Use /16 CIDR for VPC (65,536 IPs)
- Use /24 CIDR for subnets (256 IPs per subnet)
- Reserve subnets for future use
- Use multiple AZs for high availability
- Separate public and private subnets
- Use NAT Gateway in each AZ for redundancy
- Enable VPC Flow Logs for monitoring
- Use VPC endpoints to avoid internet traffic
- Implement defense in depth (NACL + SG)
- Tag all resources consistently
```

---

## Quick interview answers

**Q: Security Group vs Network ACL?**
SG: stateful, instance-level, Allow-only rules. NACL: stateless, subnet-level, supports explicit Allow and Deny, rules processed in numeric order.

**Q: What makes a subnet "public"?**
Its route table has a route to an Internet Gateway for `0.0.0.0/0` — nothing more. (Auto-assign public IP is a convenience setting, not what defines "public.")

**Q: Why use a NAT Gateway instead of just putting everything in a public subnet?**
Security — private resources (like a database) should never be directly reachable from the internet, but they may still need outbound access (e.g., to download patches or call external APIs). NAT gives one-way outbound access only.

**Q: VPC Peering vs Transit Gateway — when to use which?**
Peering for a small number of VPCs needing direct connections. Transit Gateway when you have many VPCs — avoids the N² peering explosion and centralizes routing.

**Q: Why use a VPC Endpoint instead of just routing through NAT to reach S3?**
Lower latency/cost (no NAT Gateway data processing charges), traffic never touches the public internet, and it works even without any internet access configured at all.
