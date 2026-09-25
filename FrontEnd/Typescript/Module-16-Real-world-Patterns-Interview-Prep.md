# 📦 Module 16: Real-world Patterns & Interview Prep

🔴 **Advanced**

## 16.1 Repository Pattern

Abstracts data access behind a generic interface.

```typescript
interface Repository<T> {
  findById(id: number): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(item: T): Promise<T>;
  delete(id: number): Promise<void>;
}

interface User { id: number; name: string; email: string; }

class UserRepository implements Repository<User> {
  private users: User[] = [];

  async findById(id: number): Promise<User | null> {
    return this.users.find(u => u.id === id) ?? null;
  }
  async findAll(): Promise<User[]> { return this.users; }
  async save(user: User): Promise<User> { this.users.push(user); return user; }
  async delete(id: number): Promise<void> {
    this.users = this.users.filter(u => u.id !== id);
  }
}
```

## 16.2 Builder Pattern

```typescript
class QueryBuilder {
  private table: string = '';
  private conditions: string[] = [];
  private limitVal: number = 100;

  from(table: string): this { this.table = table; return this; }
  where(condition: string): this { this.conditions.push(condition); return this; }
  limit(n: number): this { this.limitVal = n; return this; }

  build(): string {
    const where = this.conditions.length
      ? `WHERE ${this.conditions.join(' AND ')}`
      : '';
    return `SELECT * FROM ${this.table} ${where} LIMIT ${this.limitVal}`;
  }
}

const query = new QueryBuilder()
  .from("users")
  .where("age > 18")
  .limit(50)
  .build();
```

## 16.3 Exhaustive Checks with `never`

TS errors at compile time if you add a new union member and forget to handle it.

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "triangle"; base: number; height: number };

function getArea(shape: Shape): number {
  switch (shape.kind) {
    case "circle":   return Math.PI * shape.radius ** 2;
    case "square":   return shape.side ** 2;
    case "triangle": return 0.5 * shape.base * shape.height;
    default:
      // If a new shape is added and not handled, this line causes a compile error ✅
      const _exhaustive: never = shape;
      throw new Error(`Unhandled shape: ${_exhaustive}`);
  }
}
```

## 16.4 Branded / Nominal Types

Prevents accidentally mixing values of the same primitive type.

```typescript
type UserId    = number & { __brand: "UserId" };
type ProductId = number & { __brand: "ProductId" };

function createUserId(id: number): UserId { return id as UserId; }
function createProductId(id: number): ProductId { return id as ProductId; }

function getUser(id: UserId) { /* ... */ }

const uid = createUserId(1);
const pid = createProductId(2);

getUser(uid); // ✅
// getUser(pid); // ❌ ERROR — both are numbers, but different brands
// getUser(1);   // ❌ ERROR — plain number not accepted
```

## 16.5 Interview Questions & Answers

**Q: What is the difference between `interface` and `type`?**
> Both define type shapes for objects. `interface` supports declaration merging and `extends`. `type` supports unions, intersections, primitives, and tuples. Use `interface` for objects/classes, `type` for everything else.

**Q: What is `unknown` vs `any`?**
> `any` disables all type checking. `unknown` forces you to narrow the type before using it. Always prefer `unknown` for values whose types are unknown.

**Q: What is structural typing?**
> TypeScript checks types by **shape** (properties and methods), not by name. If two types have the same shape, they are compatible — even if named differently. This is structural (duck) typing.

**Q: What is a type guard?**
> A condition that narrows a union type to a specific member: `typeof`, `instanceof`, `in`, or a user-defined function with `value is T`.

**Q: What does `strict: true` enable?**
> It enables: `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, `strictPropertyInitialization`, `strictBindCallApply`, `useUnknownInCatchVariables`, and more.

**Q: What are generics?**
> Type variables (`<T>`) that make functions, classes, and interfaces reusable across different types while maintaining full type safety.

**Q: What is the `satisfies` operator?**
> It validates that a value matches a type **without widening** the inferred type — giving you both type safety and precise inference.

**Q: What are declaration files (`.d.ts`)?**
> Type definitions for JavaScript libraries — only type information, no runtime code. Consumed automatically when TypeScript resolves a module.

## 16.6 Common Mistakes Reference

| Mistake | Better Alternative |
| :--- | :--- |
| Using `any` everywhere | Use `unknown` + narrowing |
| Ignoring `strictNullChecks` | Enable `strict: true` |
| Annotating every inferred value | Let TS infer `let x = 5` |
| Using `object` type | Use `Record<string, unknown>` or specific shape |
| Forgetting `.d.ts` for JS imports | Install `@types/...` |
| Not handling `catch (e)` correctly | Always check `e instanceof Error` |
| Using `!` non-null assertion blindly | Use null check `if (x)` instead |
| Not using discriminated unions | Add a `status`/`kind` discriminant property |

## 16.7 Professional TypeScript Project Checklist

```
✅ tsconfig.json with "strict": true
✅ No implicit `any` — everything typed or inferred
✅ Types organized in src/types/ directory
✅ Zod for runtime validation of external data (API, env)
✅ Unit tests with Vitest or Jest + ts-jest
✅ ESLint with @typescript-eslint/recommended
✅ Path aliases configured (@/ → src/)
✅ Barrel files (index.ts) for clean imports
✅ Discriminated unions for state management
✅ Error handling with instanceof Error
✅ `import type` for type-only imports
✅ Exhaustive switch checks with never
```

---

## ⚡ Key Takeaways — Module 16

- Use Repository and Builder patterns for scalable, testable architecture
- Exhaustive `never` checks = compile-time safety for union variants
- Branded types prevent accidentally mixing same-typed IDs
- `strict: true` is non-negotiable in production codebases

---

## ✅ Final Checklist — Module 16

- [ ] I understand discriminated unions and exhaustive checks
- [ ] I understand structural typing and why branded types exist
- [ ] I can answer common TypeScript interview questions confidently
- [ ] I know common TypeScript pitfalls and how to avoid them
- [ ] I can architect a production-grade TypeScript project

---

# 🎓 Congratulations! You've Completed the TypeScript Masterclass!

> You now have end-to-end TypeScript knowledge — from primitives to type-level programming, from browser DOM to Node.js backends, from tsconfig to real-world architecture.

## 📚 What to Do Next

1. **Build real projects** — apply these concepts in full-stack apps
2. **TypeScript Handbook** — [typescriptlang.org/docs](https://www.typescriptlang.org/docs/)
3. **TypeScript Playground** — [typescriptlang.org/play](https://www.typescriptlang.org/play)
4. **Type Challenges** — [github.com/type-challenges/type-challenges](https://github.com/type-challenges/type-challenges)
5. **Follow TS releases** — new features every ~3 months
