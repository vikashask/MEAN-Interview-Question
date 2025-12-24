# Routing

## Basic Routing

```javascript
// Simple routes
app.get("/", (req, res) => {
  res.send("Home");
});

app.post("/users", (req, res) => {
  res.json({ message: "User created" });
});

app.put("/users/:id", (req, res) => {
  res.json({ message: "User updated" });
});

app.delete("/users/:id", (req, res) => {
  res.status(204).send();
});

// All HTTP methods
app.all("/route", (req, res) => {
  res.json({ method: req.method });
});
```

## Route Parameters

```javascript
// Single parameter
app.get("/users/:id", (req, res) => {
  const id = req.params.id;
  res.json({ userId: id });
});

// Multiple parameters
app.get("/users/:userId/posts/:postId", (req, res) => {
  const { userId, postId } = req.params;
  res.json({ userId, postId });
});

// Optional parameters
app.get("/files/:name?", (req, res) => {
  const name = req.params.name || "default.txt";
  res.json({ file: name });
});

// Regex patterns
app.get(/^\/users\/(\d+)$/, (req, res) => {
  const id = req.params[0];
  res.json({ userId: id });
});

// Named regex groups
app.get(/^\/(?<type>\w+)\/(?<id>\d+)$/, (req, res) => {
  const { type, id } = req.params;
  res.json({ type, id });
});
```

## Query Parameters

```javascript
// Access query parameters
app.get("/search", (req, res) => {
  const { q, limit, offset } = req.query;
  res.json({ query: q, limit, offset });
});

// URL: /search?q=node&limit=10&offset=0

// Parse complex queries
app.get("/filter", (req, res) => {
  // /filter?tags=javascript&tags=nodejs
  const tags = req.query.tags; // Array if multiple
  res.json({ tags });
});

// Nested query objects
app.get("/api", (req, res) => {
  // /api?filter[name]=john&filter[age]=30
  const filter = req.query.filter; // { name: 'john', age: '30' }
  res.json({ filter });
});
```

## Router Objects

```javascript
const express = require("express");
const router = express.Router();

// Define routes on router
router.get("/", (req, res) => {
  res.json({ message: "Users list" });
});

router.get("/:id", (req, res) => {
  res.json({ userId: req.params.id });
});

router.post("/", (req, res) => {
  res.status(201).json({ message: "User created" });
});

router.put("/:id", (req, res) => {
  res.json({ message: "User updated" });
});

router.delete("/:id", (req, res) => {
  res.status(204).send();
});

// Mount router on app
app.use("/users", router);

// Routes become:
// GET /users
// GET /users/:id
// POST /users
// PUT /users/:id
// DELETE /users/:id
```

## Nested Routers

```javascript
// users/router.js
const router = express.Router();

router.get("/", (req, res) => {
  res.json({ message: "Users list" });
});

router.get("/:userId", (req, res) => {
  res.json({ userId: req.params.userId });
});

// posts/router.js
const postsRouter = express.Router({ mergeParams: true });

postsRouter.get("/", (req, res) => {
  const userId = req.params.userId;
  res.json({ userId, message: "Posts list" });
});

postsRouter.get("/:postId", (req, res) => {
  const { userId, postId } = req.params;
  res.json({ userId, postId });
});

// Mount nested router
router.use("/:userId/posts", postsRouter);

// app.js
app.use("/users", router);

// Routes:
// GET /users
// GET /users/:userId
// GET /users/:userId/posts
// GET /users/:userId/posts/:postId
```

## Route Grouping

```javascript
// Group related routes
const apiRouter = express.Router();

// Public routes
apiRouter.get("/public", (req, res) => {
  res.json({ message: "Public" });
});

// Protected routes
apiRouter.use(authenticate);

apiRouter.get("/protected", (req, res) => {
  res.json({ message: "Protected" });
});

apiRouter.post("/data", (req, res) => {
  res.json({ message: "Data created" });
});

// Admin routes
apiRouter.use(requireAdmin);

apiRouter.delete("/users/:id", (req, res) => {
  res.json({ message: "User deleted" });
});

app.use("/api", apiRouter);
```

## Route Handlers

```javascript
// Single handler
app.get("/route1", (req, res) => {
  res.send("Response");
});

// Multiple handlers (middleware chain)
app.get(
  "/route2",
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

// Array of handlers
const handlers = [
  (req, res, next) => {
    console.log("1");
    next();
  },
  (req, res, next) => {
    console.log("2");
    next();
  },
  (req, res) => {
    res.send("Done");
  },
];

app.get("/route3", handlers);

// Conditional routing
app.get("/conditional", (req, res, next) => {
  if (req.query.skip) {
    return next("route"); // Skip to next route
  }
  res.send("Processed");
});

app.get("/conditional", (req, res) => {
  res.send("Skipped");
});
```

## Route Patterns

```javascript
// Exact match
app.get("/users", (req, res) => {});

// Wildcard
app.get("/users/*", (req, res) => {});

// Multiple segments
app.get("/api/v1/users/:id", (req, res) => {});

// Optional segments
app.get("/files/:name?", (req, res) => {});

// Regex
app.get(/^\/users\/(\d+)$/, (req, res) => {});

// Case-insensitive
app.get(/\/users/i, (req, res) => {});
```

## RESTful API Pattern

```javascript
const router = express.Router();

// List all
router.get("/", (req, res) => {
  res.json({ items: [] });
});

// Get one
router.get("/:id", (req, res) => {
  res.json({ id: req.params.id });
});

// Create
router.post("/", (req, res) => {
  res.status(201).json({ message: "Created" });
});

// Update
router.put("/:id", (req, res) => {
  res.json({ message: "Updated" });
});

// Partial update
router.patch("/:id", (req, res) => {
  res.json({ message: "Patched" });
});

// Delete
router.delete("/:id", (req, res) => {
  res.status(204).send();
});

app.use("/api/items", router);
```
