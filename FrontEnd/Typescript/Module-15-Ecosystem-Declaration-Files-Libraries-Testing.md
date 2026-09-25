# 📦 Module 15: Ecosystem (Declaration Files, Libraries, Testing)

🔴 **Advanced**

## 15.1 Declaration Files (`.d.ts`)

Provide type info for JavaScript libraries — **only types, no implementation**.

```bash
# Libraries with built-in types
npm install axios zod prisma

# Libraries needing separate type packages
npm install -D @types/express @types/lodash @types/node
```

## 15.2 Writing Declaration Files

```typescript
// src/types/global.d.ts

// Type SVG imports in bundlers
declare module '*.svg' {
  const content: string;
  export default content;
}

// Type an untyped JS library
declare module 'some-untyped-lib' {
  export function doSomething(value: string): number;
  export interface Options { timeout: number; }
}

// Augment global types
declare global {
  interface Window {
    analytics: { track: (event: string) => void };
  }
}
```

## 15.3 Runtime Validation with Zod

TypeScript types are erased at runtime. **Zod validates data shapes at runtime** (API responses, form inputs, env vars).

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.number(),
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().optional()
});

// Derive TS type from schema — single source of truth!
type User = z.infer<typeof UserSchema>;

async function parseUser(data: unknown): Promise<User> {
  return UserSchema.parse(data); // throws if invalid
}
```

## 15.4 Testing with Vitest

```bash
npm install -D vitest
```

```typescript
// math.ts
export function add(a: number, b: number): number { return a + b; }

// math.test.ts
import { describe, it, expect } from 'vitest';
import { add } from './math';

describe('add()', () => {
  it('adds two positive numbers', () => {
    expect(add(2, 3)).toBe(5);
  });
  it('handles negatives', () => {
    expect(add(-1, 1)).toBe(0);
  });
});
```

## 15.5 Testing with Jest + ts-jest

```bash
npm install -D jest ts-jest @types/jest
npx ts-jest config:init
```

```typescript
import { add } from './math';

test('adds numbers correctly', () => {
  expect(add(1, 2)).toBe(3);
});
```

---

## ⚡ Key Takeaways — Module 15

- `.d.ts` files provide type info for JavaScript libraries
- Install `@types/package-name` for libraries without built-in types
- Use **Zod** for runtime validation — derive TS types with `z.infer<>`
- Use **Vitest** (Vite) or **Jest + ts-jest** for unit testing

---

## ✅ Checklist — Module 15

- [ ] I understand what `.d.ts` files do
- [ ] I know how to find and install type definitions
- [ ] I can write a basic module declaration file
- [ ] I can use Zod for runtime validation
- [ ] I can write and run TypeScript unit tests

---
