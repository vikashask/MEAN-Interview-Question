# 📦 Module 13: TypeScript in Node.js (Backend)

🟡 **Intermediate**

## 13.1 Setup

```bash
mkdir my-api && cd my-api
npm init -y
npm install typescript ts-node @types/node --save-dev
npx tsc --init
```

`tsconfig.json` for Node.js:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "CommonJS",
    "moduleResolution": "node",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true
  }
}
```

## 13.2 Node.js Built-ins

```typescript
import * as fs from 'fs';
import * as path from 'path';
import { createServer, IncomingMessage, ServerResponse } from 'http';

const content: string = fs.readFileSync(path.join(__dirname, 'data.json'), 'utf-8');

const server = createServer((req: IncomingMessage, res: ServerResponse) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ message: 'Hello' }));
});
server.listen(3000);
```

## 13.3 Express with TypeScript

```bash
npm install express && npm install -D @types/express
```

```typescript
import express, { Request, Response, NextFunction } from 'express';

const app = express();
app.use(express.json());

interface CreateUserBody { name: string; email: string; }

app.post('/users', (req: Request<{}, {}, CreateUserBody>, res: Response) => {
  const { name, email } = req.body; // fully typed ✅
  res.status(201).json({ id: Date.now(), name, email });
});

app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  res.status(500).json({ error: err.message });
});

app.listen(3000, () => console.log('Server running'));
```

## 13.4 Environment Variables

```typescript
function getEnvVar(key: string): string {
  const value = process.env[key];
  if (!value) throw new Error(`Missing env var: ${key}`);
  return value;
}

export const config = {
  port: parseInt(getEnvVar('PORT'), 10),
  dbUrl: getEnvVar('DATABASE_URL'),
  jwtSecret: getEnvVar('JWT_SECRET')
};
```

---

## ⚡ Key Takeaways — Module 13

- Install `@types/node` for Node built-ins, `@types/express` for Express
- Use `Request<Params, ResBody, ReqBody, Query>` generics for typed routes
- Centralize env vars with validation
- `ts-node` for dev, `tsc && node dist/` for production

---

## ✅ Checklist — Module 13

- [ ] I can set up a TypeScript Node.js project
- [ ] I can use typed Node.js built-in modules
- [ ] I can write typed Express route handlers
- [ ] I can type Express request bodies
- [ ] I can safely validate environment variables

---
