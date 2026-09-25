# 📦 Module 11: Async TypeScript

🟡 **Intermediate**

## 11.1 Typing Promises

```typescript
function wait(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function fetchUser(id: number): Promise<{ id: number; name: string }> {
  return fetch(`/api/users/${id}`).then(res => res.json());
}
```

## 11.2 `async`/`await`

```typescript
interface User { id: number; name: string; email: string; }

async function getUser(id: number): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error(`HTTP error: ${res.status}`);
  return res.json() as Promise<User>;
}
```

## 11.3 Error Handling in Async Code

```typescript
async function loadData(): Promise<void> {
  try {
    const user = await getUser(1);
    console.log(user.name);
  } catch (error) {
    // error is 'unknown' in strict mode — must narrow
    if (error instanceof Error) {
      console.error(error.message);
    }
  }
}
```

## 11.4 Result Pattern

Functional error handling — avoids thrown exceptions.

```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function safeGetUser(id: number): Promise<Result<User>> {
  try {
    const user = await getUser(id);
    return { ok: true, value: user };
  } catch (e) {
    return { ok: false, error: e instanceof Error ? e : new Error(String(e)) };
  }
}

const result = await safeGetUser(1);
if (result.ok) {
  console.log(result.value.name); // ✅
} else {
  console.error(result.error.message); // ✅
}
```

## 11.5 `Promise.all` and `Promise.allSettled`

```typescript
// Types inferred as a tuple
const [users, products] = await Promise.all([fetchUsers(), fetchProducts()]);
// users: User[], products: Product[]

// allSettled never throws — check status per item
const results = await Promise.allSettled([fetchUsers(), fetchProducts()]);
results.forEach(r => {
  if (r.status === "fulfilled") console.log(r.value);
  else console.error(r.reason);
});
```

---

## ⚡ Key Takeaways — Module 11

- Async functions return `Promise<T>` — always annotate T
- `catch` blocks receive `unknown` — narrow with `instanceof Error`
- Result pattern avoids thrown exceptions elegantly
- `Promise.all` infers tuple types from multiple Promises

---

## ✅ Checklist — Module 11

- [ ] I can type `Promise<T>` return values
- [ ] I write typed `async/await` functions
- [ ] I handle errors correctly with `instanceof Error`
- [ ] I understand `Promise.all` and `Promise.allSettled`
- [ ] I know the Result pattern

---
