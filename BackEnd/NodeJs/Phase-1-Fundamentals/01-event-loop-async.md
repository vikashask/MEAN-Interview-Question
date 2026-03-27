# Event Loop & Async Model

## Event Loop Phases

```javascript
// Event loop executes in this order:
// 1. timers (setTimeout, setInterval)
// 2. pending callbacks
// 3. idle, prepare
// 4. poll (I/O events)
// 5. check (setImmediate)
// 6. close callbacks

// Microtasks (run between phases):
// - Promise callbacks
// - queueMicrotask()
// - process.nextTick()
```

## Callbacks

```javascript
// Basic callback
const readFile = (path, callback) => {
  fs.readFile(path, "utf8", (err, data) => {
    if (err) callback(err);
    else callback(null, data);
  });
};

readFile("file.txt", (err, data) => {
  if (err) console.error(err);
  else console.log(data);
});

// Callback hell (avoid)
readFile("file1.txt", (err, data1) => {
  readFile("file2.txt", (err, data2) => {
    readFile("file3.txt", (err, data3) => {
      // Nested callbacks
    });
  });
});
```

## Promises

```javascript
// Creating promises
const promise = new Promise((resolve, reject) => {
  setTimeout(() => resolve("Success"), 1000);
});

promise
  .then((result) => console.log(result))
  .catch((error) => console.error(error))
  .finally(() => console.log("Done"));

// Promise chaining
fs.promises
  .readFile("file1.txt", "utf8")
  .then((data) => fs.promises.readFile("file2.txt", "utf8"))
  .then((data) => console.log(data))
  .catch((err) => console.error(err));

// Promise.all (wait for all)
Promise.all([promise1, promise2, promise3])
  .then(([result1, result2, result3]) => {})
  .catch((err) => console.error(err));

// Promise.race (first to complete)
Promise.race([promise1, promise2]).then((result) => console.log(result));
```

## async/await

```javascript
// Basic async/await
const fetchData = async () => {
  try {
    const data = await fs.promises.readFile("file.txt", "utf8");
    console.log(data);
  } catch (err) {
    console.error(err);
  }
};

// Sequential operations
const processFiles = async () => {
  const file1 = await fs.promises.readFile("file1.txt", "utf8");
  const file2 = await fs.promises.readFile("file2.txt", "utf8");
  return file1 + file2;
};

// Parallel operations
const processFilesParallel = async () => {
  const [file1, file2] = await Promise.all([
    fs.promises.readFile("file1.txt", "utf8"),
    fs.promises.readFile("file2.txt", "utf8"),
  ]);
  return file1 + file2;
};

// Error handling
const safeAsync = async () => {
  try {
    const result = await riskyOperation();
    return [result, null];
  } catch (error) {
    return [null, error];
  }
};

const [data, error] = await safeAsync();
```

## Microtasks vs Macrotasks

```javascript
// Microtasks (higher priority)
// - Promise.then/catch/finally
// - queueMicrotask()
// - process.nextTick()

// Macrotasks (lower priority)
// - setTimeout
// - setInterval
// - setImmediate
// - I/O operations

console.log("1");

setTimeout(() => console.log("2"), 0); // Macrotask

Promise.resolve().then(() => console.log("3")); // Microtask

process.nextTick(() => console.log("4")); // Microtask

console.log("5");

// Output: 1, 5, 4, 3, 2
// Synchronous → nextTick → Promises → setTimeout
```

## process.nextTick vs setImmediate

```javascript
// process.nextTick - runs before I/O events
// setImmediate - runs after I/O events

process.nextTick(() => console.log("nextTick"));
setImmediate(() => console.log("setImmediate"));

// Output: nextTick, setImmediate

// Use cases
// nextTick: defer execution but before I/O
// setImmediate: defer to next iteration of event loop
```

## Non-blocking I/O Pattern

```javascript
// ✅ Non-blocking (correct)
const server = http.createServer((req, res) => {
  fs.readFile("file.txt", "utf8", (err, data) => {
    if (err) res.writeHead(500);
    else res.writeHead(200);
    res.end(data || "Error");
  });
});

// ❌ Blocking (wrong)
const server = http.createServer((req, res) => {
  const data = fs.readFileSync("file.txt", "utf8"); // Blocks!
  res.end(data);
});

// Handling multiple concurrent requests
const server = http.createServer((req, res) => {
  // Each request is handled without blocking others
  fs.readFile(req.url, "utf8", (err, data) => {
    res.end(data || "Not found");
  });
});
```

## Common Patterns

```javascript
// Retry with exponential backoff
const retry = async (fn, maxAttempts = 3, delay = 1000) => {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      return await fn();
    } catch (err) {
      if (i === maxAttempts - 1) throw err;
      await new Promise((resolve) =>
        setTimeout(resolve, delay * Math.pow(2, i))
      );
    }
  }
};

// Timeout wrapper
const withTimeout = (promise, ms) => {
  return Promise.race([
    promise,
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error("Timeout")), ms)
    ),
  ]);
};

// Debounce
const debounce = (fn, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
};
```
