# DynamoDB & ElastiCache

> **In plain English:** DynamoDB is AWS's NoSQL database — no fixed schema, scales to any size automatically, and is fast as long as you query it the way it's designed to be queried (by key). ElastiCache is an in-memory cache (Redis or Memcached) that sits in front of a slower database to make repeat reads near-instant.

## Real-world analogy

- **DynamoDB table** = a giant filing system organized entirely by a label (Partition Key) you choose upfront — fast if you look things up by that label, slow/impossible if you try to search by something else without an index.
- **Partition Key** = the drawer label. **Sort Key** = the order of folders *inside* that drawer (lets you range-query within one partition, e.g. "all of user123's orders after March 1st").
- **GSI (Global Secondary Index)** = an entirely separate filing cabinet, auto-kept in sync, organized by a *different* label — lets you query by fields other than the main partition key.
- **DynamoDB Streams** = a person standing by the filing cabinet writing down every single change (insert/update/delete) as it happens, so other systems can react.
- **DAX** = a sticky-note board in front of the filing cabinet — check the sticky notes first (cache) before walking to the actual cabinet (much faster for repeat reads).
- **ElastiCache/Redis** = a whiteboard next to your desk — near-instant read/write, but it's memory only (can lose data if it's not persisted/replicated), used as a cache in front of a "real" database.

## Core concepts (memorize these first)

| Term | What it means |
|---|---|
| **Partition Key (Hash Key)** | Determines which physical partition an item lives on; required for every item, used for fast direct lookups. |
| **Sort Key (Range Key)** | Optional second key — lets multiple items share a partition key but be ordered/range-queried within it. |
| **GSI (Global Secondary Index)** | An alternate view of the table with a different partition/sort key — lets you query by other attributes. |
| **LSI (Local Secondary Index)** | Same partition key as the base table, different sort key — must be created at table creation time, unlike GSIs. |
| **Provisioned vs On-Demand capacity** | Provisioned = you set fixed read/write capacity (cheaper, predictable load). On-Demand = pay per request, auto-scales instantly (unpredictable/spiky load). |
| **DynamoDB Streams** | A change log of every insert/update/delete — commonly consumed by Lambda for event-driven side effects. |
| **DAX** | An in-memory cache specifically built in front of DynamoDB — microsecond reads for repeat queries. |
| **Transactions** | All-or-nothing multi-item writes (e.g. transferring balance between two users atomically). |
| **Redis vs Memcached** | Redis: richer data structures (lists, sets, sorted sets, pub/sub), persistence, replication. Memcached: simpler, multi-threaded, purely a cache with no persistence — Redis is almost always the default choice today. |
| **Cache-aside pattern** | App checks cache first; on a miss, reads from the real database and then populates the cache. |
| **Write-through pattern** | Every write updates both the database and the cache at the same time, so the cache is never stale. |

**The #1 interview trap:** Query vs Scan in DynamoDB. **Query** uses the partition key (and optionally sort key) — fast, efficient, the "correct" way. **Scan** reads the *entire table* and filters afterward — slow, expensive, avoid in production hot paths.

## Memory hooks

- **"Partition Key = which drawer. Sort Key = order inside the drawer."**
- **GSI = new cabinet, new keys, created anytime. LSI = same drawer label, different order, locked in at table creation.**
- Cache-aside = "check cache, miss? go to DB, then remember it for next time." Write-through = "update both at once, always in sync."
- Redis wins almost every "which cache" interview question unless the answer specifically calls for Memcached's simplicity/multi-threading.

---

## DynamoDB Tables

Every table needs at least a partition key. GSIs let you add alternate query patterns after the fact.

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

`DynamoDBDocumentClient` lets you use plain JS objects instead of DynamoDB's verbose typed attribute format. Note `Query` (efficient, uses keys) is used far more than `Scan` (reads everything).

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

Like S3, DynamoDB never returns unlimited results in one call — loop using `LastEvaluatedKey` until it comes back empty/undefined.

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

All-or-nothing writes across multiple items — if any condition fails (like insufficient balance), the *entire* transaction is cancelled, none of the writes happen.

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

A real-time change feed of your table — every insert/update/delete produces a record a Lambda can react to. Classic use: send a welcome email the moment a new user row is inserted.

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

DAX is a purpose-built in-memory cache that sits in front of DynamoDB — same API, but repeat reads return in microseconds instead of milliseconds.

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

A replication group gives you Multi-AZ automatic failover for Redis — same idea as RDS Multi-AZ, but for your cache layer.

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

Redis isn't just key-value — it has rich data structures: strings, hashes (like objects), lists, sets, and sorted sets (great for leaderboards).

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

Two main strategies, worth memorizing by name for interviews: **cache-aside** (lazy, only caches what's actually requested) and **write-through** (always keeps cache fresh but writes cost a bit more).

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

A very common real-world use of Redis: storing user login sessions outside your app server, so any server instance can read the same session (needed once you have more than one app server).

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

---

## Quick interview answers

**Q: Query vs Scan in DynamoDB — why does it matter?**
Query uses the partition key (and optionally sort key) to jump straight to the relevant data — fast and cheap. Scan reads the *entire table* then filters — slow and expensive at scale. Always design your table/indexes so you can Query, not Scan.

**Q: GSI vs LSI?**
GSI: different partition + sort key, can be added anytime after table creation, has its own capacity. LSI: same partition key as the base table but a different sort key, must be defined at table creation time, shares the base table's capacity.

**Q: When would you choose On-Demand vs Provisioned capacity?**
On-Demand for unpredictable/spiky traffic where you don't want to manage capacity planning. Provisioned (with auto scaling) for steady, predictable traffic — cheaper per-request at scale.

**Q: Redis vs Memcached?**
Redis supports richer data types (lists, sets, sorted sets, hashes), persistence, and replication/pub-sub. Memcached is simpler and multi-threaded, purely an in-memory key-value cache with no persistence. Redis is the default pick unless you specifically need Memcached's simplicity.

**Q: Cache-aside vs write-through?**
Cache-aside: app checks cache, on miss reads DB and populates cache — cache only holds what's been requested (lazy). Write-through: every write updates the cache immediately alongside the DB — cache is never stale, but every write costs more.

**Q: What problem does DAX solve that Query/Scan optimization doesn't?**
DAX caches DynamoDB reads in-memory (microsecond latency) without changing your query patterns or table design — useful for read-heavy, repeat-key access patterns.
