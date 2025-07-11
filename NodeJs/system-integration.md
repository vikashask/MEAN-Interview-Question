# Node.js System Integration Guide

## Child Processes

### spawn()
```javascript
const { spawn } = require('child_process');

// Execute command with arguments
const ls = spawn('ls', ['-lh', '/usr']);

ls.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
});

ls.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
});

ls.on('close', (code) => {
    console.log(`Child process exited with code ${code}`);
});
```

### exec()
```javascript
const { exec } = require('child_process');

exec('ls -lh /usr', (error, stdout, stderr) => {
    if (error) {
        console.error(`Error: ${error}`);
        return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
});
```

### execFile()
```javascript
const { execFile } = require('child_process');

execFile('node', ['--version'], (error, stdout, stderr) => {
    if (error) {
        console.error(`Error: ${error}`);
        return;
    }
    console.log(`Node Version: ${stdout}`);
});
```

### fork()
```javascript
const { fork } = require('child_process');

// Fork a new Node.js process
const child = fork('worker.js');

// Send message to child
child.send({ hello: 'world' });

// Receive messages from child
child.on('message', (message) => {
    console.log('Message from child:', message);
});
```

## File System Operations

### Asynchronous File Operations
```javascript
const fs = require('fs').promises;

async function processFile() {
    try {
        // Read file
        const content = await fs.readFile('input.txt', 'utf8');
        
        // Process content
        const modified = content.toUpperCase();
        
        // Write back
        await fs.writeFile('output.txt', modified);
        
        console.log('File processing complete');
    } catch (error) {
        console.error('Error:', error);
    }
}
```

### File System Monitoring
```javascript
const fs = require('fs');

// Watch directory for changes
fs.watch('directory', (eventType, filename) => {
    console.log(`Event: ${eventType}`);
    if (filename) {
        console.log(`File changed: ${filename}`);
    }
});
```

### Directory Operations
```javascript
const fs = require('fs').promises;

async function processDirectory() {
    try {
        // Create directory
        await fs.mkdir('new-directory');
        
        // Read directory contents
        const files = await fs.readdir('directory');
        
        // Process each file
        for (const file of files) {
            const stats = await fs.stat(`directory/${file}`);
            console.log(`${file}: ${stats.size} bytes`);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
```

## Network Integration

### HTTP Server
```javascript
const http = require('http');

const server = http.createServer((req, res) => {
    if (req.url === '/api/data') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ message: 'Hello World' }));
    } else {
        res.writeHead(404);
        res.end();
    }
});

server.listen(3000, () => {
    console.log('Server running on port 3000');
});
```

### TCP Server
```javascript
const net = require('net');

const server = net.createServer((socket) => {
    console.log('Client connected');
    
    socket.on('data', (data) => {
        console.log(`Received: ${data}`);
        socket.write(`Server received: ${data}`);
    });
    
    socket.on('end', () => {
        console.log('Client disconnected');
    });
});

server.listen(8080, () => {
    console.log('TCP Server listening on port 8080');
});
```

### WebSocket Integration
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

## Database Integration

### MongoDB Connection
```javascript
const { MongoClient } = require('mongodb');

async function connectDB() {
    const client = new MongoClient('mongodb://localhost:27017');
    
    try {
        await client.connect();
        const db = client.db('mydb');
        
        // Perform operations
        const users = await db.collection('users').find().toArray();
        console.log('Users:', users);
    } finally {
        await client.close();
    }
}
```

### Redis Integration
```javascript
const Redis = require('ioredis');
const redis = new Redis();

// Set value
await redis.set('key', 'value');

// Get value
const value = await redis.get('key');

// Set with expiration
await redis.set('session', 'data', 'EX', 3600);

// Pub/Sub
const subscriber = new Redis();
const publisher = new Redis();

subscriber.subscribe('channel', (err, count) => {
    if (err) console.error(err);
    console.log(`Subscribed to ${count} channels`);
});

subscriber.on('message', (channel, message) => {
    console.log(`Received ${message} from ${channel}`);
});

publisher.publish('channel', 'Hello World');
```

## System Integration Best Practices

1. Error Handling
```javascript
process.on('uncaughtException', (error) => {
    console.error('Uncaught Exception:', error);
    // Graceful shutdown
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection:', reason);
});
```

2. Graceful Shutdown
```javascript
function gracefulShutdown() {
    console.log('Starting graceful shutdown...');
    
    // Close server
    server.close(() => {
        console.log('Server closed');
        
        // Close database connections
        mongoose.connection.close(false, () => {
            console.log('Database connections closed');
            process.exit(0);
        });
    });
    
    // Force close if graceful shutdown fails
    setTimeout(() => {
        console.error('Could not close connections in time, forcefully shutting down');
        process.exit(1);
    }, 10000);
}

process.on('SIGTERM', gracefulShutdown);
process.on('SIGINT', gracefulShutdown);
```

3. Configuration Management
```javascript
const config = {
    port: process.env.PORT || 3000,
    dbUrl: process.env.DB_URL || 'mongodb://localhost:27017',
    environment: process.env.NODE_ENV || 'development'
};

module.exports = config;
```

4. Logging
```javascript
const winston = require('winston');

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.json(),
    transports: [
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' })
    ]
});

if (process.env.NODE_ENV !== 'production') {
    logger.add(new winston.transports.Console({
        format: winston.format.simple()
    }));
}
```