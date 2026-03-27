# Security Best Practices

## Input Validation & Sanitization

```javascript
const joi = require("joi");
const xss = require("xss");
const mongoSanitize = require("express-mongo-sanitize");

// Validate input with Joi
const userSchema = joi.object({
  email: joi.string().email().required(),
  password: joi.string().min(8).required(),
  name: joi.string().max(100).required(),
});

const validateInput = (schema) => {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.body);
    if (error) {
      return res.status(400).json({ error: error.details[0].message });
    }
    req.body = value;
    next();
  };
};

app.post("/users", validateInput(userSchema), (req, res) => {
  res.json({ message: "User created" });
});

// Sanitize HTML
const sanitizedInput = xss(userInput);

// MongoDB injection prevention
app.use(mongoSanitize());

// Rate limiting
const rateLimit = require("express-rate-limit");

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: "Too many requests",
});

app.use("/api/", limiter);

// Stricter for login
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  skipSuccessfulRequests: true,
});

app.post("/login", loginLimiter, (req, res) => {
  // Login logic
});
```

## CORS Configuration

```javascript
const cors = require("cors");

// Allow specific origins
app.use(
  cors({
    origin: ["https://example.com", "https://app.example.com"],
    credentials: true,
    methods: ["GET", "POST", "PUT", "DELETE"],
    allowedHeaders: ["Content-Type", "Authorization"],
  })
);

// Dynamic origin check
app.use(
  cors({
    origin: (origin, callback) => {
      const whitelist = process.env.ALLOWED_ORIGINS.split(",");
      if (whitelist.includes(origin) || !origin) {
        callback(null, true);
      } else {
        callback(new Error("Not allowed by CORS"));
      }
    },
  })
);
```

## HTTPS & SSL/TLS

```javascript
const https = require("https");
const fs = require("fs");

// Load certificates
const options = {
  key: fs.readFileSync("private-key.pem"),
  cert: fs.readFileSync("certificate.pem"),
};

// Create HTTPS server
https.createServer(options, app).listen(443, () => {
  console.log("HTTPS server running");
});

// Redirect HTTP to HTTPS
app.use((req, res, next) => {
  if (req.header("x-forwarded-proto") !== "https") {
    res.redirect(`https://${req.header("host")}${req.url}`);
  } else {
    next();
  }
});
```

## Security Headers

```javascript
const helmet = require("helmet");

// Add security headers
app.use(helmet());

// Custom headers
app.use((req, res, next) => {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "DENY");
  res.setHeader("X-XSS-Protection", "1; mode=block");
  res.setHeader(
    "Strict-Transport-Security",
    "max-age=31536000; includeSubDomains"
  );
  next();
});
```

## SQL Injection Prevention

```javascript
// Use parameterized queries
const query = "SELECT * FROM users WHERE email = ?";
const [rows] = await pool.query(query, [email]);

// ORM prevents SQL injection
const user = await User.findOne({ where: { email } });

// Never concatenate user input
// ❌ Bad
const query = `SELECT * FROM users WHERE email = '${email}'`;

// ✅ Good
const query = "SELECT * FROM users WHERE email = ?";
```

## XSS Prevention

```javascript
// Sanitize output
const xss = require('xss');
const sanitized = xss(userInput);

// Use template escaping
// In EJS
<%= userInput %>  <!-- Automatically escaped -->

// In Handlebars
{{userInput}}  <!-- Automatically escaped -->

// Content Security Policy
app.use((req, res, next) => {
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self' 'unsafe-inline'"
  );
  next();
});
```

## CSRF Protection

```javascript
const csrf = require("csurf");
const cookieParser = require("cookie-parser");

app.use(cookieParser());
app.use(csrf({ cookie: true }));

// Add token to forms
app.get("/form", (req, res) => {
  res.send(`
    <form method="POST" action="/submit">
      <input type="hidden" name="_csrf" value="${req.csrfToken()}">
      <input type="text" name="data">
      <button>Submit</button>
    </form>
  `);
});

// Verify token on POST
app.post("/submit", (req, res) => {
  res.json({ message: "Form submitted" });
});
```

## Environment Variables & Secrets

```javascript
// .env file
DATABASE_URL=mongodb://localhost:27017/mydb
JWT_SECRET=your-secret-key
API_KEY=your-api-key

// Load environment variables
require('dotenv').config();

// Access variables
const dbUrl = process.env.DATABASE_URL;
const jwtSecret = process.env.JWT_SECRET;

// Never commit .env
// Add to .gitignore
// .env
// .env.local

// Use different secrets per environment
// .env.development
// .env.production
// .env.test
```

## Dependency Security

```bash
# Check for vulnerabilities
npm audit

# Fix vulnerabilities
npm audit fix

# Update packages
npm update

# Use lockfile
npm ci  # Install exact versions from package-lock.json

# Security scanning
npm install -g snyk
snyk test
```

## Logging & Monitoring

```javascript
const winston = require("winston");

const logger = winston.createLogger({
  level: "info",
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: "error.log", level: "error" }),
    new winston.transports.File({ filename: "combined.log" }),
  ],
});

// Log security events
logger.warn("Failed login attempt", { email, ip: req.ip });
logger.error("Unauthorized access attempt", {
  userId: req.user?.id,
  resource: req.path,
});

// Monitor for suspicious activity
const suspiciousActivity = async (req, res, next) => {
  const failedAttempts = await FailedLogin.countDocuments({
    ip: req.ip,
    timestamp: { $gte: Date.now() - 15 * 60 * 1000 },
  });

  if (failedAttempts > 5) {
    return res.status(429).json({ error: "Too many failed attempts" });
  }

  next();
};
```
