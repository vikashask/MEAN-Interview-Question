# Global Objects & Process

## Global Objects

```javascript
// global - root namespace
global.myVar = "accessible everywhere";
console.log(global.myVar);

// __dirname - current directory path
console.log(__dirname); // /home/user/project

// __filename - current file path
console.log(__filename); // /home/user/project/index.js

// Buffer - binary data
const buf = Buffer.from("hello");

// console - logging
console.log("log");
console.error("error");
console.warn("warning");
console.table([{ id: 1, name: "John" }]);

// Timers
setTimeout(() => {}, 1000);
setInterval(() => {}, 1000);
setImmediate(() => {});

// URL and URLSearchParams
const url = new URL("https://example.com/path?key=value");
console.log(url.hostname); // example.com
console.log(url.searchParams.get("key")); // value
```

## process Object

```javascript
// Process information
console.log(process.pid); // Process ID
console.log(process.version); // Node.js version
console.log(process.versions); // Dependencies versions
console.log(process.platform); // 'linux', 'darwin', 'win32'
console.log(process.arch); // 'x64', 'arm64'
console.log(process.cwd()); // Current working directory
console.log(process.env); // Environment variables
console.log(process.argv); // Command line arguments

// Change directory
process.chdir("/home/user");

// Exit process
process.exit(0); // Exit with code 0 (success)
process.exit(1); // Exit with code 1 (error)

// Uptime
console.log(process.uptime()); // Seconds since process started

// Memory usage
const mem = process.memoryUsage();
console.log(mem.heapUsed); // Used heap memory
console.log(mem.heapTotal); // Total heap memory
```

## Environment Variables

```javascript
// Access environment variables
const apiKey = process.env.API_KEY;
const port = process.env.PORT || 3000;
const nodeEnv = process.env.NODE_ENV || "development";

// Set environment variables
process.env.MY_VAR = "value";

// .env file (using dotenv)
require("dotenv").config();
const dbUrl = process.env.DATABASE_URL;
```

## Command Line Arguments

```javascript
// process.argv - array of command line arguments
// argv[0] = node executable path
// argv[1] = script path
// argv[2+] = arguments

// node script.js arg1 arg2
console.log(process.argv);
// ['node', 'script.js', 'arg1', 'arg2']

// Parse arguments manually
const args = process.argv.slice(2);
console.log(args); // ['arg1', 'arg2']

// Using yargs for parsing
const yargs = require("yargs/yargs");
const argv = yargs(process.argv.slice(2))
  .option("port", { alias: "p", type: "number", default: 3000 })
  .option("host", { alias: "h", type: "string", default: "localhost" }).argv;

console.log(argv.port); // 3000
console.log(argv.host); // localhost
```

## Signal Handling

```javascript
// Handle termination signals
process.on("SIGTERM", () => {
  console.log("SIGTERM received, shutting down gracefully");
  server.close(() => {
    process.exit(0);
  });
});

process.on("SIGINT", () => {
  console.log("SIGINT received (Ctrl+C)");
  process.exit(0);
});

// Handle uncaught exceptions
process.on("uncaughtException", (err) => {
  console.error("Uncaught Exception:", err);
  process.exit(1);
});

// Handle unhandled promise rejections
process.on("unhandledRejection", (reason, promise) => {
  console.error("Unhandled Rejection at:", promise, "reason:", reason);
  process.exit(1);
});

// Graceful shutdown
const gracefulShutdown = async () => {
  console.log("Shutting down gracefully...");
  await closeDatabase();
  await closeServer();
  process.exit(0);
};

process.on("SIGTERM", gracefulShutdown);
process.on("SIGINT", gracefulShutdown);
```

## Child Processes

```javascript
const { spawn, exec, execFile, fork } = require("child_process");

// spawn - stream-based, for large outputs
const child = spawn("ls", ["-la"]);

child.stdout.on("data", (data) => {
  console.log(`stdout: ${data}`);
});

child.stderr.on("data", (data) => {
  console.error(`stderr: ${data}`);
});

child.on("close", (code) => {
  console.log(`Process exited with code ${code}`);
});

// exec - shell command, buffers output
exec("ls -la", (error, stdout, stderr) => {
  if (error) console.error(error);
  console.log(stdout);
});

// execFile - execute file, more secure
execFile("node", ["script.js"], (error, stdout, stderr) => {
  if (error) console.error(error);
  console.log(stdout);
});

// fork - spawn Node.js process, IPC communication
const child = fork("worker.js");

child.send({ msg: "Hello from parent" });

child.on("message", (msg) => {
  console.log("Message from child:", msg);
});

// worker.js
process.on("message", (msg) => {
  console.log("Message from parent:", msg);
  process.send({ msg: "Hello from child" });
});
```

## Performance Monitoring

```javascript
// Measure execution time
const start = process.hrtime.bigint();
// ... operation ...
const end = process.hrtime.bigint();
const duration = Number(end - start) / 1e6; // Convert to ms
console.log(`Took ${duration}ms`);

// Memory monitoring
setInterval(() => {
  const mem = process.memoryUsage();
  console.log(`Memory: ${Math.round(mem.heapUsed / 1024 / 1024)}MB`);
}, 5000);

// CPU usage (approximate)
const v8 = require("v8");
const heapStats = v8.getHeapStatistics();
console.log(heapStats);
```
