# The Ultimate TypeScript Mastery Guide: From Beginner to Pro

> **A Complete Roadmap for JavaScript Developers**  
> *Learn TypeScript step-by-step with real-world examples, practical patterns, and hands-on exercises.*

---

## 📚 Table of Contents

1. [**Section 0: Setup & Tooling**](#section-0-setup--tooling)
2. [**Section 1: TypeScript Basics**](#section-1-typescript-basics-beginner)
3. [**Section 2: Functions**](#section-2-functions-core-ts)
4. [**Section 3: Objects and Interfaces**](#section-3-objects-and-interfaces)
5. [**Section 4: Classes and OOP**](#section-4-classes-and-oop-in-ts)
6. [**Section 5: Advanced Types**](#section-5-advanced-types)
7. [**Section 6: Utility Types**](#section-6-utility-types)
8. [**Section 7: Modules & Project Architecture**](#section-7-modules--project-architecture)
9. [**Section 8: Async TypeScript**](#section-8-async-typescript)
10. [**Section 9: TypeScript with Node.js**](#section-9-typescript-with-nodejs-real-world)
11. [**Section 10: TypeScript with React**](#section-10-typescript-with-react-real-world)
12. [**Section 11: Best Practices**](#section-11-typescript-best-practices)
13. [**Section 12: Testing**](#section-12-testing-with-typescript)
14. [**Section 13: Interview Prep**](#section-13-interview-prep)
15. [**Capstone Projects**](#capstone-projects)
16. [**Cheatsheet & Roadmap**](#typescript-cheatsheet--roadmap)

---

## Section 0: Setup & Tooling

### What is TypeScript?
TypeScript is a superset of JavaScript that adds static typing. Think of it as "JavaScript with safety features." 
- **JS**: You find out about errors when the user runs the app.
- **TS**: You find out about errors while you type the code.

### 💡 Why this matters
In a large JavaScript project, refactoring is scary. You change a function name, and you hope you updated usage everywhere. In TypeScript, the compiler tells you exactly what broke. It's like having a pair programmer who checks your work instantly.

### Installation & Setup

1. **Install Global TS** (Optional but useful)
   ```bash
   npm install -g typescript ts-node
   ```

2. **Initialize a Project**
   ```bash
   mkdir learn-ts
   cd learn-ts
   npm init -y
   npm install -D typescript ts-node nodemon
   npx tsc --init
   ```

### Understanding `tsconfig.json`
This file controls how TypeScript behaves. Here are the critical settings:

```json
{
  "compilerOptions": {
    "target": "ES2020",          // Which JS version to output
    "module": "commonjs",        // For Node.js (use "ESNext" for frontend)
    "strict": true,              // ENABLE THIS! Enforces best practices
    "outDir": "./dist",          // Where compiled JS goes
    "rootDir": "./src",          // Where your TS files are
    "esModuleInterop": true      // Fixes import issues with CommonJS modules
  }
}
```

### ⚠️ Common Mistakes
- **Forgetting `strict: true`**: Without this, TypeScript is too lenient and you lose many benefits.
- **Editing files in `dist/`**: Never touch the compiled JS. Only edit `.ts` files in `src/`.

### Exercises
1. Initialize a new TS project.
2. Create `src/index.ts` containing `console.log("Hello TS")`.
3. Run `npx tsc` and check `dist/index.js`.
4. Configure `nodemon` to watch `.ts` files using `ts-node` (hint: `nodemon.json` config).

---

## Section 1: TypeScript Basics (Beginner)

### Concept: The Base Types
TypeScript adds types to variables. 

### Syntax & Examples

```ts
// Primitives
let username: string = "Alice";
let age: number = 30;
let isAdmin: boolean = true;

// Arrays
let scores: number[] = [10, 20, 30];
let names: Array<string> = ["Alice", "Bob"]; // Generic syntax

// Tuples (Fixed length & type order)
let userRow: [number, string] = [1, "Alice"]; 
// userRow = ["Alice", 1]; // Error: Type mismatch

// Any (Avoid this!)
let data: any = "Could be anything"; 
data = 5; // No error (Bad!)

// Union Types (Very common)
let id: string | number;
id = 101; // OK
id = "User-101"; // OK
```

### Real-World Usage: Functional Args
```ts
function getStatus(code: 200 | 404 | 500) {
  if (code === 200) return "OK";
  // ...
}
```

### Type Narrowing
When typing allows multiple types, strict checks "narrow" it down.
```ts
function printId(id: string | number) {
  if (typeof id === "string") {
    console.log(id.toUpperCase()); // TS knows it's a string here
  } else {
    console.log(id.toFixed(2));    // TS knows it's a number here
  }
}
```

### 💡 Why this matters
`Union` types model real life. A database ID might be a number or a UUID string. TypeScript forces you to handle both cases, preventing crashing bugs.

### ⚠️ Common Mistakes
- Using `any` when you could use `unknown` (which forces a type check before use).
- Assuming a union type has methods of *all* types. (e.g., calling `.toUpperCase()` on `string | number` without checking type).

### Exercises
1. Create a variable that can be a `string` or `null`.
2. Write a function that accepts `string | string[]` and prints them joined by commas if it's an array, or just prints the string.
3. Define a tuple for a 3D coordinate `[x, y, z]`.
4. Create an Enum `UserRole` with `ADMIN`, `EDITOR`, `GUEST`.
5. Use `type` alias to define `UserID = string | number`.

---

## Section 2: Functions (Core TS)

### Typing Functions
You must type arguments. Return types are usually inferred, but explicit is better for documentation.

```ts
// Explicit return type
function add(a: number, b: number): number {
  return a + b;
}

// Optional parameters (?)
function greet(name: string, greeting?: string): string {
  // greeting is "string | undefined"
  return `${greeting || "Hello"}, ${name}`;
}

// Default parameters
function multiply(a: number, b: number = 2): number {
  return a * b;
}

// Rest parameters
function sum(...numbers: number[]): number {
  return numbers.reduce((total, n) => total + n, 0);
}
```

### Real-World Usage: API Calls
```ts
// Void: Function returns nothing
function logMessage(msg: string): void {
  console.log(msg);
}

// Async functions return Promise<Type>
async function fetchUser(id: string): Promise<{ name: string }> {
  return { name: "Alice" };
}
```

### ⚠️ Common Mistakes
- Not handling `undefined` in optional parameters.
- Putting optional parameters *before* required ones (not allowed).

### Exercises
1. Write a function `formatName` that takes `firstName` and optional `lastName`.
2. Write an arrow function typed as a variable: `const mathOp: (x: number) => number = ...`
3. Create a function that throws an error and return type `never`.
4. Implement function overloads for a function `makeDate` that accepts `timestamp: number` OR `m: number, d: number, y: number`.
5. Write a rest parameter function that concatenates infinite strings.

---

## Section 3: Objects and Interfaces

### Interface vs Type
They are 95% similar. 
- Use **interface** for objects and defining "shapes" (better error messages, supports merging).
- Use **type** for unions, primitives, and complex utility types.

### Syntax

```ts
interface User {
  readonly id: number;   // Cannot change after creation
  username: string;
  email?: string;        // Optional
  [key: string]: any;    // Index signature (allow extra properties)
}

const u1: User = {
  id: 1,
  username: "alice",
  extraProp: "allowed because of index signature"
};

// Extending Interfaces
interface Admin extends User {
  permissions: string[];
}
```

### Real-World Usage: Config Objects
```ts
interface DBConfig {
  host: string;
  port?: number; // defaults to 5432
  ssl: boolean;
}
```

### 💡 Why this matters
Interfaces are the contract of your application. If the backend API changes its response shape, you update the Interface, and TS instantly shows you every component that just broke.

### Exercises
1. Define an interface `Car` with `make`, `model`, and `year`.
2. Extend `Car` to `ElectricCar` adding `batteryLife`.
3. Create an object that uses an index signature to store a dictionary of translations (key: string, value: string).
4. Use `readonly` on an array property inside an interface.
5. Create an interface with a method definition inside it.

---

## Section 4: Classes and OOP in TS

### Syntax & Modifiers

```ts
abstract class Animal {
  constructor(public name: string) {} // Shorthand initialization
  abstract makeStyles(): void;
}

class Dog extends Animal {
  private _age: number = 0; // Only accessible inside Dog
  
  constructor(name: string) {
    super(name);
  }

  makeStyles() {
    console.log("Woof!");
  }

  // Getter & Setter
  get age() { return this._age; }
  set age(v: number) { 
    if(v < 0) throw new Error("Invalid age");
    this._age = v; 
  }
}

const d = new Dog("Buddy");
// d._age; // Error: private
```

### Implements
Classes can enforce interfaces.
```ts
interface Runnable {
  run(): void;
}

class Cat implements Runnable {
  run() { console.log("Running"); }
}
```

### 💡 Why this matters
Detailed access control (`private`, `protected`) helps encapsulate logic, preventing other devs from modifying internal state directly, which reduces bugs.

### Exercises
1. Create a class `Employee` with private `salary`.
2. Add a static method `Employee.compareSalary(e1, e2)`.
3. Create an abstract class `Shape` with `getArea()`.
4. Implement `Circle` and `Rectangle` extending `Shape`.
5. Use the `protected` modifier and show how it differs from `private` in a subclass.

---

## Section 5: Advanced Types

### Generics
Generics allow reusable components that work with any type. Think of them as "variables for types".

```ts
// T is a placeholder type
function identity<T>(arg: T): T {
  return arg;
}

const num = identity<number>(5);
const str = identity("hello"); // inferred
```

### Generic Constraints
```ts
interface HasLength {
  length: number;
}

function logLength<T extends HasLength>(item: T) {
  console.log(item.length);
}
```

### Keyof & Typeof
```ts
const config = { width: 100, height: 200 };
type Config = typeof config; // { width: number, height: number }
type ConfigKeys = keyof Config; // "width" | "height"
```

### 💡 Why this matters
Generics are the backbone of libraries like React (`useState<User>`) or tools like `axios` (`axios.get<UserResponse>`).

### Exercises
1. Create a generic class `Storage<T>` that holds an array of `T` items.
2. Write a function `getProperty<T, K extends keyof T>(obj: T, key: K)` that returns `obj[key]`.
3. Use `typeof` to create a type from a constant object.
4. Create a mapped type that turns all properties of `T` into booleans.
5. Create a conditional type `IsString<T>` that is true/false.

---

## Section 6: Utility Types

These are built-in tools to transform types.

### Common Utilities

1.  **Partial<T>**: Makes all props optional.
    ```ts
    const update: Partial<User> = { email: "new@mail.com" }; // id, name missing is OK
    ```
2.  **Pick<T, K>**: Select specific keys.
    ```ts
    type UserPreview = Pick<User, "id" | "username">;
    ```
3.  **Omit<T, K>**: Remove specific keys.
    ```ts
    type CreateUserDTO = Omit<User, "id">; // ID is generated by DB
    ```
4.  **Record<K, T>**: Create map objects.
    ```ts
    const roles: Record<string, number> = { "admin": 1, "guest": 0 };
    ```
5.  **ReturnType<T>**: Get the return type of a function.
    ```ts
    type ApiReturn = ReturnType<typeof fetchUser>;
    ```

### Exercises
1. Use `Record` to define a map of users by ID.
2. Use `Omit` to create a type for a "Passwordless User".
3. Use `Required` to make optional fields mandatory.
4. Use `Extract` to get only the string types from `string | number | boolean`.
5. Create a `DeepPartial` type (recursively makes nested props optional).

---

## Section 7: Modules & Project Architecture

### Best Practices
- **Barreling**: Create `index.ts` in folders to export contents cleanly.
  ```ts
  // features/auth/index.ts
  export * from './AuthService';
  export * from './AuthComponent';
  // Now import from 'features/auth'
  ```
- **Path Aliases**: Avoid `../../../../components`.
  In `tsconfig.json`:
  ```json
  "paths": { "@components/*": ["src/components/*"] }
  ```

---

## Section 8: Async TypeScript

### Promises & Async/Await

```ts
interface Post {
  id: number;
  title: string;
}

// Typing the Promise resolution
const getPosts = async (): Promise<Post[]> => {
  const res = await fetch('/api/posts');
  return res.json() as Promise<Post[]>;
};

// Handling Errors
try {
  await getPosts();
} catch (error: unknown) {
  // Error in catch is always 'unknown' or 'any'
  if (error instanceof Error) {
    console.error(error.message);
  }
}
```

---

## Section 9: TypeScript with Node.js (Real World)

### Express Pattern
```ts
import express, { Request, Response, NextFunction } from 'express';

interface CreateUserReq {
  username: string;
}

// Generic: Request<Params, ResBody, ReqBody>
const createUser = (req: Request<{}, {}, CreateUserReq>, res: Response) => {
  const { username } = req.body;
  res.json({ message: `Created ${username}` });
};

const app = express();
app.post('/users', createUser);
```

### Zod Validation (Highly Recommended)
Zod allows you to validate runtime data (like API body) AND infer static types.
```ts
import { z } from 'zod';

const UserSchema = z.object({
  username: z.string().min(3),
  age: z.number().optional()
});

type User = z.infer<typeof UserSchema>; // { username: string; age?: number }

app.post('/users', (req, res) => {
  const result = UserSchema.safeParse(req.body);
  if (!result.success) return res.status(400).send(result.error);
  // req.body is safe now
});
```

---

## Section 10: TypeScript with React

### Components & Props
```ts
interface ButtonProps {
  label: string;
  onClick: (e: React.MouseEvent<HTMLButtonElement>) => void;
  variant?: 'primary' | 'secondary';
}

export const Button = ({ label, onClick, variant = 'primary' }: ButtonProps) => {
  return <button className={variant} onClick={onClick}>{label}</button>;
};
```

### Hooks
```ts
// useState
const [user, setUser] = useState<User | null>(null);

// useRef
const inputRef = useRef<HTMLInputElement>(null);
// usage: inputRef.current?.focus()
```

### 💡 Why this matters
React props are the #1 source of bugs. Did you pass a string instead of a number? TS catches this instantly in VS Code before you even save the file.

---

## Section 11: TypeScript Best Practices

1. **Avoid `any` at all costs**: It disables TS. Use `unknown` if you truly don't know.
2. **Strict Mode**: Always keep `"strict": true` in tsconfig.
3. **Derived Types**: Don't duplicate types. Use `Pick`, `Omit`, `typeof` to base types on single sources of truth.
4. **Validation Bounds**: Validate data at the "edges" of your app (API response, user input) using Zod/Yup. Trust the types inside your app.

---

## Section 12: Testing with TypeScript

### Jest Setup
```bash
npm install -D jest ts-jest @types/jest
npx ts-jest config:init
```

### Mocking
```ts
// user.ts
export const getUser = (id: string) => { ... }

// user.test.ts
import { getUser } from './user';
jest.mock('./user');

const mockedGetUser = getUser as jest.MockedFunction<typeof getUser>;

test('returns user', () => {
  mockedGetUser.mockReturnValue({ id: '1', name: 'Test' });
  expect(getUser('1').name).toBe('Test');
});
```

---

## Section 13: Interview Prep

### Key Questions
1. **Explain `interface` vs `type`.** (Interface for objects/merging, Type for unions/primitives).
2. **What is "Type Erasure"?** (TS types disappear at runtime; they don't exist in the JS output).
3. **What is `unknown` vs `any`?** (`any` allows anything safely, `unknown` allows anything but requires checking before use).
4. **Explain Generics.** (Reusable templates for code).
5. **What are discriminating unions?** (Unions of objects with a common literal field to distinguish them).

---

## Capstone Projects

### 1. Beginner: Typed CLI To-Do App
**Goal**: Learn File I/O, Types, and Arrays.

**Code Structure**:
```ts
// types.ts
export interface TodoItem {
  id: number;
  task: string;
  done: boolean;
}

// index.ts
import * as fs from 'fs';
const TODOS_FILE = 'todos.json';

const loadTodos = (): TodoItem[] => {
  try {
    const data = fs.readFileSync(TODOS_FILE, 'utf-8');
    return JSON.parse(data) as TodoItem[];
  } catch {
    return [];
  }
};

const addTodo = (task: string): void => {
  const todos = loadTodos();
  const newTodo: TodoItem = { id: Date.now(), task, done: false };
  todos.push(newTodo);
  fs.writeFileSync(TODOS_FILE, JSON.stringify(todos, null, 2));
  console.log('Added:', task);
};
```

### 2. Intermediate: Typed REST API (Express + Zod)
**Goal**: Server structure, Validation, DTOs.

**Core Architecture**:
```ts
// src/utils/response.ts
interface ServiceResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

// src/services/userService.ts
import { User, CreateUserDTO } from '../types';

export const createUser = async (dto: CreateUserDTO): Promise<ServiceResponse<User>> => {
  // DB logic here
  return { success: true, data: { id: 1, ...dto, createdAt: new Date() } };
};

// src/controllers/userController.ts
import { Request, Response } from 'express';
import { CreateUserSchema } from '../schemas/userSchema';
import * as userService from '../services/userService';

export const create = async (req: Request, res: Response) => {
  // 1. Validate
  const validation = CreateUserSchema.safeParse(req.body);
  if (!validation.success) return res.status(400).json(validation.error);
  
  // 2. Call Service
  const result = await userService.createUser(validation.data);
  return res.json(result);
};
```

### 3. Advanced: React Dashboard (Generic Components)
**Goal**: Hooks, Generics, Component Composition.

**Generic Data Grid**:
```tsx
interface DataGridProps<T> {
  items: T[];
  columns: (keyof T)[];
}

export const DataGrid = <T extends { id: number | string }>({ items, columns }: DataGridProps<T>) => {
  return (
    <table>
      <thead>
        <tr>{columns.map(col => <th key={String(col)}>{String(col)}</th>)}</tr>
      </thead>
      <tbody>
        {items.map(item => (
          <tr key={item.id}>
            {columns.map(col => <td key={String(col)}>{String(item[col])}</td>)}
          </tr>
        ))}
      </tbody>
    </table>
  );
};
// Usage: <DataGrid items={users} columns={["id", "username", "email"]} />
```

---

## TypeScript Cheatsheet & Roadmap

### 30-Day Practice Roadmap
- **Week 1**: Primitives, Arrays, Functions, Interfaces. (Convert small JS scripts).
- **Week 2**: Classes, DOM Manipulation, Mini-Projects.
- **Week 3**: Generics, Utility Types, Node.js integration.
- **Week 4**: React integration, Zod, Advanced Patterns.

### Quick Reference
| Sytnax | Description |
| :--- | :--- |
| `variable: string` | Explicit typing |
| `type ID = string \| number` | Union Type |
| `interface User { ... }` | Object Shape |
| `param?: string` | Optional |
| `fn = (a: number) => void` | Function Type |
| `<T>` | Generic |
| `keyof T` | Keys of T |
| `as string` | Type Assertion (Casting) |

---
**End of Guide**
