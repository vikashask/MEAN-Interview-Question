# 📦 Module 6: Generics

🟡 **Intermediate**

## 6.1 Why Generics?

Without generics, you either lose type safety (`any`) or duplicate code for every type.

```typescript
// ✅ Generic: type-safe AND reusable
function getFirst<T>(arr: T[]): T {
  return arr[0];
}

const first1 = getFirst<string>(["a", "b"]); // string
const first2 = getFirst<number>([1, 2]);     // number
const first3 = getFirst(["x", "y"]);         // inferred: string
```

## 6.2 Multiple Type Parameters

```typescript
function pair<K, V>(key: K, value: V): [K, V] {
  return [key, value];
}

const entry = pair("name", "Alice"); // [string, string]
```

## 6.3 Generic Interfaces

```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

interface User { id: number; name: string; }

const userResponse: ApiResponse<User> = {
  data: { id: 1, name: "Alice" },
  status: 200,
  message: "OK"
};
```

## 6.4 Generic Classes

```typescript
class Stack<T> {
  private items: T[] = [];

  push(item: T): void { this.items.push(item); }
  pop(): T | undefined { return this.items.pop(); }
  isEmpty(): boolean { return this.items.length === 0; }
}

const numStack = new Stack<number>();
numStack.push(1);
numStack.pop(); // 1
```

## 6.5 Generic Constraints (`extends`)

```typescript
// T must have a .length property
function logLength<T extends { length: number }>(item: T): T {
  console.log(item.length);
  return item;
}

logLength("hello");   // ✅
logLength([1, 2, 3]); // ✅
// logLength(42);     // ❌ number has no .length
```

## 6.6 `keyof` with Generics

```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { id: 1, name: "Alice" };
getProperty(user, "name");    // ✅ "Alice"
// getProperty(user, "email"); // ❌ ERROR
```

---

## ⚡ Key Takeaways — Module 6

- Generics = type placeholders for flexible, reusable, type-safe code
- `<T>` on functions, interfaces, classes
- `T extends SomeType` constrains what T can be
- `keyof T` gives the union of a type's property keys

---

## ✅ Checklist — Module 6

- [ ] I understand why generics exist
- [ ] I can write generic functions, interfaces, and classes
- [ ] I can use `extends` to add constraints
- [ ] I can use `keyof` with generics

---
