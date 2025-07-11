# Node.js Compression and Advanced Streams

## Compression

### 1. How do you implement file compression in Node.js?
```javascript
const fs = require('fs');
const zlib = require('zlib');

// Compress a file
function compressFile(inputFile, outputFile) {
    const gzip = zlib.createGzip();
    const source = fs.createReadStream(inputFile);
    const destination = fs.createWriteStream(outputFile);
    
    return new Promise((resolve, reject) => {
        source
            .pipe(gzip)
            .pipe(destination)
            .on('finish', resolve)
            .on('error', reject);
    });
}

// Decompress a file
function decompressFile(inputFile, outputFile) {
    const gunzip = zlib.createGunzip();
    const source = fs.createReadStream(inputFile);
    const destination = fs.createWriteStream(outputFile);
    
    return new Promise((resolve, reject) => {
        source
            .pipe(gunzip)
            .pipe(destination)
            .on('finish', resolve)
            .on('error', reject);
    });
}

// Usage
async function example() {
    try {
        await compressFile('large.txt', 'large.txt.gz');
        console.log('File compressed');
        
        await decompressFile('large.txt.gz', 'large_restored.txt');
        console.log('File decompressed');
    } catch (err) {
        console.error('Error:', err);
    }
}
```

### 2. How do you implement HTTP compression?
```javascript
const express = require('express');
const compression = require('compression');
const app = express();

// Enable compression for all routes
app.use(compression({
    // Custom compression filter
    filter: (req, res) => {
        if (req.headers['x-no-compression']) {
            return false;
        }
        // Use compression for text files
        return compression.filter(req, res);
    },
    // Compression level (0-9)
    level: 6
}));

// Route handler
app.get('/api/data', (req, res) => {
    const largeData = { /* ... */ };
    res.json(largeData); // Will be automatically compressed
});
```

## Advanced Stream Concepts

### 1. How do you implement custom streams?

1. Custom Readable Stream:
```javascript
const { Readable } = require('stream');

class NumberStream extends Readable {
    constructor(max) {
        super();
        this.max = max;
        this.current = 1;
    }
    
    _read() {
        if (this.current <= this.max) {
            const buf = Buffer.from(String(this.current));
            this.push(buf);
            this.current++;
        } else {
            this.push(null);
        }
    }
}

// Usage
const numberStream = new NumberStream(5);
numberStream.on('data', (chunk) => {
    console.log(chunk.toString());
});
```

2. Custom Writable Stream:
```javascript
const { Writable } = require('stream');

class ConsoleStream extends Writable {
    _write(chunk, encoding, callback) {
        console.log('Received:', chunk.toString());
        callback();
    }
}

// Usage
const consoleStream = new ConsoleStream();
consoleStream.write('Hello');
consoleStream.end('World');
```

3. Custom Transform Stream:
```javascript
const { Transform } = require('stream');

class ReverseStream extends Transform {
    _transform(chunk, encoding, callback) {
        const reversed = chunk.toString()
            .split('')
            .reverse()
            .join('');
        
        this.push(reversed);
        callback();
    }
}

// Usage
const reverser = new ReverseStream();
process.stdin
    .pipe(reverser)
    .pipe(process.stdout);
```

### 2. How do you handle stream errors and backpressure?

1. Error Handling:
```javascript
const fs = require('fs');
const { pipeline } = require('stream');

function handleStreams(inputFile, outputFile) {
    const readStream = fs.createReadStream(inputFile);
    const writeStream = fs.createWriteStream(outputFile);
    
    // Using pipeline for better error handling
    pipeline(
        readStream,
        writeStream,
        (err) => {
            if (err) {
                console.error('Pipeline failed:', err);
            } else {
                console.log('Pipeline succeeded');
            }
        }
    );
    
    // Individual error handlers
    readStream.on('error', (err) => {
        console.error('Read error:', err);
    });
    
    writeStream.on('error', (err) => {
        console.error('Write error:', err);
    });
}
```

2. Backpressure Management:
```javascript
const fs = require('fs');

class ThrottledStream extends Writable {
    constructor(options) {
        super(options);
        this.delay = options.delay || 100;
    }
    
    _write(chunk, encoding, callback) {
        // Simulate processing delay
        setTimeout(() => {
            console.log(chunk.toString());
            callback();
        }, this.delay);
    }
}

// Usage with backpressure handling
const readable = fs.createReadStream('large.txt');
const throttled = new ThrottledStream({ delay: 100 });

readable.pipe(throttled);

// Monitor backpressure
readable.on('data', () => {
    const readableBuffered = readable.readableLength;
    const writableBuffered = throttled.writableLength;
    
    console.log(`Buffered: Read=${readableBuffered}, Write=${writableBuffered}`);
});
```

### 3. How do you implement stream multiplexing?

```javascript
const { PassThrough } = require('stream');

class Multiplexer {
    constructor() {
        this.streams = new Map();
    }
    
    createStream(id) {
        const stream = new PassThrough();
        this.streams.set(id, stream);
        return stream;
    }
    
    removeStream(id) {
        const stream = this.streams.get(id);
        if (stream) {
            stream.end();
            this.streams.delete(id);
        }
    }
    
    broadcast(data) {
        for (const stream of this.streams.values()) {
            stream.write(data);
        }
    }
}

// Usage example
const mux = new Multiplexer();

// Create multiple streams
const stream1 = mux.createStream(1);
const stream2 = mux.createStream(2);

// Handle data on individual streams
stream1.on('data', (data) => {
    console.log('Stream 1:', data.toString());
});

stream2.on('data', (data) => {
    console.log('Stream 2:', data.toString());
});

// Broadcast data to all streams
mux.broadcast('Hello to all streams!');
```

### 4. How do you implement stream chaining with promises?

```javascript
const { Transform } = require('stream');
const { promisify } = require('util');
const pipeline = promisify(require('stream').pipeline);

// Transform streams
class UppercaseTransform extends Transform {
    _transform(chunk, encoding, callback) {
        this.push(chunk.toString().toUpperCase());
        callback();
    }
}

class ReverseTransform extends Transform {
    _transform(chunk, encoding, callback) {
        this.push(chunk.toString().split('').reverse().join(''));
        callback();
    }
}

// Promise-based stream processing
async function processStream(inputStream) {
    try {
        await pipeline(
            inputStream,
            new UppercaseTransform(),
            new ReverseTransform(),
            process.stdout
        );
        console.log('Processing completed');
    } catch (err) {
        console.error('Processing failed:', err);
    }
}

// Usage
const { Readable } = require('stream');
const source = Readable.from(['hello', 'world']);
processStream(source);
```