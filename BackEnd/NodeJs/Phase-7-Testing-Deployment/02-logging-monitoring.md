# Logging & Monitoring

## Winston Logger

```javascript
const winston = require("winston");

const logger = winston.createLogger({
  level: "info",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: "user-service" },
  transports: [
    new winston.transports.File({ filename: "error.log", level: "error" }),
    new winston.transports.File({ filename: "combined.log" }),
  ],
});

if (process.env.NODE_ENV !== "production") {
  logger.add(
    new winston.transports.Console({
      format: winston.format.simple(),
    })
  );
}

// Usage
logger.info("User created", { userId: 123 });
logger.error("Database error", { error: err.message });
logger.warn("High memory usage", { memory: process.memoryUsage() });
```

## Pino Logger

```javascript
const pino = require("pino");

const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  transport: {
    target: "pino-pretty",
    options: {
      colorize: true,
    },
  },
});

// Usage
logger.info({ userId: 123 }, "User created");
logger.error({ err }, "Database error");

// With Express
const pinoExpress = require("pino-http");
app.use(pinoExpress());

// Logs are available as req.log
app.get("/users", (req, res) => {
  req.log.info("Fetching users");
  res.json([]);
});
```

## Request Logging

```javascript
const morgan = require("morgan");

// Predefined formats
app.use(morgan("combined")); // Apache combined log format
app.use(morgan("dev")); // Development format

// Custom format
morgan.token("user-id", (req) => req.user?.id || "anonymous");

app.use(morgan(":user-id :method :url :status :response-time ms"));

// Custom logger
app.use((req, res, next) => {
  const start = Date.now();
  res.on("finish", () => {
    const duration = Date.now() - start;
    logger.info({
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration,
      userId: req.user?.id,
    });
  });
  next();
});
```

## Error Tracking with Sentry

```javascript
const Sentry = require("@sentry/node");

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
});

app.use(Sentry.Handlers.requestHandler());

// Catch errors
app.use((err, req, res, next) => {
  Sentry.captureException(err);
  res.status(500).json({ error: "Internal server error" });
});

app.use(Sentry.Handlers.errorHandler());

// Manual error capture
try {
  riskyOperation();
} catch (err) {
  Sentry.captureException(err);
}

// Set user context
Sentry.setUser({ id: user.id, email: user.email });
```

## Application Monitoring

```javascript
// Health check endpoint
app.get("/health", (req, res) => {
  const health = {
    status: "ok",
    timestamp: new Date(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    database: "connected", // Check actual DB connection
  };
  res.json(health);
});

// Metrics endpoint
const prometheus = require("prom-client");

const httpRequestDuration = new prometheus.Histogram({
  name: "http_request_duration_seconds",
  help: "Duration of HTTP requests in seconds",
  labelNames: ["method", "route", "status_code"],
});

app.use((req, res, next) => {
  const start = Date.now();
  res.on("finish", () => {
    const duration = (Date.now() - start) / 1000;
    httpRequestDuration
      .labels(req.method, req.route?.path || req.path, res.statusCode)
      .observe(duration);
  });
  next();
});

app.get("/metrics", async (req, res) => {
  res.set("Content-Type", prometheus.register.contentType);
  res.end(await prometheus.register.metrics());
});
```

## Performance Monitoring

```javascript
// Track slow queries
const trackQuery = async (query, fn) => {
  const start = Date.now();
  try {
    const result = await fn();
    const duration = Date.now() - start;
    if (duration > 1000) {
      logger.warn({ query, duration }, "Slow query");
    }
    return result;
  } catch (err) {
    logger.error({ query, error: err.message }, "Query failed");
    throw err;
  }
};

// Usage
const users = await trackQuery("SELECT * FROM users", () => {
  return User.find();
});

// Memory monitoring
setInterval(() => {
  const mem = process.memoryUsage();
  logger.info({
    heapUsed: Math.round(mem.heapUsed / 1024 / 1024) + "MB",
    heapTotal: Math.round(mem.heapTotal / 1024 / 1024) + "MB",
    external: Math.round(mem.external / 1024 / 1024) + "MB",
  });
}, 60000);
```

## Distributed Tracing

```javascript
const tracer = require("dd-trace").init();

// Trace database queries
const traced = tracer.trace("db.query", async (span) => {
  span.setTag("db.type", "mongodb");
  return await User.find();
});

// Trace HTTP requests
app.use((req, res, next) => {
  const span = tracer.startSpan("http.request", {
    tags: {
      "http.method": req.method,
      "http.url": req.url,
    },
  });

  res.on("finish", () => {
    span.setTag("http.status_code", res.statusCode);
    span.finish();
  });

  next();
});
```

## Alerting

```javascript
// Alert on high error rate
let errorCount = 0;
let totalRequests = 0;

app.use((req, res, next) => {
  totalRequests++;
  const originalJson = res.json;

  res.json = function (data) {
    if (res.statusCode >= 400) {
      errorCount++;
    }
    return originalJson.call(this, data);
  };

  next();
});

setInterval(() => {
  const errorRate = (errorCount / totalRequests) * 100;
  if (errorRate > 5) {
    logger.error({ errorRate }, "High error rate detected");
    // Send alert
    sendAlert(`Error rate: ${errorRate}%`);
  }
  errorCount = 0;
  totalRequests = 0;
}, 60000);
```
