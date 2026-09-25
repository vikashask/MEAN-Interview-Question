# 📦 Module 14: Configuration & Compilation (`tsconfig.json`)

🔴 **Advanced**

## 14.1 Structure

```json
{
  "compilerOptions": {},  // compiler behavior
  "include": [],          // files to include
  "exclude": [],          // files to exclude
  "extends": ""           // inherit from another config
}
```

## 14.2 Critical Options

### Type Checking

| Option | Default | Recommended | Description |
| :--- | :--- | :--- | :--- |
| `strict` | `false` | `true` ✅ | Enables ALL strict checks |
| `noImplicitAny` | `false` | `true` | Error on implicit `any` |
| `strictNullChecks` | `false` | `true` | `null`/`undefined` not auto-assignable |
| `noUncheckedIndexedAccess` | `false` | `true` | Array index returns `T \| undefined` |

### Output

| Option | Description | Example |
| :--- | :--- | :--- |
| `target` | JS version to output | `"ES2022"` |
| `module` | Module system | `"CommonJS"`, `"ESNext"` |
| `outDir` | Output directory | `"./dist"` |
| `rootDir` | Source directory | `"./src"` |
| `declaration` | Generate `.d.ts` files | `true` |
| `sourceMap` | Generate `.map` files | `true` |
| `noEmit` | Type-check only, no output | `true` |

## 14.3 Recommended Templates

### Node.js API

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "CommonJS",
    "moduleResolution": "node",
    "strict": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "sourceMap": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Frontend (Vite/Bundler)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "paths": { "@/*": ["./src/*"] }
  }
}
```

## 14.4 Path Aliases

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@components/*": ["src/components/*"],
      "@utils/*": ["src/utils/*"]
    }
  }
}
```

```typescript
// Before: fragile
import { Button } from '../../../components/Button';
// After: clean
import { Button } from '@components/Button';
```

---

## ⚡ Key Takeaways — Module 14

- Always enable `"strict": true` — the most impactful single option
- `target` = JS output version, `module` = module system format
- `noUncheckedIndexedAccess` catches array out-of-bounds bugs
- Use `paths` aliases for clean imports in large projects

---

## ✅ Checklist — Module 14

- [ ] I understand the purpose of `tsconfig.json`
- [ ] I always enable `strict` mode
- [ ] I know the difference between `target` and `module`
- [ ] I can set up path aliases
- [ ] I know when to use `noEmit` vs `outDir`

---
