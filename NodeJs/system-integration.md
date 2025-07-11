# Node.js System Integration Interview Questions

## Understanding Unix Integration

### 1. How do you execute shell commands from Node.js?
```javascript
const { exec, spawn } = require('child_process');

// Using exec for simple commands
exec('ls -la', (error, stdout, stderr) => {
    if (error) {
        console.error(`Error: ${error}`);
        return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
});

// Using spawn for long-running processes
const process = spawn('find', ['.', '-type', 'f']);

process.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
});

process.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
});

process.on('close', (code) => {
    console.log(`Child process exited with code ${code}`);
});
```

### 2. How do you handle environment variables in Node.js?
```javascript
// Using dotenv for environment management
require('dotenv').config();

// Access environment variables
const dbConnection = {
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
};

// Setting environment variables programmatically
process.env.NODE_ENV = 'production';

// Check environment
const isDevelopment = process.env.NODE_ENV === 'development';
```

## Process Management

### 1. How do you manage multiple Node.js processes?
Using PM2:
```javascript
// ecosystem.config.js
module.exports = {
    apps: [{
        name: "app",
        script: "./app.js",
        instances: "max",
        exec_mode: "cluster",
        env: {
            NODE_ENV: "development",
        },
        env_production: {
            NODE_ENV: "production",
        }
    }]
};

// Start with PM2
// pm2 start ecosystem.config.js

// Monitoring
// pm2 monit
```

### 2. How do you handle process signals in Node.js?
```javascript
// Handle process signals
process.on('SIGTERM', () => {
    console.log('Received SIGTERM. Performing cleanup...');
    cleanup();
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('Received SIGINT. Performing cleanup...');
    cleanup();
    process.exit(0);
});

process.on('uncaughtException', (error) => {
    console.error('Uncaught Exception:', error);
    cleanup();
    process.exit(1);
});

function cleanup() {
    // Close database connections
    // Clear temporary files
    // Save state
    console.log('Cleanup completed');
}
```

## File System Operations

### 1. How do you handle file permissions in Node.js?
```javascript
const fs = require('fs');

// Change file permissions
fs.chmod('file.txt', 0o755, (err) => {
    if (err) throw err;
    console.log('Permissions changed');
});

// Check file permissions
fs.access('file.txt', fs.constants.W_OK, (err) => {
    if (err) {
        console.error('File is not writable');
    } else {
        console.log('File is writable');
    }
});

// Set file owner
fs.chown('file.txt', uid, gid, (err) => {
    if (err) throw err;
    console.log('Owner changed');
});
```

### 2. How do you handle symbolic links?
```javascript
const fs = require('fs');

// Create symbolic link
fs.symlink('target.txt', 'link.txt', 'file', (err) => {
    if (err) throw err;
    console.log('Symbolic link created');
});

// Read symbolic link
fs.readlink('link.txt', (err, linkString) => {
    if (err) throw err;
    console.log('Link points to:', linkString);
});

// Check if path is symbolic link
fs.lstat('link.txt', (err, stats) => {
    if (err) throw err;
    console.log('Is symbolic link:', stats.isSymbolicLink());
});
```

## System Resources

### 1. How do you monitor system resources in Node.js?
```javascript
const os = require('os');

// Memory usage
function getMemoryUsage() {
    const total = os.totalmem();
    const free = os.freemem();
    const used = total - free;
    const usedPercentage = (used / total) * 100;
    
    return {
        total: formatBytes(total),
        free: formatBytes(free),
        used: formatBytes(used),
        usedPercentage: `${usedPercentage.toFixed(2)}%`
    };
}

// CPU usage
function getCPUUsage() {
    const cpus = os.cpus();
    return cpus.map(cpu => {
        const total = Object.values(cpu.times).reduce((acc, tv) => acc + tv, 0);
        const idle = cpu.times.idle;
        const usage = ((total - idle) / total) * 100;
        return `${usage.toFixed(2)}%`;
    });
}

function formatBytes(bytes) {
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}
```

### 2. How do you implement resource limits?
```javascript
// Memory limits
const v8 = require('v8');

// Set heap size limits
v8.setFlagsFromString('--max_old_space_size=4096'); // 4GB

// Monitor heap usage
const heapStats = v8.getHeapStatistics();
console.log('Heap size limit:', formatBytes(heapStats.heap_size_limit));

// Process resource limits
process.setMaxListeners(15); // Set max event listeners

// Rate limiting example (using express-rate-limit)
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests per windowMs
});

app.use(limiter);
```

## Inter-Process Communication

### 1. How do you implement IPC in Node.js?
```javascript
// Parent process
const { fork } = require('child_process');
const child = fork('worker.js');

// Send message to child
child.send({ type: 'START', data: { x: 1, y: 2 } });

// Receive message from child
child.on('message', (message) => {
    console.log('From child:', message);
});

// In worker.js
process.on('message', (message) => {
    if (message.type === 'START') {
        // Process data
        const result = message.data.x + message.data.y;
        // Send result back to parent
        process.send({ type: 'RESULT', data: result });
    }
});
```

### 2. How do you implement shared memory?
```javascript
const { Worker, SharedArrayBuffer } = require('worker_threads');

// Create shared buffer
const sharedBuffer = new SharedArrayBuffer(4);
const sharedArray = new Int32Array(sharedBuffer);

// Create worker
const worker = new Worker(`
    const { parentPort } = require('worker_threads');
    
    parentPort.on('message', ({ buffer }) => {
        const array = new Int32Array(buffer);
        array[0] = 42;
        parentPort.postMessage('Done');
    });
`);

// Send shared buffer to worker
worker.postMessage({ buffer: sharedBuffer });

// Wait for worker to finish
worker.on('message', (message) => {
    console.log('Worker says:', message);
    console.log('Shared array value:', sharedArray[0]); // 42
});
```

## System Integration Best Practices

### 1. How do you implement logging in a production environment?
```javascript
const winston = require('winston');
require('winston-daily-rotate-file');

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        // Rotate log files daily
        new winston.transports.DailyRotateFile({
            filename: 'logs/application-%DATE%.log',
            datePattern: 'YYYY-MM-DD',
            maxSize: '20m',
            maxFiles: '14d'
        }),
        // Send errors to separate file
        new winston.transports.File({
            filename: 'logs/error.log',
            level: 'error'
        })
    ]
});

// In development, log to console
if (process.env.NODE_ENV !== 'production') {
    logger.add(new winston.transports.Console({
        format: winston.format.simple()
    }));
}
```

### 2. How do you implement health checks?
```javascript
const express = require('express');
const app = express();

// Basic health check
app.get('/health', (req, res) => {
    res.json({
        status: 'UP',
        timestamp: new Date(),
        uptime: process.uptime(),
        memoryUsage: process.memoryUsage()
    });
});

// Detailed health check with dependencies
async function checkHealth() {
    try {
        // Check database connection
        await mongoose.connection.db.admin().ping();
        
        // Check Redis connection
        await redisClient.ping();
        
        // Check external API
        await axios.get('https://api.example.com/health');
        
        return {
            status: 'UP',
            checks: {
                database: 'UP',
                redis: 'UP',
                api: 'UP'
            }
        };
    } catch (error) {
        return {
            status: 'DOWN',
            error: error.message
        };
    }
}

app.get('/health/detailed', async (req, res) => {
    const health = await checkHealth();
    res.status(health.status === 'UP' ? 200 : 503).json(health);
});
```