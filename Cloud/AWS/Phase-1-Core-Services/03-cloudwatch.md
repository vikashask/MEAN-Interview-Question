# CloudWatch Monitoring & Logging

> **In plain English:** CloudWatch is AWS's built-in "dashboard + alarm system + log file cabinet" for everything running in your account. If you want to know "is my app healthy," "what happened at 3am," or "text me if CPU spikes" — that's CloudWatch.

## Real-world analogy

Think of CloudWatch as a car's dashboard plus a black-box recorder:

- **Metrics** = the speedometer, fuel gauge, temperature gauge — numbers over time (CPU%, request count, latency).
- **Alarms** = the warning light that turns on when a gauge crosses a redline ("CPU > 80% for 10 minutes → alert").
- **Logs** = the black-box recorder — a running diary of everything the engine (your app) said.
- **Dashboards** = the whole dashboard view, gauges and lights arranged together on one screen.
- **Log Insights** = a search engine over the black-box recordings ("find me every ERROR line from the last hour").

## Core concepts (memorize these first)

| Term | What it means |
|---|---|
| **Namespace** | A folder/category for metrics (e.g. `AWS/EC2`, or your own `MyApp`). |
| **Metric** | A single measurable number tracked over time (e.g. `CPUUtilization`). |
| **Dimension** | A tag that narrows a metric down (e.g. `InstanceId=i-123` — "CPU of *this* instance specifically"). |
| **Period** | How often a metric is aggregated/reported (e.g. every 300 seconds). |
| **Alarm** | A rule: "if metric crosses threshold for N periods, do X" (X = notify SNS, auto-scale, etc). |
| **Log Group** | A folder for logs, usually one per app/Lambda function (e.g. `/aws/lambda/MyFunction`). |
| **Log Stream** | A single sequence of log entries inside a group (e.g. one per running instance/invocation). |
| **Log Insights** | A query language (like SQL-lite) to search/aggregate log data. |
| **CloudWatch Agent** | A small program installed on EC2/on-prem servers to push OS-level metrics (memory, disk — not collected by default) and custom log files into CloudWatch. |

**Important gotcha to remember:** EC2 gives you CPU, network, and disk *I/O* for free — but **not** memory usage or disk *space* usage. You must install the CloudWatch Agent to get those.

## Memory hooks

- **"Metrics are numbers, Logs are sentences."**
- Alarm states: `OK` → `ALARM` → `INSUFFICIENT_DATA` (not enough data points yet to decide).
- **Log group = filing cabinet drawer. Log stream = one folder inside the drawer.**

---

## CloudWatch Metrics

Read built-in metrics AWS already tracks for you, or push your own custom ones.

```bash
# List metrics
aws cloudwatch list-metrics --namespace AWS/EC2

# Get metric statistics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T23:59:59Z \
  --period 3600 \
  --statistics Average,Maximum

# Put custom metric
aws cloudwatch put-metric-data \
  --namespace MyApp \
  --metric-name PageLoadTime \
  --value 150 \
  --unit Milliseconds
```

## Custom Metrics with SDK

Push your own application-level numbers (request counts, error rates) — anything not automatically tracked by AWS.

```javascript
import {
  CloudWatchClient,
  PutMetricDataCommand,
} from "@aws-sdk/client-cloudwatch";

const cloudwatch = new CloudWatchClient({ region: "us-east-1" });

// Send custom metric
const putMetric = async (metricName, value, unit = "None") => {
  const command = new PutMetricDataCommand({
    Namespace: "MyApp",
    MetricData: [
      {
        MetricName: metricName,
        Value: value,
        Unit: unit,
        Timestamp: new Date(),
        Dimensions: [
          { Name: "Environment", Value: "production" },
          { Name: "Service", Value: "api" },
        ],
      },
    ],
  });

  await cloudwatch.send(command);
};

// Usage
await putMetric("ApiRequests", 100, "Count");
await putMetric("ResponseTime", 250, "Milliseconds");
await putMetric("ErrorRate", 2.5, "Percent");
```

## CloudWatch Alarms

An alarm watches one metric and fires an action (usually notify SNS, but can also auto-scale) once a threshold is breached for a set number of periods in a row — this avoids false alarms from a single noisy spike.

```bash
# Create alarm
aws cloudwatch put-metric-alarm \
  --alarm-name high-cpu-alarm \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:MyTopic

# List alarms
aws cloudwatch describe-alarms

# Delete alarm
aws cloudwatch delete-alarms --alarm-names high-cpu-alarm
```

## CloudWatch Logs

Log group = a named container (usually per-app or per-Lambda function). Log stream = one thread of entries within that group.

```bash
# Create log group
aws logs create-log-group --log-group-name /aws/app/myapp

# Create log stream
aws logs create-log-stream \
  --log-group-name /aws/app/myapp \
  --log-stream-name stream-1

# Put log events
aws logs put-log-events \
  --log-group-name /aws/app/myapp \
  --log-stream-name stream-1 \
  --log-events timestamp=$(date +%s000),message="Application started"

# Tail logs
aws logs tail /aws/app/myapp --follow

# Filter logs
aws logs filter-log-events \
  --log-group-name /aws/app/myapp \
  --filter-pattern "ERROR" \
  --start-time $(date -d '1 hour ago' +%s000)
```

## CloudWatch Logs SDK

A small reusable logger class — note it has to track a `sequenceToken` between writes so log entries land in the right order.

```javascript
import {
  CloudWatchLogsClient,
  CreateLogGroupCommand,
  CreateLogStreamCommand,
  PutLogEventsCommand,
} from "@aws-sdk/client-cloudwatch-logs";

const logsClient = new CloudWatchLogsClient({ region: "us-east-1" });

class CloudWatchLogger {
  constructor(logGroupName, logStreamName) {
    this.logGroupName = logGroupName;
    this.logStreamName = logStreamName;
    this.sequenceToken = null;
  }

  async init() {
    try {
      await logsClient.send(
        new CreateLogGroupCommand({
          logGroupName: this.logGroupName,
        })
      );
    } catch (err) {
      if (err.name !== "ResourceAlreadyExistsException") throw err;
    }

    try {
      await logsClient.send(
        new CreateLogStreamCommand({
          logGroupName: this.logGroupName,
          logStreamName: this.logStreamName,
        })
      );
    } catch (err) {
      if (err.name !== "ResourceAlreadyExistsException") throw err;
    }
  }

  async log(message, level = "INFO") {
    const command = new PutLogEventsCommand({
      logGroupName: this.logGroupName,
      logStreamName: this.logStreamName,
      logEvents: [
        {
          message: JSON.stringify({
            timestamp: new Date().toISOString(),
            level,
            message,
          }),
          timestamp: Date.now(),
        },
      ],
      sequenceToken: this.sequenceToken,
    });

    const response = await logsClient.send(command);
    this.sequenceToken = response.nextSequenceToken;
  }

  async info(message) {
    await this.log(message, "INFO");
  }

  async error(message) {
    await this.log(message, "ERROR");
  }

  async warn(message) {
    await this.log(message, "WARN");
  }
}

// Usage
const logger = new CloudWatchLogger("/aws/app/myapp", "stream-1");
await logger.init();
await logger.info("Application started");
await logger.error("Database connection failed");
```

## Log Insights Queries

Think of Log Insights as SQL for your log files — filter, aggregate, sort text logs without downloading them.

```bash
# Run query
aws logs start-query \
  --log-group-name /aws/app/myapp \
  --start-time $(date -d '1 hour ago' +%s) \
  --end-time $(date +%s) \
  --query-string 'fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp desc | limit 20'

# Get query results
aws logs get-query-results --query-id <query-id>
```

```
// Common Log Insights queries

// Find errors
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 20

// Aggregate by status code
stats count() by statusCode
| sort count desc

// Average response time
stats avg(responseTime) by bin(5m)

// Find slow queries
fields @timestamp, query, duration
| filter duration > 1000
| sort duration desc
```

## Metric Filters

A metric filter watches incoming logs and converts a text pattern match into a numeric metric — e.g. every log line containing "ERROR" bumps an `Errors` counter, so you can alarm on it like any other metric.

```bash
# Create metric filter
aws logs put-metric-filter \
  --log-group-name /aws/app/myapp \
  --filter-name ErrorCount \
  --filter-pattern "[time, request_id, level = ERROR*, msg]" \
  --metric-transformations \
    metricName=Errors,metricNamespace=MyApp,metricValue=1
```

## CloudWatch Dashboards

A dashboard is just a saved JSON layout of widgets (metric graphs + log query panels) shown together on one screen.

```javascript
import {
  CloudWatchClient,
  PutDashboardCommand,
} from "@aws-sdk/client-cloudwatch";

const dashboard = {
  widgets: [
    {
      type: "metric",
      properties: {
        metrics: [["AWS/EC2", "CPUUtilization", { stat: "Average" }]],
        period: 300,
        stat: "Average",
        region: "us-east-1",
        title: "EC2 CPU Utilization",
      },
    },
    {
      type: "log",
      properties: {
        query:
          "SOURCE '/aws/app/myapp' | fields @timestamp, @message | filter @message like /ERROR/",
        region: "us-east-1",
        title: "Error Logs",
      },
    },
  ],
};

const command = new PutDashboardCommand({
  DashboardName: "MyAppDashboard",
  DashboardBody: JSON.stringify(dashboard),
});

await cloudwatch.send(command);
```

## CloudWatch Agent

The Agent is a separate install — required to collect things AWS doesn't track for free: memory usage, disk space usage, and any custom log files on the box.

```bash
# Install CloudWatch Agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i -E ./amazon-cloudwatch-agent.deb

# Configure agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard

# Start agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -s \
  -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json
```

```json
// CloudWatch Agent config
{
  "metrics": {
    "namespace": "MyApp",
    "metrics_collected": {
      "mem": {
        "measurement": [{ "name": "mem_used_percent", "rename": "MemoryUsage" }]
      },
      "disk": {
        "measurement": [{ "name": "used_percent", "rename": "DiskUsage" }],
        "resources": ["*"]
      }
    }
  },
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/app/*.log",
            "log_group_name": "/aws/app/myapp",
            "log_stream_name": "{instance_id}"
          }
        ]
      }
    }
  }
}
```

---

## Quick interview answers

**Q: Does EC2 report memory usage to CloudWatch by default?**
No. CPU, network, and disk I/O are free/automatic; memory and disk *space* require installing the CloudWatch Agent.

**Q: Metric vs Log — what's the difference and when do you use each?**
Metric = a number over time, cheap to query, great for alarms/graphs/trends. Log = free-text detail, great for "what exactly happened at this moment" debugging. Use metrics for "is something wrong," logs for "why."

**Q: Why does an alarm need `evaluation-periods` and not just fire on one bad data point?**
To avoid false positives from a single noisy spike — the metric must breach the threshold for N consecutive periods before the alarm actually fires.

**Q: What triggers when an alarm fires?**
Usually an SNS notification (email/Slack/PagerDuty), but it can also directly trigger Auto Scaling actions.

**Q: What is CloudWatch Logs Insights used for?**
Ad-hoc querying/aggregating of raw log text without exporting logs elsewhere — e.g., "count errors by status code in the last hour."
