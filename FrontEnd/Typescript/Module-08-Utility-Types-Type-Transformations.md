# 📦 Module 8: Utility Types (Type Transformations)

🔴 **Advanced**

TypeScript's built-in utilities transform existing types into new shapes.

## 8.1 `Partial<T>` and `Required<T>`

```typescript
interface User { id: number; name: string; email: string; }

type PartialUser = Partial<User>;
// { id?: number; name?: string; email?: string; }

type RequiredUser = Required<Partial<User>>;
// All props required again

// Use case: update functions
function updateUser(id: number, changes: Partial<User>) { /* ... */ }
```

## 8.2 `Readonly<T>`, `Pick<T, K>`, `Omit<T, K>`

```typescript
type ReadonlyUser = Readonly<User>;
// const u: ReadonlyUser; u.name = "x"; // ❌ ERROR

type UserPreview = Pick<User, "id" | "name">;
// { id: number; name: string }

type UserWithoutEmail = Omit<User, "email">;
// { id: number; name: string }
```

## 8.3 `Record<K, V>`

```typescript
type Role = "admin" | "user" | "guest";
type Permissions = Record<Role, string[]>;

const permissions: Permissions = {
  admin: ["read", "write", "delete"],
  user:  ["read", "write"],
  guest: ["read"]
};
```

## 8.4 `Exclude<T, U>`, `Extract<T, U>`, `NonNullable<T>`

```typescript
type AllEvents = "click" | "hover" | "focus" | "blur";

type MouseOnly = Exclude<AllEvents, "focus" | "blur">; // "click" | "hover"
type Common    = Extract<AllEvents, "click" | "hover">; // "click" | "hover"

type MaybeString = string | null | undefined;
type DefiniteString = NonNullable<MaybeString>; // string
```

## 8.5 `ReturnType<T>`, `Parameters<T>`, `Awaited<T>`

```typescript
function createUser(name: string, age: number) {
  return { id: Date.now(), name, age };
}

type CreatedUser    = ReturnType<typeof createUser>;
// { id: number; name: string; age: number }

type CreateParams   = Parameters<typeof createUser>;
// [name: string, age: number]

async function fetchData(): Promise<{ id: number }> { return { id: 1 }; }
type FetchResult    = Awaited<ReturnType<typeof fetchData>>;
// { id: number }
```

---

## ⚡ Quick Reference — Module 8

| Utility | What it does |
| :--- | :--- |
| `Partial<T>` | All props optional |
| `Required<T>` | All props required |
| `Readonly<T>` | All props readonly |
| `Pick<T, K>` | Keep only K keys |
| `Omit<T, K>` | Remove K keys |
| `Record<K, V>` | Map K keys to V values |
| `Exclude<T, U>` | Remove U from union T |
| `Extract<T, U>` | Keep overlap of T and U |
| `NonNullable<T>` | Remove null/undefined |
| `ReturnType<T>` | Get return type of function |
| `Parameters<T>` | Get params as tuple |
| `Awaited<T>` | Unwrap Promise type |

---

## ✅ Checklist — Module 8

- [ ] I know when to use `Partial` vs `Required`
- [ ] I can `Pick` and `Omit` properties from a type
- [ ] I can use `Record` to build mapped object types
- [ ] I understand `Exclude`, `Extract`, and `NonNullable`
- [ ] I can use `ReturnType` and `Parameters`

---
