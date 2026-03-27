# DynamoDB & ElastiCache

## DynamoDB Tables

```bash
# Create table
aws dynamodb create-table \
  --table-name Users \
  --attribute-definitions \
    AttributeName=id,AttributeType=S \
    AttributeName=email,AttributeType=S \
  --key-schema \
    AttributeName=id,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --global-secondary-indexes '[{
    "IndexName": "EmailIndex",
    "KeySchema": [{"AttributeName":"email","KeyType":"HASH"}],
    "Projection": {"ProjectionType":"ALL"},
    "ProvisionedThroughput": {"ReadCapacityUnits":5,"WriteCapacityUnits":5}
  }]'

# Switch to on-demand billing
aws dynamodb update-table \
  --table-name Users \
  --billing-mode PAY_PER_REQUEST
```

## DynamoDB with SDK

```javascript
import {
  DynamoDBClient,
  PutItemCommand,
  GetItemCommand,
  QueryCommand,
  ScanCommand,
  UpdateItemCommand,
  DeleteItemCommand,
  BatchWriteItemCommand,
} from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  PutCommand,
  GetCommand,
  QueryCommand as DocQueryCommand,
  UpdateCommand,
  DeleteCommand,
} from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({ region: "us-east-1" });
const docClient = DynamoDBDocumentClient.from(client);

// Put item
const createUser = async (user) => {
  const command = new PutCommand({
    TableName: "Users",
    Item: {
      id: user.id,
      name: user.name,
      email: user.email,
      createdAt: new Date().toISOString(),
    },
  });

  await docClient.send(command);
};

// Get item
const getUser = async (id) => {
  const command = new GetCommand({
    TableName: "Users",
    Key: { id },
  });

  const response = await docClient.send(command);
  return response.Item;
};

// Query with partition key
const getUsersByStatus = async (status) => {
  const command = new DocQueryCommand({
    TableName: "Users",
    IndexName: "StatusIndex",
    KeyConditionExpression: "#status = :status",
    ExpressionAttributeNames: {
      "#status": "status",
    },
    ExpressionAttributeValues: {
      ":status": status,
    },
  });

  const response = await docClient.send(command);
  return response.Items;
};

// Query with sort key condition
const getOrdersByUser = async (userId, fromDate) => {
  const command = new DocQueryCommand({
    TableName: "Orders",
    KeyConditionExpression: "userId = :userId AND createdAt >= :fromDate",
    ExpressionAttributeValues: {
      ":userId": userId,
      ":fromDate": fromDate,
    },
    ScanIndexForward: false, // Descending order
    Limit: 20,
  });

  const response = await docClient.send(command);
  return response.Items;
};

// Update item
const updateUser = async (id, updates) => {
  const command = new UpdateCommand({
    TableName: "Users",
    Key: { id },
    UpdateExpression: "SET #name = :name, updatedAt = :updatedAt",
    ExpressionAttributeNames: {
      "#name": "name",
    },
    ExpressionAttributeValues: {
      ":name": updates.name,
      ":updatedAt": new Date().toISOString(),
    },
    ReturnValues: "ALL_NEW",
  });

  const response = await docClient.send(command);
  return response.Attributes;
};

// Conditional update
const incrementCounter = async (id) => {
  const command = new UpdateCommand({
    TableName: "Users",
    Key: { id },
    UpdateExpression:
      "SET loginCount = if_not_exists(loginCount, :zero) + :inc",
    ExpressionAttributeValues: {
      ":zero": 0,
      ":inc": 1,
    },
    ReturnValues: "UPDATED_NEW",
  });

  await docClient.send(command);
};

// Delete item
const deleteUser = async (id) => {
  const command = new DeleteCommand({
    TableName: "Users",
    Key: { id },
  });

  await docClient.send(command);
};

// Batch write
const batchCreateUsers = async (users) => {
  const chunks = [];
  for (let i = 0; i < users.length; i += 25) {
    chunks.push(users.slice(i, i + 25));
  }

  for (const chunk of chunks) {
    const command = new BatchWriteItemCommand({
      RequestItems: {
        Users: chunk.map((user) => ({
          PutRequest: {
            Item: {
              id: { S: user.id },
              name: { S: user.name },
              email: { S: user.email },
            },
          },
        })),
      },
    });

    await client.send(command);
  }
};
```

## DynamoDB Pagination

```javascript
const getAllUsers = async () => {
  const users = [];
  let lastEvaluatedKey = null;

  do {
    const command = new DocQueryCommand({
      TableName: "Users",
      KeyConditionExpression: "status = :status",
      ExpressionAttributeValues: {
        ":status": "active",
      },
      ExclusiveStartKey: lastEvaluatedKey,
    });

    const response = await docClient.send(command);
    users.push(...response.Items);
    lastEvaluatedKey = response.LastEvaluatedKey;
  } while (lastEvaluatedKey);

  return users;
};
```

## DynamoDB Transactions

```javascript
import { TransactWriteItemsCommand } from "@aws-sdk/client-dynamodb";

const transferBalance = async (fromUserId, toUserId, amount) => {
  const command = new TransactWriteItemsCommand({
    TransactItems: [
      {
        Update: {
          TableName: "Users",
          Key: { id: { S: fromUserId } },
          UpdateExpression: "SET balance = balance - :amount",
          ConditionExpression: "balance >= :amount",
          ExpressionAttributeValues: {
            ":amount": { N: amount.toString() },
          },
        },
      },
      {
        Update: {
          TableName: "Users",
          Key: { id: { S: toUserId } },
          UpdateExpression: "SET balance = balance + :amount",
          ExpressionAttributeValues: {
            ":amount": { N: amount.toString() },
          },
        },
      },
    ],
  });

  try {
    await client.send(command);
  } catch (error) {
    if (error.name === "TransactionCanceledException") {
      console.error("Transaction failed - insufficient balance");
    }
    throw error;
  }
};
```

## DynamoDB Streams

```javascript
// Lambda function to process DynamoDB stream
export const handler = async (event) => {
  for (const record of event.Records) {
    console.log("Event:", record.eventName);

    if (record.eventName === "INSERT") {
      const newItem = record.dynamodb.NewImage;
      console.log("New item:", newItem);

      // Send welcome email for new users
      await sendWelcomeEmail(newItem.email.S);
    }

    if (record.eventName === "MODIFY") {
      const oldItem = record.dynamodb.OldImage;
      const newItem = record.dynamodb.NewImage;

      // Log changes
      console.log("Updated from:", oldItem);
      console.log("Updated to:", newItem);
    }

    if (record.eventName === "REMOVE") {
      const oldItem = record.dynamodb.OldImage;
      console.log("Deleted item:", oldItem);
    }
  }
};
```

## DynamoDB DAX (Caching)

```javascript
import AmazonDaxClient from "amazon-dax-client";

const dax = new AmazonDaxClient({
  endpoints: ["mycluster.dax-clusters.us-east-1.amazonaws.com:8111"],
  region: "us-east-1",
});

const daxDocClient = DynamoDBDocumentClient.from(dax);

// Queries go through DAX cache
const getUser = async (id) => {
  const command = new GetCommand({
    TableName: "Users",
    Key: { id },
  });

  const response = await daxDocClient.send(command);
  return response.Item;
};
```

## ElastiCache Redis

```bash
# Create Redis cluster
aws elasticache create-cache-cluster \
  --cache-cluster-id my-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1 \
  --cache-subnet-group-name my-subnet-group \
  --security-group-ids sg-12345

# Create replication group (Multi-AZ)
aws elasticache create-replication-group \
  --replication-group-id my-redis-cluster \
  --replication-group-description "Production Redis" \
  --engine redis \
  --cache-node-type cache.r6g.large \
  --num-cache-clusters 3 \
  --automatic-failover-enabled \
  --at-rest-encryption-enabled \
  --transit-encryption-enabled
```

## Redis with Node.js

```javascript
import { createClient } from "redis";

// Connect to Redis
const redis = createClient({
  socket: {
    host: process.env.REDIS_HOST,
    port: 6379,
  },
  password: process.env.REDIS_PASSWORD,
});

redis.on("error", (err) => console.error("Redis error:", err));
await redis.connect();

// String operations
await redis.set("user:123", JSON.stringify({ name: "John", age: 30 }));
const user = JSON.parse(await redis.get("user:123"));

// Set with expiration
await redis.setEx("session:abc123", 3600, JSON.stringify({ userId: 123 }));

// Hash operations
await redis.hSet("user:123", {
  name: "John",
  email: "john@example.com",
  age: "30",
});
const userData = await redis.hGetAll("user:123");

// List operations
await redis.lPush(
  "notifications:123",
  JSON.stringify({ message: "New comment" })
);
const notifications = await redis.lRange("notifications:123", 0, -1);

// Set operations
await redis.sAdd("tags:post:1", ["javascript", "nodejs", "aws"]);
const tags = await redis.sMembers("tags:post:1");

// Sorted set operations
await redis.zAdd("leaderboard", [
  { score: 100, value: "user1" },
  { score: 200, value: "user2" },
  { score: 150, value: "user3" },
]);
const topUsers = await redis.zRange("leaderboard", 0, 9, { REV: true });

// Increment counter
await redis.incr("page:views");
await redis.incrBy("user:123:points", 10);

// Pipeline for bulk operations
const pipeline = redis.multi();
pipeline.set("key1", "value1");
pipeline.set("key2", "value2");
pipeline.incr("counter");
await pipeline.exec();

// Pub/Sub
const subscriber = redis.duplicate();
await subscriber.connect();

subscriber.subscribe("notifications", (message) => {
  console.log("Received:", message);
});

// Publisher
await redis.publish(
  "notifications",
  JSON.stringify({ type: "new_order", orderId: 123 })
);
```

## Caching Patterns

```javascript
// Cache-aside pattern
const getUser = async (userId) => {
  const cacheKey = `user:${userId}`;

  // Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // Cache miss - fetch from database
  const user = await User.findByPk(userId);

  // Store in cache
  await redis.setEx(cacheKey, 3600, JSON.stringify(user));

  return user;
};

// Write-through cache
const updateUser = async (userId, updates) => {
  // Update database
  const user = await User.update(updates, { where: { id: userId } });

  // Update cache
  const cacheKey = `user:${userId}`;
  await redis.setEx(cacheKey, 3600, JSON.stringify(user));

  return user;
};

// Cache invalidation
const deleteUser = async (userId) => {
  // Delete from database
  await User.destroy({ where: { id: userId } });

  // Invalidate cache
  await redis.del(`user:${userId}`);
};

// Distributed locking
const acquireLock = async (lockKey, timeout = 10) => {
  const result = await redis.set(lockKey, "1", {
    NX: true,
    EX: timeout,
  });
  return result === "OK";
};

const releaseLock = async (lockKey) => {
  await redis.del(lockKey);
};

// Usage
const processOrder = async (orderId) => {
  const lockKey = `lock:order:${orderId}`;

  if (await acquireLock(lockKey, 30)) {
    try {
      // Process order
      await processOrderLogic(orderId);
    } finally {
      await releaseLock(lockKey);
    }
  } else {
    throw new Error("Order is being processed");
  }
};
```

## Redis Session Store

```javascript
import session from "express-session";
import RedisStore from "connect-redis";

app.use(
  session({
    store: new RedisStore({ client: redis }),
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: true,
      httpOnly: true,
      maxAge: 1000 * 60 * 60 * 24, // 24 hours
    },
  })
);
```
