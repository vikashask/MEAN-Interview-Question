# File System & Streams

## File System Operations

```javascript
const fs = require("fs");
const path = require("path");

// Synchronous (blocking - avoid in production)
const data = fs.readFileSync("file.txt", "utf8");
fs.writeFileSync("file.txt", "content");
fs.appendFileSync("file.txt", "more content");

// Asynchronous callbacks
fs.readFile("file.txt", "utf8", (err, data) => {
  if (err) console.error(err);
  else console.log(data);
});

fs.writeFile("file.txt", "content", (err) => {
  if (err) console.error(err);
  else console.log("Written");
});

// Promises (fs.promises)
const data = await fs.promises.readFile("file.txt", "utf8");
await fs.promises.writeFile("file.txt", "content");
await fs.promises.appendFile("file.txt", "more");

// Directory operations
fs.mkdir("newdir", (err) => {});
fs.rmdir("newdir", (err) => {});
fs.readdir("path", (err, files) => {});
fs.stat("file.txt", (err, stats) => {});

// File info
const stats = fs.statSync("file.txt");
console.log(stats.isFile()); // true/false
console.log(stats.isDirectory()); // true/false
console.log(stats.size); // bytes
console.log(stats.mtime); // modified time
```

## Streams

```javascript
// Readable Stream
const readStream = fs.createReadStream("input.txt", {
  encoding: "utf8",
  highWaterMark: 64 * 1024, // 64KB chunks
});

readStream.on("data", (chunk) => {
  console.log("Chunk:", chunk.length);
});

readStream.on("end", () => {
  console.log("Finished reading");
});

readStream.on("error", (err) => {
  console.error("Error:", err);
});

// Writable Stream
const writeStream = fs.createWriteStream("output.txt");

writeStream.write("Hello ");
writeStream.write("World");
writeStream.end(); // Signal end

writeStream.on("finish", () => {
  console.log("Finished writing");
});

// Pipe (connect streams)
fs.createReadStream("input.txt").pipe(fs.createWriteStream("output.txt"));

// Transform Stream
const { Transform } = require("stream");

const uppercase = new Transform({
  transform(chunk, encoding, callback) {
    this.push(chunk.toString().toUpperCase());
    callback();
  },
});

fs.createReadStream("input.txt")
  .pipe(uppercase)
  .pipe(fs.createWriteStream("output.txt"));
```

## Buffers

```javascript
// Creating buffers
const buf1 = Buffer.alloc(10); // 10 bytes, zeroed
const buf2 = Buffer.allocUnsafe(10); // 10 bytes, uninitialized
const buf3 = Buffer.from("hello"); // From string
const buf4 = Buffer.from([1, 2, 3]); // From array

// Writing to buffer
const buf = Buffer.alloc(10);
buf.write("hello");
console.log(buf); // <Buffer 68 65 6c 6c 6f 00 00 00 00 00>

// Reading from buffer
console.log(buf.toString()); // 'hello'
console.log(buf.toString("utf8", 0, 5)); // 'hello'

// Buffer operations
const buf1 = Buffer.from("hello");
const buf2 = Buffer.from("world");
const combined = Buffer.concat([buf1, buf2]);
console.log(combined.toString()); // 'helloworld'

// Encoding/Decoding
const str = "hello";
const utf8 = Buffer.from(str, "utf8");
const base64 = utf8.toString("base64");
const decoded = Buffer.from(base64, "base64").toString("utf8");
```

## Path Operations

```javascript
const path = require("path");

// Path parsing
const filePath = "/home/user/documents/file.txt";
console.log(path.dirname(filePath)); // /home/user/documents
console.log(path.basename(filePath)); // file.txt
console.log(path.extname(filePath)); // .txt
console.log(path.parse(filePath)); // { root, dir, base, name, ext }

// Path joining
const fullPath = path.join("/home", "user", "documents", "file.txt");
const resolved = path.resolve("documents", "file.txt");

// Relative paths
const rel = path.relative("/home/user", "/home/user/documents/file.txt");
console.log(rel); // documents/file.txt

// Check if absolute
console.log(path.isAbsolute("/home/user")); // true
console.log(path.isAbsolute("documents")); // false
```

## Watching Files

```javascript
// Watch for changes
fs.watch("file.txt", (eventType, filename) => {
  console.log(`${filename} changed: ${eventType}`);
});

// Watch directory
fs.watch("directory", { recursive: true }, (eventType, filename) => {
  console.log(`${filename} changed`);
});

// Watchfile (less efficient)
fs.watchFile("file.txt", (curr, prev) => {
  if (curr.mtime > prev.mtime) {
    console.log("File changed");
  }
});
```

## Common Patterns

```javascript
// Copy file
const copy = async (src, dest) => {
  await fs.promises.copyFile(src, dest);
};

// Delete file
const deleteFile = async (filePath) => {
  await fs.promises.unlink(filePath);
};

// Recursive directory deletion
const deleteDir = async (dirPath) => {
  const files = await fs.promises.readdir(dirPath);
  for (const file of files) {
    const filePath = path.join(dirPath, file);
    const stat = await fs.promises.stat(filePath);
    if (stat.isDirectory()) {
      await deleteDir(filePath);
    } else {
      await fs.promises.unlink(filePath);
    }
  }
  await fs.promises.rmdir(dirPath);
};

// Read large file line by line
const readline = require("readline");
const rl = readline.createInterface({
  input: fs.createReadStream("large-file.txt"),
});

rl.on("line", (line) => {
  console.log(line);
});

rl.on("close", () => {
  console.log("Finished");
});
```
