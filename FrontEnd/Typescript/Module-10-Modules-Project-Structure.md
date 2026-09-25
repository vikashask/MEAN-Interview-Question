# 📦 Module 10: Modules & Project Structure

🟡 **Intermediate**

## 10.1 ES Module Syntax

```typescript
// math.ts — named exports
export function add(a: number, b: number): number { return a + b; }
export type MathFn = (a: number, b: number) => number;

// utils.ts — default export
export default function formatDate(date: Date): string {
  return date.toISOString();
}

// app.ts — imports
import { add, type MathFn } from './math';
import formatDate from './utils';
import * as MathUtils from './math'; // namespace import
```

## 10.2 `import type` — Type-Only Imports

```typescript
// Erased at compile time — no runtime overhead
import type { User } from './types';
```

## 10.3 Barrel Files (Re-exporting)

```typescript
// features/user/index.ts — public API of the folder
export { UserService } from './user.service';
export { UserController } from './user.controller';
export type { User, CreateUserDto } from './user.types';

// main.ts — clean single import
import { UserService, type User } from './features/user';
```

## 10.4 Module Resolution Modes

| Setting | Behavior |
| :--- | :--- |
| `"node"` | Classic Node.js / CommonJS |
| `"node16"` / `"nodenext"` | Node.js ESM (requires `.js` extensions) |
| `"bundler"` | For Vite, webpack, esbuild (recommended for browsers) |

---

## ⚡ Key Takeaways — Module 10

- Use ES Module syntax (`import`/`export`), not `require()`
- `import type` keeps bundles clean
- Barrel `index.ts` files create clean public APIs for folders
- Avoid `namespace` in new TypeScript code

---

## ✅ Checklist — Module 10

- [ ] I can use named, default, and re-exports
- [ ] I understand `import type` and when to use it
- [ ] I can create barrel files
- [ ] I understand module resolution modes

---
