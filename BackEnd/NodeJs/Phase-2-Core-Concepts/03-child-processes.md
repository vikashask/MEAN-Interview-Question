# Process & Child Processes

## Child Process Methods

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

child.on("error", (err) => {
  console.error("Failed to start process:", err);
});

// exec - shell command, buffers output (max 200KB)
exec("ls -la", (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error.message}`);
    return;
  }
  console.log(`Output:\n${stdout}`);
});

// execFile - execute file, more secure (no shell)
execFile("node", ["script.js", "arg1"], (error, stdout, stderr) => {
  if (error) console.error(error);
  console.log(stdout);
});

// fork - spawn Node.js process with IPC
const child = fork("worker.js");

child.send({ msg: "Hello from parent" });

child.on("message", (msg) => {
  console.log("Message from child:", msg);
});

child.on("error", (err) => {
  console.error("Child error:", err);
});

child.on("exit", (code, signal) => {
  console.log(`Child exited with code ${code}`);
});
```

## Inter-Process Communication (IPC)

```javascript
// parent.js
const { fork } = require("child_process");

const child = fork("worker.js");

// Send message to child
child.send({ type: "START", data: [1, 2, 3] });

// Receive message from child
child.on("message", (msg) => {
  if (msg.type === "RESULT") {
    console.log("Result:", msg.data);
  }
});

// worker.js
process.on("message", (msg) => {
  if (msg.type === "START") {
    const result = msg.data.reduce((a, b) => a + b, 0);
    process.send({ type: "RESULT", data: result });
  }
});

// Disconnect
child.disconnect();
```

## Spawning Processes

```javascript
// Long-running process
const child = spawn("node", ["server.js"]);

// Pipe output
child.stdout.pipe(process.stdout);
child.stderr.pipe(process.stderr);

// Send signal
setTimeout(() => {
  child.kill("SIGTERM"); // Graceful shutdown
}, 5000);

// Detached process (runs independently)
const detached = spawn("node", ["background-task.js"], {
  detached: true,
  stdio: "ignore",
});

detached.unref(); // Allow parent to exit

// With environment variables
const child2 = spawn("node", ["script.js"], {
  env: { ...process.env, NODE_ENV: "production" },
});

// With working directory
const child3 = spawn("npm", ["start"], {
  cwd: "/home/user/project",
});
```

## Process Management

```javascript
// Cluster for multi-core
const cluster = require("cluster");
const os = require("os");
const http = require("http");

if (cluster.isMaster) {
  const numCPUs = os.cpus().length;

  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  // Handle worker exit
  cluster.on("exit", (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`);
    cluster.fork(); // Restart worker
  });
} else {
  // Worker process
  http
    .createServer((req, res) => {
      res.writeHead(200);
      res.end("Hello from worker " + process.pid);
    })
    .listen(3000);
}

// Worker communication
cluster.on("message", (worker, message) => {
  console.log(`Message from worker ${worker.id}:`, message);
});

// Send message to worker
for (const id in cluster.workers) {
  cluster.workers[id].send({ cmd: "shutdown" });
}
```

## Signal Handling

```javascript
// Handle signals
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

process.on("SIGHUP", () => {
  console.log("SIGHUP received, reloading config");
  // Reload configuration
});

// Send signal to child
child.kill("SIGTERM");
child.kill("SIGKILL"); // Force kill

// Check if process is running
if (!child.killed) {
  console.log("Process is still running");
}
```

## Process Monitoring

```javascript
// Monitor child process
const { spawn } = require("child_process");

const startWorker = () => {
  const worker = spawn("node", ["worker.js"]);

  worker.on("exit", (code, signal) => {
    if (code !== 0 && !worker.killed) {
      console.log("Worker crashed, restarting...");
      setTimeout(startWorker, 1000);
    }
  });

  return worker;
};

let worker = startWorker();

// Graceful shutdown
process.on("SIGTERM", () => {
  worker.kill("SIGTERM");
  setTimeout(() => {
    if (!worker.killed) {
      worker.kill("SIGKILL");
    }
    process.exit(0);
  }, 5000);
});
```

## Common Patterns

```javascript
// Run command and get output
const runCommand = (command, args = []) => {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args);
    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    child.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    child.on("close", (code) => {
      if (code === 0) {
        resolve(stdout);
      } else {
        reject(new Error(stderr));
      }
    });
  });
};

const output = await runCommand("ls", ["-la"]);

// Timeout for child process
const runWithTimeout = (command, args, timeout = 5000) => {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args);
    const timer = setTimeout(() => {
      child.kill();
      reject(new Error("Process timeout"));
    }, timeout);

    let stdout = "";
    child.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    child.on("close", () => {
      clearTimeout(timer);
      resolve(stdout);
    });
  });
};
```
