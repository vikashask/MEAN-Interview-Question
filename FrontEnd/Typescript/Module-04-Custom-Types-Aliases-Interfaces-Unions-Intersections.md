# 📦 Module 4: Custom Types (Aliases, Interfaces, Unions, Intersections)

🟡 **Intermediate**

## 4.1 Type Aliases (`type`)

Create reusable names for any type — primitives, unions, tuples, functions, objects.

```typescript
type ID = string | number;
type Coordinates = [number, number];
type Formatter = (value: string) => string;

type User = {
  id: ID;
  name: string;
  createdAt: Date;
};
```

## 4.2 Interfaces (`interface`)

Specifically for **object shapes** and **class contracts**.

```typescript
interface Product {
  id: number;
  name: string;
  price: number;
  description?: string;  // optional
  readonly sku: string;  // immutable
}

// Extending interfaces
interface Electronics extends Product {
  warrantyYears: number;
}
```

### Declaration Merging (Interfaces Only)

```typescript
interface Window {
  myCustomProp: string; // extends the global Window type
}
```

## 4.3 `type` vs `interface`

| Feature | `type` | `interface` |
| :--- | :--- | :--- |
| **Objects** | ✅ | ✅ |
| **Primitives/Unions/Tuples** | ✅ | ❌ |
| **Extending** | `&` intersection | `extends` keyword |
| **Declaration Merging** | ❌ | ✅ |
| **Best for** | Unions, utilities | Objects, OOP, classes |

> **Rule of thumb:** `interface` for objects/classes. `type` for unions, primitives, and transformations.

## 4.4 Union Types (`|`) and Literal Types

```typescript
function printId(id: string | number): void {
  console.log(`ID: ${id}`);
}

// Literal types — narrow to specific values
type Direction = "up" | "down" | "left" | "right";
type StatusCode = 200 | 400 | 404 | 500;

function move(dir: Direction): void { console.log(`Moving ${dir}`); }
move("up");    // ✅
// move("diagonal"); // ❌ ERROR
```

## 4.5 Intersection Types (`&`)

Value must satisfy **all** combined types.

```typescript
type Timestamps = { createdAt: Date; updatedAt: Date };
type BaseEntity = { id: number };
type Auditable = BaseEntity & Timestamps;

const record: Auditable = {
  id: 1,
  createdAt: new Date(),
  updatedAt: new Date()
};
```

---

## ⚡ Key Takeaways — Module 4

- `type`: flexible, handles unions/primitives/tuples
- `interface`: best for objects and classes, supports `extends` and merging
- `|` = OR (union), `&` = AND (intersection)
- Literal types narrow strings/numbers to specific allowed values

---

## ✅ Checklist — Module 4

- [ ] I know when to use `type` vs `interface`
- [ ] I can create and compose union types
- [ ] I can create intersection types
- [ ] I understand literal types and their use in unions
- [ ] I know what declaration merging is

---
