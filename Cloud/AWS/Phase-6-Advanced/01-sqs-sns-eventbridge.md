# SQS, SNS & EventBridge

> **In plain English:** These three services let different parts of your app talk to each other *without* calling each other directly — this is "decoupling," and it's the backbone of event-driven architecture. SQS = a queue (one message, one consumer). SNS = a broadcast (one message, many subscribers). EventBridge = a smart router that filters and routes events based on their content.

## Real-world analogy

- **SQS (queue)** = a single ticket line at a counter — each ticket (message) is served by exactly one worker (consumer), and the ticket disappears once handled. If no worker is free, tickets just wait in line.
- **SNS (pub/sub)** = a radio broadcast — one announcement goes out, and every subscribed radio (email, SQS queue, Lambda, phone) hears it simultaneously.
- **Fan-out (SNS + SQS)** = one radio broadcast being recorded onto multiple separate tape decks (queues) at once, so each department can process it at their own pace without missing anything.
- **EventBridge** = a mailroom clerk who reads the *content* of each envelope and routes it to the correct department based on rules — much smarter than a name-only broadcast.
- **Dead Letter Queue (DLQ)** = the "return to sender" bin — messages that failed processing too many times get set aside here instead of being retried forever or silently lost.
- **FIFO queue** = a strict single-file line — no cutting, first come first served, exactly once.

## Core concepts (memorize these first)

| Term | What it means |
|---|---|
| **SQS Standard Queue** | At-least-once delivery, best-effort ordering, nearly unlimited throughput. |
| **SQS FIFO Queue** | Strict ordering + exactly-once processing, but lower throughput; messages with the same `MessageGroupId` are processed in order. |
| **Visibility Timeout** | Once a consumer picks up a message, it's hidden from others for this duration — if the consumer doesn't delete it in time (crash/slow), it reappears for someone else to retry. |
| **Long Polling** | Consumer waits up to N seconds for a message to arrive instead of instantly returning empty — cheaper and lower-latency than constantly re-polling ("short polling"). |
| **Dead Letter Queue (DLQ)** | Where messages go after failing processing too many times (`maxReceiveCount`) — prevents infinite retry loops and poison messages from blocking the queue. |
| **SNS Topic** | A named channel that broadcasts one message to every subscriber (email, SMS, Lambda, SQS, HTTP). |
| **Fan-out pattern** | SNS topic with multiple SQS queues subscribed — one publish reaches many independent consumers, each processing at its own pace. |
| **EventBridge Event Bus** | A router that matches incoming events against rules (event patterns) and sends matches to one or more targets. |
| **Event Pattern** | The filter rule EventBridge uses to decide which events go where (can match on source, detail-type, and even values inside the event body). |
| **EventBridge Scheduler** | Cron-like or one-time scheduled triggering of targets (e.g. Lambda) — the modern replacement for CloudWatch Events "scheduled rules." |

**The #1 interview trap:** SQS vs SNS. SQS = pull-based, one consumer processes and removes each message (queue). SNS = push-based, broadcasts to *all* subscribers at once (topic). They're often combined: SNS fans out to multiple SQS queues so each downstream service gets its own durable copy.

**SNS/SQS vs EventBridge:** SNS/SQS route by *destination* (who's subscribed). EventBridge routes by *content* (rules based on what's inside the event) — much more powerful filtering, and it's the standard choice for building event-driven microservices today.

## Memory hooks

- **"SQS = queue, one winner takes the message. SNS = topic, everyone subscribed gets a copy."**
- **Fan-out = SNS shouts once, many SQS queues each get their own durable copy.**
- Visibility timeout too short = message gets processed twice (duplicate work). Too long = failed messages take forever to retry. Tune it close to your actual processing time.
- EventBridge = "route by what's inside the message." SNS = "route by who signed up."

---

## SQS (Simple Queue Service)

FIFO queues need a `.fifo` suffix in the name and typically enable content-based deduplication to avoid processing the same message twice.

```bash
# Create queue
aws sqs create-queue --queue-name my-queue

# Create FIFO queue
aws sqs create-queue \
  --queue-name my-queue.fifo \
  --attributes FifoQueue=true,ContentBasedDeduplication=true

# Get queue URL
aws sqs get-queue-url --queue-name my-queue

# Send message
aws sqs send-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue \
  --message-body "Hello World"

# Receive messages
aws sqs receive-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue \
  --max-number-of-messages 10

# Delete message
aws sqs delete-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue \
  --receipt-handle "receipt-handle-value"
```

## SQS with SDK

The core worker loop pattern: receive → process → delete. If processing throws, you *don't* delete the message, so it becomes visible again after the visibility timeout and gets retried.

```javascript
import {
  SQSClient,
  SendMessageCommand,
  ReceiveMessageCommand,
  DeleteMessageCommand,
} from "@aws-sdk/client-sqs";

const sqs = new SQSClient({ region: "us-east-1" });
const queueUrl = "https://sqs.us-east-1.amazonaws.com/123456789012/my-queue";

// Send message
const sendMessage = async (message) => {
  const command = new SendMessageCommand({
    QueueUrl: queueUrl,
    MessageBody: JSON.stringify(message),
    MessageAttributes: {
      Type: {
        DataType: "String",
        StringValue: "Order",
      },
      Priority: {
        DataType: "Number",
        StringValue: "1",
      },
    },
  });

  const response = await sqs.send(command);
  return response.MessageId;
};

// Send batch messages
const sendBatchMessages = async (messages) => {
  const entries = messages.map((msg, index) => ({
    Id: index.toString(),
    MessageBody: JSON.stringify(msg),
  }));

  const command = new SendMessageBatchCommand({
    QueueUrl: queueUrl,
    Entries: entries,
  });

  await sqs.send(command);
};

// Receive messages
const receiveMessages = async () => {
  const command = new ReceiveMessageCommand({
    QueueUrl: queueUrl,
    MaxNumberOfMessages: 10,
    WaitTimeSeconds: 20, // Long polling
    MessageAttributeNames: ["All"],
  });

  const response = await sqs.send(command);
  return response.Messages || [];
};

// Delete message
const deleteMessage = async (receiptHandle) => {
  const command = new DeleteMessageCommand({
    QueueUrl: queueUrl,
    ReceiptHandle: receiptHandle,
  });

  await sqs.send(command);
};

// Process messages
const processMessages = async () => {
  while (true) {
    const messages = await receiveMessages();

    for (const message of messages) {
      try {
        const body = JSON.parse(message.Body);
        console.log("Processing:", body);

        // Process message
        await handleMessage(body);

        // Delete after successful processing
        await deleteMessage(message.ReceiptHandle);
      } catch (error) {
        console.error("Error processing message:", error);
        // Message will return to queue after visibility timeout
      }
    }
  }
};
```

## SQS FIFO Queue

Messages sharing the same `MessageGroupId` are guaranteed to be processed in the order they were sent — different group IDs can be processed in parallel.

```javascript
// Send to FIFO queue
const sendFifoMessage = async (message, groupId) => {
  const command = new SendMessageCommand({
    QueueUrl: fifoQueueUrl,
    MessageBody: JSON.stringify(message),
    MessageGroupId: groupId,
    MessageDeduplicationId: message.id, // Or use ContentBasedDeduplication
  });

  await sqs.send(command);
};

// Usage - messages with same GroupId are processed in order
await sendFifoMessage({ id: "1", action: "create" }, "user-123");
await sendFifoMessage({ id: "2", action: "update" }, "user-123");
await sendFifoMessage({ id: "3", action: "delete" }, "user-123");
```

## Dead Letter Queue

After `maxReceiveCount` failed attempts, a message is automatically moved to the DLQ instead of retrying forever — lets you inspect/debug "poison" messages without them blocking the whole queue.

```bash
# Create DLQ
aws sqs create-queue --queue-name my-dlq

# Configure main queue with DLQ
aws sqs set-queue-attributes \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue \
  --attributes '{
    "RedrivePolicy": "{\"deadLetterTargetArn\":\"arn:aws:sqs:us-east-1:123456789012:my-dlq\",\"maxReceiveCount\":\"3\"}"
  }'
```

## SNS (Simple Notification Service)

A topic is the broadcast channel; anything subscribed (email, SMS, SQS, Lambda, HTTP endpoint) receives every message published to it.

```bash
# Create topic
aws sns create-topic --name my-topic

# Subscribe email
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789012:my-topic \
  --protocol email \
  --notification-endpoint user@example.com

# Subscribe SQS
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789012:my-topic \
  --protocol sqs \
  --notification-endpoint arn:aws:sqs:us-east-1:123456789012:my-queue

# Publish message
aws sns publish \
  --topic-arn arn:aws:sns:us-east-1:123456789012:my-topic \
  --message "Hello World"
```

## SNS with SDK

```javascript
import {
  SNSClient,
  PublishCommand,
  SubscribeCommand,
} from "@aws-sdk/client-sns";

const sns = new SNSClient({ region: "us-east-1" });
const topicArn = "arn:aws:sns:us-east-1:123456789012:my-topic";

// Publish message
const publishMessage = async (message, subject) => {
  const command = new PublishCommand({
    TopicArn: topicArn,
    Message: JSON.stringify(message),
    Subject: subject,
    MessageAttributes: {
      type: {
        DataType: "String",
        StringValue: "notification",
      },
    },
  });

  const response = await sns.send(command);
  return response.MessageId;
};

// Subscribe Lambda
const subscribeLambda = async (lambdaArn) => {
  const command = new SubscribeCommand({
    TopicArn: topicArn,
    Protocol: "lambda",
    Endpoint: lambdaArn,
  });

  await sns.send(command);
};

// Publish to specific subscriber
const publishToPhone = async (phoneNumber, message) => {
  const command = new PublishCommand({
    PhoneNumber: phoneNumber,
    Message: message,
  });

  await sns.send(command);
};
```

## Fan-Out Pattern (SNS + SQS)

The classic combo: publish once to SNS, and every subscribed SQS queue gets its own independent, durable copy — each downstream service (processing, analytics, notifications) can consume at its own pace without stepping on each other.

```javascript
// SNS publishes to multiple SQS queues
const setupFanOut = async () => {
  // Create topic
  const topic = await sns.send(new CreateTopicCommand({ Name: "orders" }));

  // Create multiple queues
  const queues = ["order-processing", "order-analytics", "order-notifications"];

  for (const queueName of queues) {
    // Create queue
    const queue = await sqs.send(
      new CreateQueueCommand({ QueueName: queueName })
    );

    // Subscribe queue to topic
    await sns.send(
      new SubscribeCommand({
        TopicArn: topic.TopicArn,
        Protocol: "sqs",
        Endpoint: queue.QueueUrl,
      })
    );
  }
};

// Publish once, all queues receive
await publishMessage({ orderId: 123, total: 99.99 }, "New Order");
```

## EventBridge

Unlike SNS (which broadcasts to whoever subscribed), EventBridge routes based on the *content* of the event — the rule's `event-pattern` decides which events go to which targets.

```bash
# Create event bus
aws events create-event-bus --name my-event-bus

# Put rule
aws events put-rule \
  --name OrderCreatedRule \
  --event-pattern '{
    "source": ["myapp"],
    "detail-type": ["Order Created"]
  }' \
  --state ENABLED

# Add target (Lambda)
aws events put-targets \
  --rule OrderCreatedRule \
  --targets Id=1,Arn=arn:aws:lambda:us-east-1:123456789012:function:ProcessOrder

# Put event
aws events put-events \
  --entries '[{
    "Source": "myapp",
    "DetailType": "Order Created",
    "Detail": "{\"orderId\":123,\"total\":99.99}"
  }]'
```

## EventBridge with SDK

Rules can filter on values *inside* the event body, not just its type — here, only orders over $1000 trigger the `NotifyManager` Lambda.

```javascript
import {
  EventBridgeClient,
  PutEventsCommand,
  PutRuleCommand,
  PutTargetsCommand,
} from "@aws-sdk/client-eventbridge";

const eventBridge = new EventBridgeClient({ region: "us-east-1" });

// Publish event
const publishEvent = async (eventData) => {
  const command = new PutEventsCommand({
    Entries: [
      {
        Source: "myapp",
        DetailType: "Order Created",
        Detail: JSON.stringify(eventData),
        EventBusName: "my-event-bus",
      },
    ],
  });

  const response = await eventBridge.send(command);
  return response.FailedEntryCount === 0;
};

// Create rule
const createRule = async () => {
  const ruleCommand = new PutRuleCommand({
    Name: "HighValueOrders",
    EventPattern: JSON.stringify({
      source: ["myapp"],
      "detail-type": ["Order Created"],
      detail: {
        total: [{ numeric: [">", 1000] }],
      },
    }),
    State: "ENABLED",
    EventBusName: "my-event-bus",
  });

  await eventBridge.send(ruleCommand);

  // Add Lambda target
  const targetCommand = new PutTargetsCommand({
    Rule: "HighValueOrders",
    EventBusName: "my-event-bus",
    Targets: [
      {
        Id: "1",
        Arn: "arn:aws:lambda:us-east-1:123456789012:function:NotifyManager",
      },
    ],
  });

  await eventBridge.send(targetCommand);
};

// Usage
await publishEvent({
  orderId: 123,
  customerId: 456,
  total: 1500.0,
  items: [{ id: 1, quantity: 2 }],
});
```

## EventBridge Scheduler

The modern way to run something on a schedule (cron-like) or at a specific one-time future moment — replaces the older "CloudWatch Events scheduled rule" pattern.

```javascript
import {
  SchedulerClient,
  CreateScheduleCommand,
} from "@aws-sdk/client-scheduler";

const scheduler = new SchedulerClient({ region: "us-east-1" });

// Create recurring schedule
const createSchedule = async () => {
  const command = new CreateScheduleCommand({
    Name: "DailyReport",
    ScheduleExpression: "rate(1 day)",
    Target: {
      Arn: "arn:aws:lambda:us-east-1:123456789012:function:GenerateReport",
      RoleArn: "arn:aws:iam::123456789012:role/EventBridgeSchedulerRole",
    },
    FlexibleTimeWindow: {
      Mode: "OFF",
    },
  });

  await scheduler.send(command);
};

// One-time schedule
const scheduleOneTime = async (dateTime) => {
  const command = new CreateScheduleCommand({
    Name: "SendReminder",
    ScheduleExpression: `at(${dateTime})`,
    Target: {
      Arn: "arn:aws:lambda:us-east-1:123456789012:function:SendEmail",
      RoleArn: "arn:aws:iam::123456789012:role/EventBridgeSchedulerRole",
      Input: JSON.stringify({ userId: 123, type: "reminder" }),
    },
    FlexibleTimeWindow: {
      Mode: "OFF",
    },
  });

  await scheduler.send(command);
};
```

## Event-Driven Architecture Pattern

The payoff of all this: the order service doesn't need to know or care who reacts to a new order — inventory, notifications, and analytics services each independently subscribe and react on their own.

```javascript
// Order service publishes event
const createOrder = async (orderData) => {
  // Save to database
  const order = await Order.create(orderData);

  // Publish event
  await publishEvent({
    orderId: order.id,
    customerId: order.customerId,
    total: order.total,
    status: "created",
  });

  return order;
};

// Multiple services react to event
// 1. Inventory service (Lambda)
export const handler = async (event) => {
  const order = JSON.parse(event.detail);
  await reserveInventory(order.items);
};

// 2. Notification service (Lambda)
export const handler = async (event) => {
  const order = JSON.parse(event.detail);
  await sendOrderConfirmation(order.customerId, order.id);
};

// 3. Analytics service (Lambda)
export const handler = async (event) => {
  const order = JSON.parse(event.detail);
  await trackOrderMetrics(order);
};
```

---

## Quick interview answers

**Q: SQS vs SNS — the core difference?**
SQS is pull-based, a durable queue — one consumer processes and removes each message. SNS is push-based, a broadcast — every subscriber gets a copy of every message immediately, with no built-in durability for a slow/offline subscriber.

**Q: What is the fan-out pattern and why use it?**
Publishing once to an SNS topic that has multiple SQS queues subscribed — each downstream service gets its own durable queue to process independently, at its own pace, without missing messages.

**Q: What happens if a consumer fails to process an SQS message?**
It doesn't delete the message, so once the visibility timeout expires, the message becomes visible again for another consumer to retry — after `maxReceiveCount` failed attempts, it's moved to the Dead Letter Queue.

**Q: SNS/SQS vs EventBridge — when would you pick EventBridge?**
When routing needs to be based on the *content* of the event, not just "who subscribed." EventBridge's event patterns can filter on fields inside the event body, making it the better fit for complex event-driven microservice architectures.

**Q: FIFO vs Standard SQS queue?**
FIFO guarantees strict order and exactly-once processing (within a MessageGroupId) but has lower throughput limits. Standard offers nearly unlimited throughput with at-least-once delivery and best-effort ordering (duplicates and out-of-order delivery are possible).

**Q: Why use long polling instead of short polling?**
Long polling waits up to N seconds for a message before returning empty, reducing the number of empty API calls (cheaper) and reducing latency compared to constantly re-polling on a tight loop.
