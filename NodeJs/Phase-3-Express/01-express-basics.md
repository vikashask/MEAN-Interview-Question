# Express Basics

## Setup & Server

```javascript
const express = require("express");
const app = express();

// Create server
const server = app.listen(3000, () => {
  console.log("Server running on port 3000");
});

// Or use http module
const http = require("http");
const server = http.createServer(app);
server.listen(3000);

// Graceful shutdown
process.on("SIGTERM", () => {
  server.close(() => {
    console.log("Server closed");
    process.exit(0);
  });
});
```

## Basic Routing

```javascript
// GET request
app.get("/", (req, res) => {
  res.send("Hello World");
});

// POST request
app.post("/users", (req, res) => {
  res.json({ message: "User created" });
});

// PUT request
app.put("/users/:id", (req, res) => {
  res.json({ message: "User updated" });
});

// DELETE request
app.delete("/users/:id", (req, res) => {
  res.status(204).send();
});

// PATCH request
app.patch("/users/:id", (req, res) => {
  res.json({ message: "User patched" });
});

// All methods
app.all("/api/*", (req, res) => {
  res.json({ method: req.method });
});
```

## Route Parameters & Queries

```javascript
// Route parameters
app.get("/users/:id", (req, res) => {
  const id = req.params.id;
  res.json({ userId: id });
});

// Multiple parameters
app.get("/users/:userId/posts/:postId", (req, res) => {
  const { userId, postId } = req.params;
  res.json({ userId, postId });
});

// Query parameters
app.get("/search", (req, res) => {
  const { q, limit, offset } = req.query;
  res.json({ query: q, limit, offset });
});

// Optional parameters
app.get("/files/:name?", (req, res) => {
  const name = req.params.name || "default";
  res.json({ file: name });
});

// Regex patterns
app.get(/^\/users\/(\d+)$/, (req, res) => {
  const id = req.params[0];
  res.json({ userId: id });
});
```

## Request & Response

```javascript
// Request properties
app.get("/info", (req, res) => {
  console.log(req.method); // GET, POST, etc.
  console.log(req.url); // /info?key=value
  console.log(req.path); // /info
  console.log(req.query); // { key: 'value' }
  console.log(req.params); // Route parameters
  console.log(req.headers); // Request headers
  console.log(req.body); // Request body (requires middleware)
  console.log(req.ip); // Client IP
  console.log(req.hostname); // Host name
});

// Response methods
app.get("/response-types", (req, res) => {
  // Send text
  res.send("Hello");

  // Send JSON
  res.json({ message: "Hello" });

  // Send file
  res.sendFile("/path/to/file.pdf");

  // Redirect
  res.redirect("/new-path");
  res.redirect(301, "/new-path");

  // Status code
  res.status(201).json({ id: 1 });

  // Headers
  res.set("X-Custom-Header", "value");
  res.type("application/json");

  // End response
  res.end();
});

// Response chaining
app.get("/chain", (req, res) => {
  res
    .status(200)
    .set("Content-Type", "application/json")
    .json({ message: "Success" });
});
```

## Middleware

```javascript
// Application-level middleware
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`);
  next(); // Pass to next middleware
});

// Conditional middleware
app.use("/api", (req, res, next) => {
  console.log("API request");
  next();
});

// Multiple middleware
app.get(
  "/route",
  (req, res, next) => {
    console.log("First");
    next();
  },
  (req, res, next) => {
    console.log("Second");
    next();
  },
  (req, res) => {
    res.send("Done");
  }
);

// Error handling middleware (must have 4 parameters)
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: err.message });
});

// Skip middleware
app.use((req, res, next) => {
  if (req.path === "/skip") {
    return next("route"); // Skip to next route
  }
  next();
});
```

## Built-in Middleware

```javascript
// Parse JSON
app.use(express.json());

// Parse URL-encoded form data
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use(express.static("public"));
app.use("/files", express.static("uploads"));

// Custom static middleware
app.use((req, res, next) => {
  if (req.path.startsWith("/static/")) {
    res.sendFile(req.path.replace("/static/", ""));
  } else {
    next();
  }
});
```

## Router Objects

```javascript
const router = express.Router();

// Define routes on router
router.get("/", (req, res) => {
  res.json({ message: "Users list" });
});

router.post("/", (req, res) => {
  res.status(201).json({ message: "User created" });
});

router.get("/:id", (req, res) => {
  res.json({ userId: req.params.id });
});

// Mount router
app.use("/users", router);

// Now routes are:
// GET /users
// POST /users
// GET /users/:id
```

## Error Handling

```javascript
// Catch 404
app.use((req, res) => {
  res.status(404).json({ error: "Not found" });
});

// Error middleware
app.use((err, req, res, next) => {
  const status = err.status || 500;
  const message = err.message || "Internal server error";

  res.status(status).json({
    error: {
      status,
      message,
    },
  });
});

// Async error handling
app.get("/async", async (req, res, next) => {
  try {
    const data = await fetchData();
    res.json(data);
  } catch (err) {
    next(err); // Pass to error middleware
  }
});

// Wrapper for async routes
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

app.get(
  "/route",
  asyncHandler(async (req, res) => {
    const data = await fetchData();
    res.json(data);
  })
);
```

## Common Patterns

```javascript
// Health check
app.get("/health", (req, res) => {
  res.json({ status: "ok", timestamp: Date.now() });
});

// API versioning
app.use("/api/v1", require("./routes/v1"));
app.use("/api/v2", require("./routes/v2"));

// Request logging
app.use((req, res, next) => {
  const start = Date.now();
  res.on("finish", () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} ${res.statusCode} ${duration}ms`);
  });
  next();
});

// CORS
const cors = require("cors");
app.use(cors());
app.use(cors({ origin: "https://example.com" }));

// Compression
const compression = require("compression");
app.use(compression());
```
