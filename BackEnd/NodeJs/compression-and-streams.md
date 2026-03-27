# Node.js Compression and Streams

## Streams

### Stream Types

#### Readable Streams
```javascript
const fs = require('fs');

// Create readable stream
const readStream = fs.createReadStream('input.txt', {
    encoding: 'utf8',
    highWaterMark: 64 * 1024 // 64KB chunks
});

// Handle data
readStream.on('data', (chunk) => {
    console.log('Received chunk:', chunk.length);
});

readStream.on('end', () => {
    console.log('Finished reading');
});

readStream.on('error', (error) => {
    console.error('Error:', error);
});
```

#### Writable Streams
```javascript
const writeStream = fs.createWriteStream('output.txt');

// Write data
writeStream.write('Hello ');
writeStream.write('World!');
writeStream.end();

// Handle events
writeStream.on('finish', () => {
    console.log('Finished writing');
});

writeStream.on('error', (error) => {
    console.error('Error:', error);
});
```

#### Duplex Streams
```javascript
const { Duplex } = require('stream');

class MyDuplex extends Duplex {
    constructor(options) {
        super(options);
        this.data = ['Hello', 'World', '!'];
    }
    
    _read() {
        const data = this.data.shift();
        if (data) {
            this.push(data);
        } else {
            this.push(null);
        }
    }
    
    _write(chunk, encoding, callback) {
        console.log('Received:', chunk.toString());
        callback();
    }
}
```

#### Transform Streams
```javascript
const { Transform } = require('stream');

class UppercaseTransform extends Transform {
    _transform(chunk, encoding, callback) {
        this.push(chunk.toString().toUpperCase());
        callback();
    }
}

const upperCaseStream = new UppercaseTransform();
process.stdin
    .pipe(upperCaseStream)
    .pipe(process.stdout);
```

### Stream Operations

#### Piping Streams
```javascript
const fs = require('fs');
const zlib = require('zlib');

// Chain multiple streams
fs.createReadStream('input.txt')
    .pipe(zlib.createGzip())
    .pipe(fs.createWriteStream('input.txt.gz'));

// Handle pipe errors
source.pipe(destination)
    .on('error', (error) => {
        console.error('Pipe error:', error);
    });
```

#### Stream Events
```javascript
readStream
    .on('data', (chunk) => {
        console.log('Data:', chunk);
    })
    .on('end', () => {
        console.log('End of stream');
    })
    .on('error', (error) => {
        console.error('Error:', error);
    })
    .on('close', () => {
        console.log('Stream closed');
    });
```

## Compression

### Gzip Compression
```javascript
const zlib = require('zlib');
const fs = require('fs');

// Compress file
function compressFile(input, output) {
    const gzip = zlib.createGzip();
    const source = fs.createReadStream(input);
    const destination = fs.createWriteStream(output);
    
    return new Promise((resolve, reject) => {
        source
            .pipe(gzip)
            .pipe(destination)
            .on('finish', resolve)
            .on('error', reject);
    });
}

// Decompress file
function decompressFile(input, output) {
    const gunzip = zlib.createGunzip();
    const source = fs.createReadStream(input);
    const destination = fs.createWriteStream(output);
    
    return new Promise((resolve, reject) => {
        source
            .pipe(gunzip)
            .pipe(destination)
            .on('finish', resolve)
            .on('error', reject);
    });
}
```

### HTTP Compression
```javascript
const express = require('express');
const compression = require('compression');
const app = express();

// Enable compression
app.use(compression({
    level: 6, // compression level
    threshold: 100 * 1024 // min size to compress (100KB)
}));

// Custom compression filter
app.use(compression({
    filter: (req, res) => {
        if (req.headers['x-no-compression']) {
            return false;
        }
        return compression.filter(req, res);
    }
}));
```

### Memory-Efficient Processing
```javascript
const csv = require('csv-parser');
const fs = require('fs');

// Process large CSV file
fs.createReadStream('large-file.csv')
    .pipe(csv())
    .on('data', (row) => {
        // Process each row
        processRow(row);
    })
    .on('end', () => {
        console.log('CSV processing complete');
    });

// Custom transform for data processing
const { Transform } = require('stream');

class DataProcessor extends Transform {
    constructor(options = {}) {
        super({ ...options, objectMode: true });
    }
    
    _transform(chunk, encoding, callback) {
        // Process data in chunks
        const processed = processData(chunk);
        this.push(processed);
        callback();
    }
}
```

## Best Practices

### 1. Error Handling
```javascript
function handleStream(stream) {
    return new Promise((resolve, reject) => {
        stream
            .on('error', reject)
            .on('end', resolve)
            .on('finish', resolve);
    });
}

// Usage
async function processFile() {
    try {
        const stream = fs.createReadStream('input.txt');
        await handleStream(stream);
        console.log('Processing complete');
    } catch (error) {
        console.error('Stream error:', error);
    }
}
```

### 2. Memory Management
```javascript
const { Transform } = require('stream');

class BatchProcessor extends Transform {
    constructor(options = {}) {
        super({ ...options, objectMode: true });
        this.batch = [];
        this.batchSize = options.batchSize || 1000;
    }
    
    _transform(chunk, encoding, callback) {
        this.batch.push(chunk);
        
        if (this.batch.length >= this.batchSize) {
            this._processBatch();
        }
        
        callback();
    }
    
    _flush(callback) {
        if (this.batch.length > 0) {
            this._processBatch();
        }
        callback();
    }
    
    _processBatch() {
        const result = processBatch(this.batch);
        this.push(result);
        this.batch = [];
    }
}
```

### 3. Performance Optimization
```javascript
const fs = require('fs');
const { pipeline } = require('stream');
const zlib = require('zlib');

// Use pipeline for better error handling
async function compressFile(input, output) {
    const gzip = zlib.createGzip({
        level: zlib.constants.Z_BEST_COMPRESSION,
        memLevel: 9
    });
    
    await pipeline(
        fs.createReadStream(input),
        gzip,
        fs.createWriteStream(output)
    );
}

// Implement backpressure handling
class ThrottledStream extends Transform {
    _transform(chunk, encoding, callback) {
        if (this._isBackpressured()) {
            setTimeout(() => {
                this.push(chunk);
                callback();
            }, 100);
        } else {
            this.push(chunk);
            callback();
        }
    }
    
    _isBackpressured() {
        return !this._readableState.needDrain;
    }
}
```

### 4. Resource Cleanup
```javascript
const { finished } = require('stream');

function cleanup(stream) {
    finished(stream, (error) => {
        if (error) {
            console.error('Stream failed:', error);
        }
        // Cleanup resources
        stream.destroy();
    });
}

// Usage with multiple streams
function processStreams(input, output) {
    const readStream = fs.createReadStream(input);
    const writeStream = fs.createWriteStream(output);
    
    cleanup(readStream);
    cleanup(writeStream);
    
    readStream
        .pipe(transform)
        .pipe(writeStream);
}
```