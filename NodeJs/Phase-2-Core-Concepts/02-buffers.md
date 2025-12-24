# Working with Buffers

## Creating Buffers

```javascript
// Allocate buffer
const buf1 = Buffer.alloc(10); // 10 bytes, filled with 0
const buf2 = Buffer.allocUnsafe(10); // 10 bytes, uninitialized (faster)

// Create from string
const buf3 = Buffer.from("hello"); // Default UTF-8
const buf4 = Buffer.from("hello", "utf8");
const buf5 = Buffer.from("aGVsbG8=", "base64");

// Create from array
const buf6 = Buffer.from([1, 2, 3, 4, 5]);

// Create from another buffer
const buf7 = Buffer.from(buf3);
```

## Buffer Operations

```javascript
// Writing to buffer
const buf = Buffer.alloc(10);
buf.write("hello");
console.log(buf); // <Buffer 68 65 6c 6c 6f 00 00 00 00 00>

// Reading from buffer
console.log(buf.toString()); // 'hello'
console.log(buf.toString("utf8", 0, 5)); // 'hello'
console.log(buf[0]); // 104 (ASCII code for 'h')

// Buffer length
console.log(buf.length); // 10

// Slice buffer
const slice = buf.slice(0, 5);
console.log(slice.toString()); // 'hello'

// Copy buffer
const dest = Buffer.alloc(5);
buf.copy(dest, 0, 0, 5);
console.log(dest.toString()); // 'hello'

// Concatenate buffers
const buf1 = Buffer.from("hello");
const buf2 = Buffer.from("world");
const combined = Buffer.concat([buf1, buf2]);
console.log(combined.toString()); // 'helloworld'

// Compare buffers
const a = Buffer.from("abc");
const b = Buffer.from("abc");
console.log(a.equals(b)); // true

// Fill buffer
const buf3 = Buffer.alloc(5);
buf3.fill("a");
console.log(buf3.toString()); // 'aaaaa'
```

## Encoding & Decoding

```javascript
// Supported encodings
// 'utf8', 'utf16le', 'latin1', 'ascii', 'base64', 'hex'

// UTF-8 (default)
const str = "hello";
const buf = Buffer.from(str, "utf8");
console.log(buf.toString("utf8")); // 'hello'

// Base64
const base64Str = "aGVsbG8=";
const buf2 = Buffer.from(base64Str, "base64");
console.log(buf2.toString()); // 'hello'

// Hex
const hexStr = "68656c6c6f";
const buf3 = Buffer.from(hexStr, "hex");
console.log(buf3.toString()); // 'hello'

// Convert between encodings
const utf8 = Buffer.from("hello", "utf8");
const base64 = utf8.toString("base64");
const hex = utf8.toString("hex");

console.log(base64); // 'aGVsbG8='
console.log(hex); // '68656c6c6f'
```

## Buffer with Streams

```javascript
const fs = require("fs");

// Reading file as buffer
const data = fs.readFileSync("file.txt");
console.log(data); // <Buffer ...>
console.log(data.toString());

// Stream with buffer chunks
const stream = fs.createReadStream("file.txt");

stream.on("data", (chunk) => {
  console.log("Chunk type:", chunk.constructor.name); // Buffer
  console.log("Chunk size:", chunk.length);
  console.log("Chunk content:", chunk.toString());
});

// Control buffer size
const stream2 = fs.createReadStream("file.txt", {
  highWaterMark: 64 * 1024, // 64KB chunks
});
```

## Binary Data Operations

```javascript
// Read/write binary data
const buf = Buffer.alloc(4);
buf.writeUInt32BE(0x12345678, 0); // Big-endian
console.log(buf); // <Buffer 12 34 56 78>

const value = buf.readUInt32BE(0);
console.log(value); // 305419896

// Different integer types
const buf2 = Buffer.alloc(8);
buf2.writeInt8(-1, 0);
buf2.writeUInt8(255, 1);
buf2.writeInt16BE(1000, 2);
buf2.writeUInt32LE(0xffffffff, 4);

// Float operations
const buf3 = Buffer.alloc(8);
buf3.writeFloatBE(3.14, 0);
buf3.writeDoubleBE(3.14159, 4);

const float = buf3.readFloatBE(0);
const double = buf3.readDoubleBE(4);
```

## Common Use Cases

```javascript
// Hashing
const crypto = require("crypto");

const data = Buffer.from("hello");
const hash = crypto.createHash("sha256").update(data).digest("hex");
console.log(hash);

// Encryption
const cipher = crypto.createCipher("aes-256-cbc", "password");
let encrypted = cipher.update(data, "utf8", "hex");
encrypted += cipher.final("hex");

const decipher = crypto.createDecipher("aes-256-cbc", "password");
let decrypted = decipher.update(encrypted, "hex", "utf8");
decrypted += decipher.final("utf8");

// Base64 encoding for transmission
const payload = { id: 1, name: "John" };
const encoded = Buffer.from(JSON.stringify(payload)).toString("base64");
const decoded = JSON.parse(Buffer.from(encoded, "base64").toString());

// File upload handling
const uploadFile = async (fileBuffer) => {
  const fileName = `file-${Date.now()}.bin`;
  await fs.promises.writeFile(fileName, fileBuffer);
};
```

## Memory Management

```javascript
// Check buffer memory
console.log(Buffer.byteLength("hello")); // 5
console.log(Buffer.byteLength("你好")); // 6 (multi-byte UTF-8)

// Large buffer handling
const largeBuffer = Buffer.alloc(1024 * 1024 * 100); // 100MB
console.log(process.memoryUsage().heapUsed);

// Clear buffer reference
let buf = Buffer.alloc(1024 * 1024);
buf = null; // Allow garbage collection

// Buffer pooling (for performance)
const pool = Buffer.allocUnsafe(10);
// Reuse pool instead of allocating new buffers
```
