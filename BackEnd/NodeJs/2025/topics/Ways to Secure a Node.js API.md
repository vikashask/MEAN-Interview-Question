# Ways to Secure a Node.js API

Securing a Node.js API is critical to protect data, prevent unauthorized access, and ensure the integrity of your application. Here are the common and effective ways to secure a Node.js API:

---

## 1. Use HTTPS

- Always use HTTPS to encrypt data in transit.
- Redirect all HTTP requests to HTTPS.

```js
const https = require('https');
const fs = require('fs');
const app = require('express')();

https.createServer({
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem')
}, app).listen(443);
```

## 2. Authentication

- Implement strong authentication mechanisms like:
  - JWT (JSON Web Tokens)
  - OAuth2
  - API keys
- Use secure password storage (e.g., bcrypt).

```js
const jwt = require('jsonwebtoken');
const token = jwt.sign({ userId: 123 }, 'your-secret-key', { expiresIn: '1h' });
```

## 3. Authorization

- Enforce role-based access control (RBAC).
- Limit resource access based on user permissions.

```js
function checkAdmin(req, res, next) {
  if (req.user.role !== 'admin') return res.status(403).send('Access denied.');
  next();
}
```

## 4. Input Validation and Sanitization

- Validate all user inputs using libraries like `express-validator` or `Joi`.
- Sanitize inputs to prevent injection attacks (e.g., SQL injection, NoSQL injection, XSS).

```js
const { body } = require('express-validator');

app.post('/user', [
  body('email').isEmail(),
  body('password').isLength({ min: 5 })
], (req, res) => { ... });
```

## 5. Rate Limiting and Throttling

- Use middleware like `express-rate-limit` to:
  - Limit number of requests per user/IP.
  - Prevent brute force attacks and DoS.

```js
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
});
app.use(limiter);
```

## 6. Secure Headers

- Use `helmet` middleware to set HTTP security headers.

```js
const helmet = require('helmet');
app.use(helmet());
```

## 7. CORS Configuration

- Configure CORS properly to only allow trusted origins.

```js
const cors = require('cors');
app.use(cors({ origin: 'https://yourdomain.com' }));
```

## 8. Avoid Information Leakage

- Don't expose stack traces or error messages to users.
- Customize error handling middleware.

```js
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something went wrong!');
});
```

## 9. Use Environment Variables

- Store sensitive config (e.g., DB credentials, API keys) in environment variables, not in code.

```js
require('dotenv').config();
const dbPassword = process.env.DB_PASSWORD;
```

## 10. Keep Dependencies Updated

- Regularly update packages using `npm audit` or `snyk`.
- Remove unused or vulnerable packages.

```bash
npm audit fix
```

## 11. Use a Web Application Firewall (WAF)

- Protect APIs against known threats and automated attacks.

```text
Use services like Cloudflare or AWS WAF to protect your API from common threats.
```

## 12. Logging and Monitoring

- Log all access and errors.
- Use monitoring tools to detect suspicious activity.

```js
const morgan = require('morgan');
app.use(morgan('combined'));
```

## 13. CSRF Protection

- Use CSRF tokens if your API interacts with browsers and uses cookies.

```js
const csurf = require('csurf');
app.use(csurf());
```

## 14. Secure Your Database

- Enforce least privilege access for DB users.
- Use parameterized queries or ORM frameworks.

```js
const user = await User.findOne({ email: req.body.email }); // Using Mongoose ORM
```

## 15. Container and Deployment Security

- Use Docker best practices (non-root users, image scanning).
- Apply security patches and use secure cloud configurations.

```dockerfile
FROM node:18-alpine
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

---

By applying these security practices, you can significantly reduce vulnerabilities and protect your Node.js API from various threats.