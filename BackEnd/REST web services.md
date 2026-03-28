# REST Web Services Guide

## REST Principles

### 1. Resource Identification
```
// Good URLs
GET /users
GET /users/123
GET /users/123/orders

// Bad URLs
GET /getUsers
GET /getUserById/123
GET /getUserOrders/123
```

### 2. HTTP Methods

#### GET - Read
```http
GET /api/users
GET /api/users/123

// Query Parameters
GET /api/users?role=admin
GET /api/users?page=1&limit=10
```

#### POST - Create
```http
POST /api/users
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com"
}
```

#### PUT - Update (Full)
```http
PUT /api/users/123
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
}
```

#### PATCH - Update (Partial)
```http
PATCH /api/users/123
Content-Type: application/json

{
    "email": "newemail@example.com"
}
```

#### DELETE - Remove
```http
DELETE /api/users/123
```

### 3. Response Status Codes

#### Success Responses
```http
200 OK - Request succeeded
201 Created - Resource created
204 No Content - Request succeeded but no content returned
```

#### Client Error Responses
```http
400 Bad Request - Invalid request format
401 Unauthorized - Authentication required
403 Forbidden - Authentication succeeded but user lacks permissions
404 Not Found - Resource not found
422 Unprocessable Entity - Validation failed
```

#### Server Error Responses
```http
500 Internal Server Error - Server error
503 Service Unavailable - Server temporarily unavailable
```

## Best Practices

### 1. Versioning
```http
// URL Versioning
GET /api/v1/users
GET /api/v2/users

// Header Versioning
GET /api/users
Accept: application/vnd.company.api+json;version=1
```

### 2. Filtering, Sorting, and Pagination
```http
// Filtering
GET /api/users?role=admin
GET /api/products?category=electronics&price[gte]=100

// Sorting
GET /api/users?sort=name
GET /api/users?sort=-createdAt

// Pagination
GET /api/users?page=2&limit=10
GET /api/users?offset=20&limit=10
```

### 3. Response Format
```javascript
// Success Response
{
    "data": {
        "id": "123",
        "name": "John Doe",
        "email": "john@example.com"
    },
    "meta": {
        "timestamp": "2025-07-11T10:00:00Z"
    }
}

// Error Response
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": [
            {
                "field": "email",
                "message": "Invalid email format"
            }
        ]
    }
}

// Collection Response
{
    "data": [
        {
            "id": "123",
            "name": "John Doe"
        },
        {
            "id": "124",
            "name": "Jane Smith"
        }
    ],
    "meta": {
        "total": 50,
        "page": 1,
        "limit": 10
    }
}
```

### 4. Authentication
```http
// Bearer Token
GET /api/users
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

// API Key
GET /api/users
X-API-Key: your-api-key-here
```

### 5. Rate Limiting
```http
// Response Headers
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 98
X-RateLimit-Reset: 1436452399

// Rate Limit Exceeded Response
429 Too Many Requests
{
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Rate limit exceeded. Try again in 60 seconds"
    }
}
```

## Implementation Examples

### Express.js REST API
```javascript
const express = require('express');
const app = express();

// Middleware
app.use(express.json());
app.use(authMiddleware);

// Routes
app.get('/api/users', async (req, res) => {
    try {
        const users = await User.find()
            .skip(parseInt(req.query.offset))
            .limit(parseInt(req.query.limit));
            
        res.json({
            data: users,
            meta: {
                total: await User.count()
            }
        });
    } catch (error) {
        res.status(500).json({
            error: {
                message: 'Internal server error'
            }
        });
    }
});

app.post('/api/users', async (req, res) => {
    try {
        const user = new User(req.body);
        await user.validate();
        await user.save();
        
        res.status(201).json({
            data: user
        });
    } catch (error) {
        if (error.name === 'ValidationError') {
            res.status(422).json({
                error: {
                    code: 'VALIDATION_ERROR',
                    message: 'Invalid input data',
                    details: Object.values(error.errors).map(err => ({
                        field: err.path,
                        message: err.message
                    }))
                }
            });
        } else {
            res.status(500).json({
                error: {
                    message: 'Internal server error'
                }
            });
        }
    }
});
```

### Error Handling Middleware
```javascript
function errorHandler(err, req, res, next) {
    console.error(err.stack);
    
    if (err.type === 'validation') {
        return res.status(422).json({
            error: {
                code: 'VALIDATION_ERROR',
                message: err.message,
                details: err.details
            }
        });
    }
    
    res.status(500).json({
        error: {
            code: 'INTERNAL_ERROR',
            message: 'An unexpected error occurred'
        }
    });
}

app.use(errorHandler);
```

### Authentication Middleware
```javascript
async function authMiddleware(req, res, next) {
    const token = req.headers.authorization?.split(' ')[1];
    
    if (!token) {
        return res.status(401).json({
            error: {
                code: 'UNAUTHORIZED',
                message: 'Authentication required'
            }
        });
    }
    
    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded;
        next();
    } catch (error) {
        res.status(401).json({
            error: {
                code: 'INVALID_TOKEN',
                message: 'Invalid or expired token'
            }
        });
    }
}
```

### Rate Limiting Middleware
```javascript
const rateLimit = require('express-rate-limit');

const apiLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
    handler: function (req, res) {
        res.status(429).json({
            error: {
                code: 'RATE_LIMIT_EXCEEDED',
                message: 'Too many requests'
            }
        });
    }
});

app.use('/api/', apiLimiter);
```