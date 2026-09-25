# 📦 Module 3: Functions

🟢 **Beginner**

## 3.1 Basic Function Typing

```typescript
function greet(name: string): string {
  return `Hello, ${name}!`;
}

const add = (a: number, b: number): number => a + b;

// void: returns nothing
function logMessage(msg: string): void {
  console.log(msg);
}
```

## 3.2 Optional, Default, and Rest Parameters

```typescript
// Default parameter (TS infers type from default)
function sayHi(name: string, greeting = "Hello"): string {
  return `${greeting}, ${name}`;
}

// Optional parameter — MUST come after required params
function buildUrl(base: string, path?: string): string {
  return path ? `${base}/${path}` : base;
}

// Rest parameters
function sum(...nums: number[]): number {
  return nums.reduce((total, n) => total + n, 0);
}
```

## 3.3 Function Types & Callbacks

```typescript
type MathOperation = (a: number, b: number) => number;
const multiply: MathOperation = (a, b) => a * b;

function fetchUser(id: number, onSuccess: (name: string) => void): void {
  onSuccess("Alice");
}
```

## 3.4 Function Overloads

Define multiple signatures for the same function.

```typescript
function format(value: string): string;
function format(value: number): string;
function format(value: string | number): string {
  if (typeof value === "string") return value.toUpperCase();
  return value.toFixed(2);
}

format("hello"); // "HELLO"
format(3.14159); // "3.14"
```

## 3.5 `void` vs `never`

| | `void` | `never` |
| :--- | :--- | :--- |
| **Meaning** | Returns, but no value | NEVER returns (throws or infinite loop) |
| **Example** | `console.log(...)` | `throw new Error(...)` |

```typescript
function fail(msg: string): never {
  throw new Error(msg); // never returns
}
```

---

## 🛑 Common Mistakes — Module 3

1. Putting optional params before required: `function f(a?: string, b: number)` ❌
2. Confusing `void` (finishes) and `never` (doesn't return at all)

---

## ⚡ Key Takeaways — Module 3

- Type parameters and return values on public APIs
- Optional params (`?`) always at the end; defaults work too
- `void` = returns nothing, `never` = doesn't return at all
- Use overloads when one function handles genuinely different shapes

---

## ✅ Checklist — Module 3

- [ ] I can type function parameters and return values
- [ ] I understand optional, default, and rest parameters
- [ ] I can write and use callback types
- [ ] I know the difference between `void` and `never`
- [ ] I understand function overloads

---
