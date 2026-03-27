# CloudWatch Monitoring & Logging

## CloudWatch Metrics

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
