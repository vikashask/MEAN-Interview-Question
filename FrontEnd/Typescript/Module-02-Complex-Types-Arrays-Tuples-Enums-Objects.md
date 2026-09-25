# 📦 Module 2: Complex Types (Arrays, Tuples, Enums, Objects)

🟢 **Beginner**

## 2.1 Arrays

```typescript
let scores: number[] = [90, 85, 100];
let names: Array<string> = ["Alice", "Bob"]; // Generic syntax

// scores.push("A"); // ❌ ERROR
let mixed: (string | number)[] = ["Alice", 100];

// Readonly arrays — prevents mutation
const readonlyScores: readonly number[] = [1, 2, 3];
// readonlyScores.push(4); // ❌ ERROR
```

## 2.2 Tuples

Fixed-length, fixed-type arrays. **Order strictly matters.**

```typescript
let userRecord: [number, string] = [1, "Alice"];

// Named tuples (TypeScript 4.0+)
let coordinate: [x: number, y: number] = [10, 20];

// Optional tuple elements
let withOptional: [string, number?] = ["Bob"];

// ⚠️ Gotcha: .push() bypasses tuple length checks at runtime
userRecord.push("extra"); // TS allows this (design limitation)
```

**When to use:** Fixed pairs like `[lat, lng]`, React's `[value, setter]`.

## 2.3 Enums

**Always prefer String Enums for clarity.**

```typescript
// Numeric Enum (auto-increments — avoid)
enum Direction { Up, Down, Left, Right }

// String Enum (explicit values — recommended ✅)
enum Status {
  Active = "ACTIVE",
  Inactive = "INACTIVE",
  Pending = "PENDING"
}

// Const Enum (erased at compile time — best performance)
const enum HttpMethod { Get = "GET", Post = "POST", Delete = "DELETE" }
```

| | Numeric | String |
| :--- | :--- | :--- |
| **Debugging** | Confusing (logs `0`, `1`) | Clear (logs `"ACTIVE"`) |
| **Recommended** | ❌ Avoid | ✅ Prefer |

## 2.4 Objects

```typescript
let user: { name: string; age: number; isAdmin?: boolean } = {
  name: "Bob",
  age: 30
  // isAdmin is optional — valid to omit
};

// Readonly properties
let config: { readonly apiUrl: string } = { apiUrl: "https://api.example.com" };
// config.apiUrl = "other"; // ❌ ERROR
```

---

## ⚡ Key Takeaways — Module 2

- `type[]` for arrays, `[t1, t2]` for tuples (fixed-length, fixed-type)
- Use String Enums for readability, `const enum` for performance
- `?` = optional property, `readonly` = immutable property

---

## ✅ Checklist — Module 2

- [ ] I can type arrays with `type[]` and `Array<type>`
- [ ] I understand tuples and when to use them
- [ ] I prefer String Enums over Numeric Enums
- [ ] I can use `?` for optional and `readonly` for immutable properties

---
