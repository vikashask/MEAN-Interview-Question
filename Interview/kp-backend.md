# Backend (Node.js) – API Orchestration Interview Q&A

---

## ❓ Question 1

How do you call multiple APIs sequentially (dependent APIs) in Node.js?

### ✅ Answer

When each API depends on the previous API’s response, use `async/await` to chain them sequentially.

### 💻 Example (Express Route)

```js
const express = require("express");
const fetch = require("node-fetch");

const app = express();

app.get("/sequential-flow", async (req, res) => {
  try {
    // API 1
    const userRes = await fetch("http://service-a/api/user");
    const user = await userRes.json();

    // API 2 (depends on user.id)
    const ordersRes = await fetch(`http://service-b/api/orders/${user.id}`);
    const orders = await ordersRes.json();

    // API 3 (depends on orders.orderId)
    const paymentRes = await fetch(
      `http://service-c/api/payment/${orders.orderId}`,
    );
    const payment = await paymentRes.json();

    // API 4 (depends on payment.paymentId)
    const shippingRes = await fetch(
      `http://service-d/api/shipping/${payment.paymentId}`,
    );
    const shipping = await shippingRes.json();

    res.json({ user, orders, payment, shipping });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Sequential flow failed" });
  }
});

module.exports = app;
```

### ⚡ Key Points

- Uses `async/await` for readability
- Ensures strict order of execution
- Best for **dependent microservice calls**

---

## ❓ Question 2

How do you call multiple APIs in parallel after the first API in Node.js?

### ✅ Answer

Call the first API to get a common dependency (e.g., `userId`), then trigger the remaining APIs in parallel using `Promise.all`.

### 💻 Example (Express Route)

```js
const express = require("express");
const fetch = require("node-fetch");

const app = express();

app.get("/parallel-after-first", async (req, res) => {
  try {
    // First API (sequential)
    const userRes = await fetch("http://service-a/api/user");
    const user = await userRes.json();

    // Parallel APIs (independent but depend on user.id)
    const [ordersRes, profileRes, settingsRes] = await Promise.all([
      fetch(`http://service-b/api/orders/${user.id}`),
      fetch(`http://service-c/api/profile/${user.id}`),
      fetch(`http://service-d/api/settings/${user.id}`),
    ]);

    const [orders, profile, settings] = await Promise.all([
      ordersRes.json(),
      profileRes.json(),
      settingsRes.json(),
    ]);

    res.json({ user, orders, profile, settings });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Parallel flow failed" });
  }
});

module.exports = app;
```

### ⚡ Key Points

- First call is **sequential**
- Remaining calls are **parallel**
- Reduces total latency significantly
- Ideal for **microservices aggregation layer (BFF / API Gateway)**

---

## 🧠 Advanced Tips (Backend Architect Level)

- Use `Promise.allSettled` when partial failures are acceptable
- Add retries (e.g., exponential backoff) for flaky downstream services
- Implement timeouts to avoid hanging requests
- Use circuit breakers for resilience (e.g., `opossum`)
- Log correlation IDs for tracing across services
- Consider moving orchestration to a dedicated service (BFF)

### 💻 Example (Partial Failure Handling)

```js
const results = await Promise.allSettled([
  fetch(url1),
  fetch(url2),
  fetch(url3),
]);

const parsed = await Promise.all(
  results.map(async (r) => (r.status === "fulfilled" ? r.value.json() : null)),
);
```

## ❓ Question 3 : how octa worked end to end in details

## ❓ Question 4 : how to monitor inftra and backend api
