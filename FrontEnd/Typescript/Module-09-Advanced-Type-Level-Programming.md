# 📦 Module 9: Advanced Type-Level Programming

🔴 **Advanced**

## 9.1 Conditional Types

Like a ternary operator for types.

```typescript
type IsString<T> = T extends string ? "yes" : "no";

type A = IsString<string>;  // "yes"
type B = IsString<number>;  // "no"
```

### `infer` — Extracting Inner Types

```typescript
// Extract return type manually (like ReturnType)
type GetReturn<T> = T extends (...args: any[]) => infer R ? R : never;
type Result = GetReturn<(x: number) => string>; // string
```

## 9.2 Mapped Types

Transform every property in a type systematically.

```typescript
// Manual Partial
type MyPartial<T> = { [K in keyof T]?: T[K]; };

// All values nullable
type Nullable<T> = { [K in keyof T]: T[K] | null; };

// Remap keys
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
```

## 9.3 Template Literal Types

```typescript
type EventName = "click" | "focus" | "blur";
type Handler = `on${Capitalize<EventName>}`;
// "onClick" | "onFocus" | "onBlur"

type HttpMethod = "get" | "post" | "delete";
type Endpoint = "/users" | "/products";
type Route = `${Uppercase<HttpMethod>} ${Endpoint}`;
// "GET /users" | "GET /products" | "POST /users" | ...
```

## 9.4 Recursive Types

```typescript
type JSONValue =
  | string | number | boolean | null
  | JSONValue[]
  | { [key: string]: JSONValue };

type TreeNode<T> = {
  value: T;
  children: TreeNode<T>[];
};
```

## 9.5 `satisfies` Operator (TypeScript 4.9+)

Validates a value matches a type **without widening** the inferred type.

```typescript
type Config = Record<string, string | number>;

const config = {
  port: 3000,
  host: "localhost"
} satisfies Config;

config.port.toFixed(2); // ✅ still inferred as number, not string | number
```

---

## ⚡ Key Takeaways — Module 9

- **Conditional types:** `T extends U ? X : Y` — types as logic
- **`infer`:** Extract a type from within a conditional type
- **Mapped types:** `[K in keyof T]: ...` — transform all properties
- **Template literal types:** Build string patterns as types
- **Recursive types:** Types that reference themselves
- **`satisfies`:** Validate type without widening inference

---

## ✅ Checklist — Module 9

- [ ] I understand conditional types
- [ ] I understand what `infer` does
- [ ] I can write mapped types
- [ ] I understand template literal types
- [ ] I can write recursive types
- [ ] I know when to use `satisfies`

---
