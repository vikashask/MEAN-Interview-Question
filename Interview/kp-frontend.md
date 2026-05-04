# Sequential API Calls in React (Dependent APIs)

## 📌 Problem Statement
Sometimes you need to call multiple APIs where each API depends on the response of the previous one.

Example flow:
- API1 → returns userId
- API2 → uses userId
- API3 → uses orderId
- API4 → uses paymentId

---

## ✅ Basic Approach using async/await

```jsx
import React, { useEffect, useState } from "react";

const MyComponent = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res1 = await fetch("/api/user");
        const user = await res1.json();

        const res2 = await fetch(`/api/orders/${user.id}`);
        const orders = await res2.json();

        const res3 = await fetch(`/api/payment/${orders.orderId}`);
        const payment = await res3.json();

        const res4 = await fetch(`/api/shipping/${payment.paymentId}`);
        const shipping = await res4.json();

        setData(shipping);
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, []);

  return <div>{JSON.stringify(data)}</div>;
};

export default MyComponent;
```

---

## 🧱 Better Architecture (Service Layer)

### apiService.js
```js
export const fetchCompleteFlow = async () => {
  const user = await (await fetch("/api/user")).json();
  const orders = await (await fetch(`/api/orders/${user.id}`)).json();
  const payment = await (await fetch(`/api/payment/${orders.orderId}`)).json();
  return await (await fetch(`/api/shipping/${payment.paymentId}`)).json();
};
```

### Component
```jsx
useEffect(() => {
  fetchCompleteFlow()
    .then(setData)
    .catch(console.error);
}, []);
```

---

## ⚡ Best Practices

- Use async/await instead of nested `.then()`
- Move API logic to service layer
- Handle loading and error states
- Add retry logic for production apps
- Use AbortController to cancel requests on unmount

---

## 🚀 Advanced Option

Use libraries like React Query (TanStack Query) for:
- caching
- retries
- dependent queries
- better state management

---


## ⚠️ Note

If APIs are independent, use parallel execution:

```js
await Promise.all([api1(), api2(), api3()]);
```

---

# ❓ Interview Q&A: Parallel APIs After First API

## Question
How can you call multiple APIs in parallel after the first API response is received in a React component?

---

## ✅ Answer

If the first API provides a common dependency (like `userId`), and the remaining APIs do not depend on each other, you should:

👉 Call the first API  
👉 Then trigger the remaining APIs in parallel using `Promise.all`

---

## 💻 Example

```jsx
import React, { useEffect, useState } from "react";

const MyComponent = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // First API (sequential)
        const res1 = await fetch("/api/user");
        const user = await res1.json();

        // Parallel APIs (independent but depend on userId)
        const [ordersRes, profileRes, settingsRes] = await Promise.all([
          fetch(`/api/orders/${user.id}`),
          fetch(`/api/profile/${user.id}`),
          fetch(`/api/settings/${user.id}`)
        ]);

        const [orders, profile, settings] = await Promise.all([
          ordersRes.json(),
          profileRes.json(),
          settingsRes.json()
        ]);

        setData({ orders, profile, settings });
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, []);

  return <div>{JSON.stringify(data)}</div>;
};

export default MyComponent;
```

---

## ⚡ Key Points

- First API is **sequential**
- Remaining APIs are **parallel**
- Use `Promise.all` for performance optimization
- Reduces total API response time significantly

---

## 🧠 Architect Tip

Use this pattern when:
- APIs share a common dependency
- APIs are independent of each other afterward
- You want to reduce latency in UI rendering

Avoid this pattern when:
- APIs depend on each other's response
- You need strict ordering (then use chaining)
