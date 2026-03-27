# SQS, SNS & EventBridge

## SQS (Simple Queue Service)

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
