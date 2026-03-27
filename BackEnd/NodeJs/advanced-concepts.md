# Node.js Advanced Concepts Interview Questions

## EventEmitter

### What is EventEmitter in Node.js and how does it work?

EventEmitter is a core module in Node.js that facilitates communication between objects in Node. It's the foundation of Node's asynchronous event-driven architecture.

Example:

```javascript
const EventEmitter = require('events');

class MyEmitter extends EventEmitter {}
const myEmitter = new MyEmitter();

// Register listener
myEmitter.on('event', (data) => {
    console.log('Event received:', data);
});

// Emit event
myEmitter.emit('event', 'Hello World');
```

### What's the difference between `on()` and `once()`?

Two key event listener methods:

- **on()**: Adds a listener that will be called every time the event is emitted
- **once()**: Adds a one-time listener that will be removed after it's called once

Example:

```javascript
const emitter = new EventEmitter();

// Will be called every time
emitter.on('message', () => console.log('on called'));

// Will be called only once
emitter.once('message', () => console.log('once called'));

emitter.emit('message'); // Logs both messages
emitter.emit('message'); // Logs only 'on called'
```

## Buffers

### What are Buffers in Node.js and when should you use them?

Buffers are used to handle binary data in Node.js. They represent a fixed-length sequence of bytes and are particularly useful when dealing with:

- File system operations
- Network protocols
- Binary data manipulation

Example:

```javascript
// Creating buffers
const buf1 = Buffer.alloc(10);  // Creates a buffer of 10 bytes
const buf2 = Buffer.from('Hello'); // Creates a buffer from string
const buf3 = Buffer.from([1, 2, 3]); // Creates a buffer from array

// Common operations
console.log(buf2.toString()); // Convert to string
console.log(buf2.length);     // Get buffer length
console.log(buf2[0]);         // Access individual bytes
```

### How do you handle large binary files in Node.js?

Using streams with buffers is the best approach for large files:

```javascript
const fs = require('fs');

const readStream = fs.createReadStream('largefile.txt');
const writeStream = fs.createWriteStream('output.txt');

readStream.on('data', (chunk) => {
    // chunk is a buffer
    console.log('Received chunk:', chunk.length, 'bytes');
    writeStream.write(chunk);
});
```

## File System

### What are the different ways to handle files in Node.js?

1. Synchronous (blocking):
```javascript
const fs = require('fs');

try {
    const data = fs.readFileSync('file.txt', 'utf8');
    console.log(data);
} catch (err) {
    console.error('Error reading file:', err);
}
```

2. Asynchronous (non-blocking):
```javascript
const fs = require('fs');

fs.readFile('file.txt', 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading file:', err);
        return;
    }
    console.log(data);
});
```

3. Promises (modern approach):
```javascript
const fs = require('fs/promises');

async function readFile() {
    try {
        const data = await fs.readFile('file.txt', 'utf8');
        console.log(data);
    } catch (err) {
        console.error('Error reading file:', err);
    }
}
```

### How do you watch for file changes in Node.js?
```javascript
const fs = require('fs');

fs.watch('file.txt', (eventType, filename) => {
    console.log(`File ${filename} was ${eventType}`);
});
```

## Streams

### What are Streams in Node.js and what are their types?

Streams are objects that let you read data from a source or write data to a destination continuously. There are four types of streams:

1. Readable Streams:
```javascript
const fs = require('fs');
const readStream = fs.createReadStream('file.txt');

readStream.on('data', (chunk) => {
    console.log('Received chunk:', chunk);
});
```

2. Writable Streams:
```javascript
const writeStream = fs.createWriteStream('output.txt');
writeStream.write('Hello World!');
writeStream.end();
```

3. Duplex Streams (both readable and writable):
```javascript
const { Duplex } = require('stream');

class MyDuplex extends Duplex {
    _read() {}
    _write(chunk, encoding, callback) {
        this.push(chunk);
        callback();
    }
}
```

4. Transform Streams (modify data):
```javascript
const { Transform } = require('stream');

const upperCaseTransform = new Transform({
    transform(chunk, encoding, callback) {
        this.push(chunk.toString().toUpperCase());
        callback();
    }
});
```

### How do you handle backpressure in Node.js streams?

Backpressure is handled automatically when using pipe():
```javascript
const fs = require('fs');

const readStream = fs.createReadStream('input.txt');
const writeStream = fs.createWriteStream('output.txt');

// Handles backpressure automatically
readStream.pipe(writeStream);
```

Manual handling:
```javascript
const writeStream = fs.createWriteStream('output.txt');
let canWrite;

// Write data only when buffer is not full
function writeData() {
    while (canWrite) {
        canWrite = writeStream.write('some data');
    }
}

writeStream.on('drain', () => {
    canWrite = true;
    writeData();
});
```

## Networking

### How do you create a TCP server in Node.js?
```javascript
const net = require('net');

const server = net.createServer((socket) => {
    console.log('Client connected');
    
    socket.on('data', (data) => {
        console.log('Received:', data.toString());
        socket.write('Server received your message');
    });
    
    socket.on('end', () => {
        console.log('Client disconnected');
    });
});

server.listen(3000, () => {
    console.log('Server listening on port 3000');
});
```

### How do you implement a WebSocket server?
Using the `ws` package:
```javascript
const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
    console.log('New client connected');
    
    ws.on('message', (message) => {
        console.log('Received:', message);
        ws.send(`Server received: ${message}`);
    });
    
    ws.on('close', () => {
        console.log('Client disconnected');
    });
});
```

## HTTP

### How do you create an HTTP server in Node.js?
```javascript
const http = require('http');

const server = http.createServer((req, res) => {
    if (req.url === '/') {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('Hello World\n');
    } else if (req.url === '/api') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ message: 'Hello API' }));
    } else {
        res.writeHead(404);
        res.end('Not Found\n');
    }
});

server.listen(3000, () => {
    console.log('Server running at http://localhost:3000/');
});
```

### How do you handle file uploads in Node.js?
Using Express and Multer:
```javascript
const express = require('express');
const multer = require('multer');
const app = express();

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + '-' + file.originalname);
    }
});

const upload = multer({ storage: storage });

app.post('/upload', upload.single('file'), (req, res) => {
    res.json({ message: 'File uploaded successfully' });
});
```

## Multi-Threading

### How does Node.js handle multi-threading with Worker Threads?
```javascript
const { Worker, isMainThread, parentPort } = require('worker_threads');

if (isMainThread) {
    // This code runs in the main thread
    const worker = new Worker(__filename);
    
    worker.on('message', (message) => {
        console.log('From worker:', message);
    });
    
    worker.postMessage('Hello Worker');
} else {
    // This code runs in the worker thread
    parentPort.on('message', (message) => {
        console.log('From main:', message);
        parentPort.postMessage('Hello Main');
    });
}
```

### What's the difference between Worker Threads and Child Processes?
Example using Child Process:
```javascript
const { fork } = require('child_process');

// Parent process
const child = fork('child.js');

child.send({ hello: 'world' });
child.on('message', (message) => {
    console.log('From child:', message);
});

// In child.js
process.on('message', (message) => {
    console.log('From parent:', message);
    process.send({ hello: 'parent' });
});
```

## Security

### How do you implement authentication in Node.js?
Using JWT (JSON Web Tokens):
```javascript
const jwt = require('jsonwebtoken');
const express = require('express');
const app = express();

// Authentication middleware
function authenticate(req, res, next) {
    const token = req.headers.authorization;
    
    if (!token) {
        return res.status(401).json({ message: 'No token provided' });
    }
    
    try {
        const decoded = jwt.verify(token, 'secret_key');
        req.user = decoded;
        next();
    } catch (err) {
        res.status(401).json({ message: 'Invalid token' });
    }
}

// Login route
app.post('/login', (req, res) => {
    // Verify credentials
    const user = { id: 1, username: 'john' };
    const token = jwt.sign(user, 'secret_key');
    res.json({ token });
});

// Protected route
app.get('/protected', authenticate, (req, res) => {
    res.json({ message: 'Protected data', user: req.user });
});
```

### How do you handle input validation and sanitization?
Using Express-Validator:
```javascript
const { body, validationResult } = require('express-validator');

app.post('/user',
    // Validation rules
    body('email').isEmail(),
    body('password').isLength({ min: 6 }),
    body('name').trim().escape(),
    
    (req, res) => {
        // Check for validation errors
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }
        
        // Process valid input
        const { email, password, name } = req.body;
        // ... save user
    }
);
```

## Cryptography

### How do you implement encryption and hashing in Node.js?
```javascript
const crypto = require('crypto');

// Hashing passwords
function hashPassword(password) {
    return crypto.createHash('sha256')
        .update(password)
        .digest('hex');
}

// Encryption/Decryption
function encrypt(text, key) {
    const cipher = crypto.createCipher('aes-256-cbc', key);
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return encrypted;
}

function decrypt(encrypted, key) {
    const decipher = crypto.createDecipher('aes-256-cbc', key);
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
}
```

### How do you generate secure random values?
```javascript
const crypto = require('crypto');

// Generate random bytes
crypto.randomBytes(16, (err, buffer) => {
    if (err) throw err;
    console.log(buffer.toString('hex'));
});

// Generate random string
function generateToken(length = 32) {
    return crypto.randomBytes(length).toString('hex');
}

// Generate random number within range
function secureRandom(min, max) {
    return crypto.randomInt(min, max);
}
```

## Performance Optimization

### How do you profile a Node.js application?
```javascript
const profiler = require('v8-profiler-next');
const fs = require('fs');

// CPU Profiling
profiler.startProfiling('CPU Profile');

setTimeout(() => {
    const profile = profiler.stopProfiling();
    profile.export()
        .pipe(fs.createWriteStream('profile.cpuprofile'))
        .on('finish', () => profile.delete());
}, 30000);

// Memory Heap Snapshot
profiler.takeSnapshot()
    .export()
    .pipe(fs.createWriteStream('snapshot.heapsnapshot'));
```

### How do you implement caching in Node.js?
Using Node-Cache:
```javascript
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 100 });

async function getCachedData(key) {
    // Try to get from cache
    const value = cache.get(key);
    if (value) {
        return value;
    }
    
    // If not in cache, fetch and store
    const data = await fetchDataFromDB(key);
    cache.set(key, data);
    return data;
}
```

## Best Practices

### How do you handle errors in Node.js?
```javascript
// Custom error class
class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = 'ValidationError';
    }
}

// Global error handler (Express)
app.use((err, req, res, next) => {
    console.error(err.stack);
    
    if (err instanceof ValidationError) {
        return res.status(400).json({ error: err.message });
    }
    
    res.status(500).json({ error: 'Something broke!' });
});

// Async error handling
async function handleRequest(req, res, next) {
    try {
        const data = await processRequest(req);
        res.json(data);
    } catch (err) {
        next(err); // Pass to error handler
    }
}
```

### How do you implement graceful shutdown?
```javascript
const server = app.listen(3000);

function gracefulShutdown() {
    console.log('Starting graceful shutdown...');
    
    server.close(() => {
        console.log('Server closed');
        
        // Close database connections
        mongoose.connection.close(false, () => {
            console.log('Database connection closed');
            process.exit(0);
        });
    });
    
    // Force close if graceful shutdown fails
    setTimeout(() => {
        console.error('Could not close connections in time, forcefully shutting down');
        process.exit(1);
    }, 10000);
}

// Listen for shutdown signals
process.on('SIGTERM', gracefulShutdown);
process.on('SIGINT', gracefulShutdown);
```