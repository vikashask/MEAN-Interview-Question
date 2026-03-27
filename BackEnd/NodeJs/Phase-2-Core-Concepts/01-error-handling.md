# Error Handling

## try/catch with async/await

```javascript
// Basic error handling
const fetchData = async () => {
  try {
    const data = await fs.promises.readFile("file.txt", "utf8");
    return data;
  } catch (err) {
    console.error("Error reading file:", err.message);
    throw err; // Re-throw if needed
  }
};

// Multiple operations
const processData = async () => {
  try {
    const file1 = await fs.promises.readFile("file1.txt", "utf8");
    const file2 = await fs.promises.readFile("file2.txt", "utf8");
    return file1 + file2;
  } catch (err) {
    if (err.code === "ENOENT") {
      console.error("File not found");
    } else {
      console.error("Unknown error:", err);
    }
  } finally {
    console.log("Cleanup");
  }
};

// Error object properties
try {
  throw new Error("Something went wrong");
} catch (err) {
  console.log(err.message); // Error message
  console.log(err.stack); // Stack trace
  console.log(err.name); // Error type
  console.log(err.code); // Error code (for system errors)
}
```

## Custom Error Classes

```javascript
// Base custom error
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Specific errors
class ValidationError extends AppError {
  constructor(message) {
    super(message, 400);
    this.name = "ValidationError";
  }
}

class NotFoundError extends AppError {
  constructor(message) {
    super(message, 404);
    this.name = "NotFoundError";
  }
}

class AuthenticationError extends AppError {
  constructor(message) {
    super(message, 401);
    this.name = "AuthenticationError";
  }
}

// Usage
const validateUser = (user) => {
  if (!user.email) {
    throw new ValidationError("Email is required");
  }
};

try {
  validateUser({});
} catch (err) {
  if (err instanceof ValidationError) {
    console.log(`Validation failed: ${err.message}`);
  }
}
```

## Promise Error Handling

```javascript
// Promise chain
readFile("file.txt")
  .then((data) => processData(data))
  .then((result) => saveResult(result))
  .catch((err) => {
    console.error("Error:", err.message);
  })
  .finally(() => {
    console.log("Done");
  });

// Multiple catch handlers
readFile("file.txt")
  .catch((err) => {
    if (err.code === "ENOENT") {
      return "default content";
    }
    throw err;
  })
  .catch((err) => {
    console.error("Fatal error:", err);
  });

// Promise.allSettled (handles all, including errors)
const results = await Promise.allSettled([
  readFile("file1.txt"),
  readFile("file2.txt"),
  readFile("file3.txt"),
]);

results.forEach((result, index) => {
  if (result.status === "fulfilled") {
    console.log(`File ${index}: ${result.value}`);
  } else {
    console.error(`File ${index} error: ${result.reason}`);
  }
});
```

## Uncaught Exception Handling

```javascript
// Global uncaught exception handler
process.on("uncaughtException", (err) => {
  console.error("Uncaught Exception:", err);
  // Log to external service
  logError(err);
  // Exit process
  process.exit(1);
});

// Unhandled promise rejection
process.on("unhandledRejection", (reason, promise) => {
  console.error("Unhandled Rejection:", reason);
  logError(reason);
  process.exit(1);
});

// Warning for deprecated features
process.on("warning", (warning) => {
  console.warn(warning.name);
  console.warn(warning.message);
  console.warn(warning.stack);
});
```

## Error Handling Patterns

```javascript
// Wrapper for safe async operations
const asyncHandler = (fn) => {
  return async (...args) => {
    try {
      return await fn(...args);
    } catch (err) {
      console.error(err);
      throw err;
    }
  };
};

const safeReadFile = asyncHandler(async (path) => {
  return await fs.promises.readFile(path, "utf8");
});

// Go-style error handling
const tryCatch = async (promise) => {
  try {
    const data = await promise;
    return [data, null];
  } catch (err) {
    return [null, err];
  }
};

const [data, err] = await tryCatch(readFile("file.txt"));
if (err) {
  console.error("Error:", err);
} else {
  console.log("Data:", data);
}

// Retry logic
const retry = async (fn, maxAttempts = 3, delay = 1000) => {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      return await fn();
    } catch (err) {
      if (i === maxAttempts - 1) throw err;
      console.log(`Attempt ${i + 1} failed, retrying...`);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
};

const data = await retry(() => fetchFromAPI());
```

## Validation & Assertions

```javascript
// Manual validation
const validateEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!regex.test(email)) {
    throw new ValidationError("Invalid email format");
  }
};

// Using joi for schema validation
const schema = joi.object({
  email: joi.string().email().required(),
  age: joi.number().min(18).required(),
  name: joi.string().required(),
});

const { error, value } = schema.validate(user);
if (error) {
  throw new ValidationError(error.details[0].message);
}

// Assertions
const assert = (condition, message) => {
  if (!condition) {
    throw new Error(message);
  }
};

assert(user.id, "User ID is required");
```

## Error Logging

```javascript
// Simple logger
const logError = (err, context = {}) => {
  console.error({
    timestamp: new Date().toISOString(),
    message: err.message,
    stack: err.stack,
    context,
  });
};

// With Winston
const winston = require("winston");

const logger = winston.createLogger({
  level: "error",
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: "error.log" }),
    new winston.transports.Console(),
  ],
});

logger.error("Something went wrong", { userId: 123 });

// With Sentry (production)
const Sentry = require("@sentry/node");

Sentry.init({ dsn: process.env.SENTRY_DSN });

try {
  riskyOperation();
} catch (err) {
  Sentry.captureException(err);
}
```
