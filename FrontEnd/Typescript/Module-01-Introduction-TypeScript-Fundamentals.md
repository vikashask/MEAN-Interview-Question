# 📦 Module 1: Introduction & TypeScript Fundamentals

🟢 **Beginner**

## 1.1 What is TypeScript and Why Use It?

**Concept:** TypeScript (TS) is a syntactic **superset** of JavaScript (JS) that adds **static typing**.
- **JavaScript** is dynamically typed — types are checked at *runtime*. Bugs crash live apps.
- **TypeScript** is statically typed — types are checked at *compile time*. Bugs are caught in your editor.

### JS vs TS Comparison

| Feature | JavaScript | TypeScript |
| :--- | :--- | :--- |
| **Type Checking** | Dynamic (Runtime) | Static (Compile time) |
| **Browser Execution** | Runs directly | Must be compiled to JS first |
| **Tooling / Autocomplete** | Basic | Excellent |
| **Error Discovery** | User finds bugs | Editor finds bugs |

## 1.2 The Compiler

TypeScript does **not** run in browsers or Node.js directly. The `tsc` compiler reads `.ts` files, strips types, and outputs `.js` files.

```bash
npm install -g typescript   # Install
tsc --version               # Verify
tsc index.ts                # Compile one file
tsc --init                  # Create tsconfig.json
```

## 1.3 Core Primitive Types

```typescript
// string
let firstName: string = "Alice";
let greeting: string = `Hello, ${firstName}`;

// number (integers, floats, hex, binary, octal)
let age: number = 25;
let price: number = 19.99;

// boolean
let isActive: boolean = true;

// null and undefined
let emptyValue: null = null;
let notAssigned: undefined = undefined;

// any — turns off all type checking (AVOID)
let anything: any = 42;
anything = "string now"; // TS allows this — dangerous!
```

## 1.4 Type Inference

TypeScript automatically infers types from values. **Only annotate explicitly when necessary.**

```typescript
let city = "New York";   // inferred: string
let score = 0;           // inferred: number
// city = 100;           // ERROR: number not assignable to string

// Explicit annotation needed when declaring without a value:
let loggedInUser: string;
loggedInUser = "Bob"; // OK
```

## 1.5 `any` vs `unknown`

| | `any` | `unknown` |
| :--- | :--- | :--- |
| **Safety** | ❌ Disables type checking | ✅ Forces type checking before use |
| **Use when** | Migrating old JS code | You don't know the type yet |

```typescript
let val: unknown = "hello";
// val.toUpperCase(); // ERROR: must narrow first
if (typeof val === "string") {
  val.toUpperCase(); // OK ✅
}
```

---

## 🛑 Common Mistakes — Module 1

1. **Over-annotating inferred types:** `let name: string = "John"` → just write `let name = "John"`.
2. **Using capitalized wrapper types:** `String`, `Number`, `Boolean` are JavaScript object wrappers — always use lowercase.
3. **Using `any` to silence errors** — use `unknown` instead and narrow properly.

---

## ⚡ Key Takeaways — Module 1

- TypeScript = JavaScript + Static Types, compiled to JS before running.
- Use lowercase primitives: `string`, `number`, `boolean`.
- Let TS infer types; annotate only when declaring without a value.
- Prefer `unknown` over `any`.

---

## ✅ Checklist — Module 1

- [ ] I understand TS compiles to JS
- [ ] I can declare primitive types
- [ ] I understand type inference
- [ ] I know why `any` is dangerous and `unknown` is safer
- [ ] I know to use lowercase `string`, not `String`

---
