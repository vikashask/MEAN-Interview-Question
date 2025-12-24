# VPC (Virtual Private Cloud)

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
