# 📦 Module 5: Type Narrowing & Guards

🟡 **Intermediate**

## 5.1 What is Narrowing?

When a value has a union type, TS won't let you use type-specific methods until you **prove** which type it is.

```typescript
function describe(value: string | number) {
  if (typeof value === "number") {
    console.log(value.toFixed(2)); // TS knows: number
  } else {
    console.log(value.toUpperCase()); // TS knows: string
  }
}
```

## 5.2 Narrowing Techniques

```typescript
// typeof — for primitives
if (typeof input === "string") { /* string */ }

// instanceof — for class instances
if (error instanceof Error) { console.log(error.message); }

// in — for object properties
type Fish = { swim: () => void };
type Bird = { fly: () => void };
function move(animal: Fish | Bird) {
  if ("swim" in animal) { animal.swim(); } // TS knows: Fish
  else { animal.fly(); }                   // TS knows: Bird
}

// Truthiness guard
function printName(name: string | null) {
  if (name) { console.log(name.toUpperCase()); }
}
```

## 5.3 Discriminated Unions (Most Important Pattern!)

Add a shared literal property so TS can narrow via `switch`.

```typescript
interface LoadingState { status: "loading" }
interface SuccessState { status: "success"; data: string[] }
interface ErrorState   { status: "error"; message: string }

type AppState = LoadingState | SuccessState | ErrorState;

function render(state: AppState) {
  switch (state.status) {
    case "loading": console.log("Loading..."); break;
    case "success": console.log(state.data); break;   // data available ✅
    case "error":   console.log(state.message); break; // message available ✅
  }
}
```

## 5.4 Type Assertions (`as`) and Non-null Assertion (`!`)

```typescript
// as: tell TS "I know the type" (overrides compiler — use sparingly)
const input = document.getElementById("name") as HTMLInputElement;
console.log(input.value);

// !: tell TS "this is definitely not null"
const canvas = document.getElementById("canvas")!;
```

## 5.5 User-defined Type Guards

```typescript
interface Cat { meow(): void }
interface Dog { bark(): void }

function isCat(animal: Cat | Dog): animal is Cat {
  return (animal as Cat).meow !== undefined;
}

function interact(animal: Cat | Dog) {
  if (isCat(animal)) { animal.meow(); } // TS knows: Cat ✅
  else { animal.bark(); }
}
```

---

## 🛑 Common Mistakes — Module 5

1. Overusing `as` — assertions bypass safety. Prefer narrowing.
2. Forgetting `unknown` requires narrowing before use.
3. Not using discriminated unions for complex state.

---

## ⚡ Key Takeaways — Module 5

- Narrowing proves which type a value is before using type-specific features
- Use `typeof`, `instanceof`, `in` for narrowing
- Discriminated unions are the most scalable narrowing pattern
- `as` bypasses type checking — prefer narrowing. `x!` removes nullability — use carefully

---

## ✅ Checklist — Module 5

- [ ] I understand why narrowing is needed
- [ ] I can use `typeof`, `instanceof`, and `in` guards
- [ ] I understand and can build discriminated unions
- [ ] I know when to use `as` vs proper narrowing
- [ ] I can write a user-defined type guard with `is`

---
