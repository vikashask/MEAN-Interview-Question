# Middleware

## Middleware Concept

```javascript
// Middleware function signature
const myMiddleware = (req, res, next) => {
  // Do something
  next(); // Pass to next middleware
};

// Error handling middleware (4 parameters)
const errorMiddleware = (err, req, res, next) => {
  res.status(500).json({ error: err.message });
};

// Middleware execution order
app.use(middleware1);
app.use(middleware2);
app.get("/route", middleware3, (req, res) => {
  res.send("Response");
});

// Order: middleware1 → middleware2 → middleware3 → route handler
```

## Custom Middleware

```javascript
// Logging middleware
const logger = (req, res, next) => {
  console.log(`${new Date().toISOString()} ${req.method} ${req.path}`);
  next();
};

app.use(logger);

// Authentication middleware
const authenticate = (req, res, next) => {
  const token = req.headers.authorization?.split(" ")[1];
  if (!token) {
    return res.status(401).json({ error: "Unauthorized" });
  }
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    res.status(401).json({ error: "Invalid token" });
  }
};

app.get("/protected", authenticate, (req, res) => {
  res.json({ user: req.user });
});

// Validation middleware
const validateRequest = (schema) => {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.body);
    if (error) {
      return res.status(400).json({ error: error.details[0].message });
    }
    req.body = value;
    next();
  };
};

const userSchema = joi.object({
  email: joi.string().email().required(),
  password: joi.string().min(6).required(),
});

app.post("/users", validateRequest(userSchema), (req, res) => {
  res.json({ message: "User created" });
});

// Rate limiting middleware
const rateLimit = require("express-rate-limit");

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: "Too many requests",
});

app.use("/api/", limiter);

// Conditional middleware
const requireAdmin = (req, res, next) => {
  if (req.user?.role !== "admin") {
    return res.status(403).json({ error: "Forbidden" });
  }
  next();
};

app.delete("/users/:id", authenticate, requireAdmin, (req, res) => {
  res.json({ message: "User deleted" });
});
```

## Middleware Ordering

```javascript
// Global middleware (runs for all routes)
app.use(express.json());
app.use(express.static("public"));
app.use(logger);

// Route-specific middleware
app.get("/public", (req, res) => {
  res.send("Public route");
});

app.get("/protected", authenticate, (req, res) => {
  res.send("Protected route");
});

// Multiple middleware on same route
app.post(
  "/admin/users",
  authenticate,
  requireAdmin,
  validateRequest(userSchema),
  (req, res) => {
    res.json({ message: "User created" });
  }
);

// Middleware for specific path
app.use("/api", authenticate);

// Skip middleware
app.use((req, res, next) => {
  if (req.path === "/public") {
    return next("route"); // Skip to next route
  }
  next();
});
```

## Built-in Middleware

```javascript
// JSON parser
app.use(express.json({ limit: "10mb" }));

// URL-encoded parser
app.use(express.urlencoded({ extended: true, limit: "10mb" }));

// Static file serving
app.use(express.static("public"));
app.use("/downloads", express.static("files"));

// Static with options
app.use(
  express.static("public", {
    maxAge: "1d",
    etag: false,
  })
);

// Router
const router = express.Router();
router.get("/", (req, res) => res.send("Home"));
app.use("/api", router);
```

## Third-party Middleware

```javascript
// CORS
const cors = require("cors");
app.use(cors());

// Compression
const compression = require("compression");
app.use(compression());

// Helmet (security headers)
const helmet = require("helmet");
app.use(helmet());

// Morgan (HTTP request logger)
const morgan = require("morgan");
app.use(morgan("combined"));

// Body parser (deprecated, use express.json)
const bodyParser = require("body-parser");
app.use(bodyParser.json());

// Multer (file upload)
const multer = require("multer");
const upload = multer({ dest: "uploads/" });

app.post("/upload", upload.single("file"), (req, res) => {
  res.json({ filename: req.file.filename });
});

// Cookie parser
const cookieParser = require("cookie-parser");
app.use(cookieParser());

app.get("/cookies", (req, res) => {
  console.log(req.cookies);
  res.cookie("name", "value", { maxAge: 3600000 });
  res.send("Cookie set");
});

// Session
const session = require("express-session");
app.use(
  session({
    secret: "your-secret-key",
    resave: false,
    saveUninitialized: true,
    cookie: { secure: true, httpOnly: true },
  })
);

app.get("/login", (req, res) => {
  req.session.userId = 123;
  res.send("Session set");
});
```

## Error Handling Middleware

```javascript
// Catch all errors
app.use((err, req, res, next) => {
  console.error(err.stack);

  const status = err.status || 500;
  const message = err.message || "Internal server error";

  res.status(status).json({
    error: {
      status,
      message,
      ...(process.env.NODE_ENV === "development" && { stack: err.stack }),
    },
  });
});

// Custom error class
class AppError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

// Throw custom error
app.get("/error", (req, res, next) => {
  next(new AppError("Something went wrong", 400));
});

// Async error handling
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

app.get(
  "/async",
  asyncHandler(async (req, res) => {
    throw new AppError("Async error", 500);
  })
);
```

## Middleware Composition

```javascript
// Compose multiple middleware
const compose = (...middleware) => {
  return (req, res, next) => {
    let index = -1;

    const dispatch = (i) => {
      if (i <= index)
        return Promise.reject(new Error("next() called multiple times"));
      index = i;

      if (i < middleware.length) {
        return Promise.resolve(middleware[i](req, res, () => dispatch(i + 1)));
      }
      return Promise.resolve(next());
    };

    return dispatch(0);
  };
};

// Use composed middleware
const authChain = compose(authenticate, requireAdmin, validateRequest(schema));
app.post("/admin/users", authChain, (req, res) => {
  res.json({ message: "User created" });
});
```
