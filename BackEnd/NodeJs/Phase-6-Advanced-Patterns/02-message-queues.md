# Message Queues

## RabbitMQ

```javascript
const amqp = require("amqplib");

// Connect
const connection = await amqp.connect("amqp://localhost");
const channel = await connection.createChannel();

// Declare queue
await channel.assertQueue("tasks", { durable: true });

// Producer - send message
const sendTask = async (task) => {
  const message = JSON.stringify(task);
  channel.sendToQueue("tasks", Buffer.from(message), { persistent: true });
};

// Consumer - receive message
const consumeTask = async () => {
  await channel.consume("tasks", async (msg) => {
    const task = JSON.parse(msg.content.toString());
    console.log("Processing task:", task);

    try {
      await processTask(task);
      channel.ack(msg); // Acknowledge
    } catch (err) {
      console.error("Error processing task:", err);
      channel.nack(msg, false, true); // Requeue
    }
  });
};

// Usage
app.post("/tasks", async (req, res) => {
  await sendTask(req.body);
  res.json({ message: "Task queued" });
});
```

## Redis Queues

```javascript
const redis = require("redis");

const client = redis.createClient();
await client.connect();

// Producer
const enqueueJob = async (queue, job) => {
  await client.lPush(queue, JSON.stringify(job));
};

// Consumer
const processQueue = async (queue) => {
  while (true) {
    const job = await client.brPop(queue, 0); // Blocking pop
    if (job) {
      const jobData = JSON.parse(job[1]);
      try {
        await processJob(jobData);
      } catch (err) {
        console.error("Job failed:", err);
        // Retry or move to dead letter queue
        await client.lPush(`${queue}:failed`, JSON.stringify(jobData));
      }
    }
  }
};

// Usage
app.post("/jobs", async (req, res) => {
  await enqueueJob("jobs", req.body);
  res.json({ message: "Job queued" });
});

// Start consumer
processQueue("jobs");
```

## Bull (Redis-based job queue)

```javascript
const Queue = require("bull");

// Create queue
const emailQueue = new Queue("emails", {
  redis: { host: "localhost", port: 6379 },
});

// Producer
app.post("/send-email", async (req, res) => {
  const job = await emailQueue.add(
    { to: req.body.email, subject: "Welcome" },
    { delay: 5000, attempts: 3, backoff: { type: "exponential", delay: 2000 } }
  );
  res.json({ jobId: job.id });
});

// Consumer
emailQueue.process(async (job) => {
  console.log("Processing email job:", job.data);
  await sendEmail(job.data);
  return { success: true };
});

// Event handlers
emailQueue.on("completed", (job) => {
  console.log(`Job ${job.id} completed`);
});

emailQueue.on("failed", (job, err) => {
  console.log(`Job ${job.id} failed:`, err.message);
});

// Monitor queue
app.get("/queue/stats", async (req, res) => {
  const counts = await emailQueue.getJobCounts();
  res.json(counts);
});
```

## Pub/Sub Pattern

```javascript
const redis = require("redis");

const publisher = redis.createClient();
const subscriber = redis.createClient();

await publisher.connect();
await subscriber.connect();

// Subscribe to channel
await subscriber.subscribe("notifications", (message) => {
  console.log("Received:", message);
});

// Publish message
await publisher.publish("notifications", "Hello subscribers!");

// Multiple channels
await subscriber.subscribe(["channel1", "channel2", "channel3"]);

// Pattern subscription
await subscriber.pSubscribe("user:*", (message) => {
  console.log("User event:", message);
});

// Publish to pattern
await publisher.publish("user:123:login", "User logged in");
```

## Event-Driven Architecture

```javascript
const EventEmitter = require("events");

class EventBus extends EventEmitter {
  async emit(event, data) {
    // Emit locally
    super.emit(event, data);

    // Publish to Redis for distributed systems
    await redis.publish(event, JSON.stringify(data));
  }

  async subscribe(event, handler) {
    this.on(event, handler);

    // Subscribe to Redis
    const subscriber = redis.duplicate();
    await subscriber.subscribe(event, (message) => {
      handler(JSON.parse(message));
    });
  }
}

const eventBus = new EventBus();

// Emit event
await eventBus.emit("user:created", { id: 1, name: "John" });

// Subscribe to event
await eventBus.subscribe("user:created", async (user) => {
  console.log("New user:", user);
  await sendWelcomeEmail(user);
});

// Usage in Express
app.post("/users", async (req, res) => {
  const user = await User.create(req.body);
  await eventBus.emit("user:created", user);
  res.status(201).json(user);
});
```

## Dead Letter Queue

```javascript
// Handle failed jobs
emailQueue.on("failed", async (job, err) => {
  console.log(`Job ${job.id} failed:`, err.message);

  // Move to DLQ
  const dlq = new Queue("emails:dlq");
  await dlq.add(job.data, {
    failedReason: err.message,
    originalJobId: job.id,
  });
});

// Process DLQ manually
const dlq = new Queue("emails:dlq");

dlq.process(async (job) => {
  console.log("Processing DLQ job:", job.data);
  // Manual retry or logging
  await logFailedJob(job.data);
});

// Retry failed jobs
app.post("/queue/retry/:jobId", async (req, res) => {
  const job = await emailQueue.getJob(req.params.jobId);
  if (job) {
    await job.retry();
    res.json({ message: "Job retried" });
  } else {
    res.status(404).json({ error: "Job not found" });
  }
});
```
