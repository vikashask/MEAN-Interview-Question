# Design Patterns Handbook (JavaScript Focus, Polyglot-Friendly)

> **What this is:** A practical, example-driven guide to classic design patterns and how to apply them in JavaScript/TypeScript and other languages (Java/C#/Python). Includes when to use, trade-offs, anti‑patterns, and testing notes.

---

## Table of Contents

1. [Why Design Patterns?](#why-design-patterns)
2. [How to Choose a Pattern](#how-to-choose-a-pattern)
3. [Core Principles (SOLID & Friends)](#core-principles-solid--friends)
4. [Creational Patterns](#creational-patterns)
   - Singleton • Factory Method • Abstract Factory • Builder • Prototype
5. [Structural Patterns](#structural-patterns)
   - Adapter • Bridge • Composite • Decorator • Facade • Flyweight • Proxy
6. [Behavioral Patterns](#behavioral-patterns)
   - Chain of Responsibility • Command • Interpreter • Iterator • Mediator • Memento • Observer • State • Strategy • Template Method • Visitor
7. [JavaScript‑Native/Architectural Patterns](#javascript-nativearchitectural-patterns)
   - Module • Revealing Module • Pub/Sub vs Observer • MVC/MVP/MVVM • Dependency Injection • Middleware • Reactor/Event Loop
8. [Async & Concurrency Patterns in JS](#async--concurrency-patterns-in-js)
9. [Pattern Selection Cheatsheet](#pattern-selection-cheatsheet)
10. [Testing & Maintainability Tips](#testing--maintainability-tips)
11. [Anti‑Patterns to Avoid](#anti-patterns-to-avoid)
12. [Further Reading](#further-reading)

---

## Why Design Patterns?

- Provide **shared vocabulary** for solutions to recurring design problems.
- Improve **maintainability, testability, and extensibility**.
- In JS apps (Node/React/Angular), patterns map cleanly to **modules, services, hooks, middleware, and components**.
- Use patterns **judiciously**—prefer simplicity; patterns are tools, not goals.

## How to Choose a Pattern

1. Identify the **forces** (what varies): construction, behavior, or structure.
2. Prefer **composition over inheritance**.
3. Start simple → refactor toward a pattern when duplication/complexity emerges.

> **Heuristic**: If many `if/else` branches select algorithms → **Strategy**. If object creation logic explodes → **Factory/Builder**. If incompatible APIs → **Adapter**. If you need to add cross‑cutting features (logging/cache) at runtime → **Decorator/Proxy**.

## Core Principles (SOLID & Friends)

- **S**ingle Responsibility: one reason to change.
- **O**pen/Closed: open for extension, closed for modification.
- **L**iskov Substitution: subtypes must be usable via base types.
- **I**nterface Segregation: many small interfaces over fat ones.
- **D**ependency Inversion: depend on abstractions, not concretions.
- **DRY**, **KISS**, **YAGNI**, **Law of Demeter**.

---

## Creational Patterns

### 1) Singleton

Ensures single instance; global access. In Node.js, **modules are singletons by default** due to caching.

**JavaScript**

```js
// config.js
class Config {
  constructor() {
    this.port = 3000;
  }
}
module.exports = new Config(); // Node's module cache ensures singleton
```

**Use when**: shared configuration, connection pools.  
**Trade‑offs**: hidden global state; complicates tests. Prefer DI in large systems.

### 2) Factory Method

Defer instantiation to subclasses or functions.

```ts
interface Logger {
  log(msg: string): void;
}
class ConsoleLogger implements Logger {
  log(m) {
    console.log(m);
  }
}
class FileLogger implements Logger {
  constructor(path) {
    this.path = path;
  }
  log(m) {
    /* write */
  }
}
function createLogger(env: "dev" | "prod"): Logger {
  return env === "prod"
    ? new FileLogger("/var/log/app.log")
    : new ConsoleLogger();
}
```

**Use**: choose implementation at runtime; hide creation complexity.

### 3) Abstract Factory

Create **families** of related objects without specifying concrete classes.

```ts
// UI theme widgets
interface Button {
  render(): string;
}
interface Checkbox {
  render(): string;
}
interface WidgetFactory {
  createButton(): Button;
  createCheckbox(): Checkbox;
}
class LightFactory implements WidgetFactory {
  createButton() {
    return { render: () => '<button class="light">OK</button>' };
  }
  createCheckbox() {
    return { render: () => '<input class="light" type="checkbox"/>' };
  }
}
class DarkFactory implements WidgetFactory {
  /* similar dark variants */
}
```

**Use**: multi‑theme UI kits; database client families.

### 4) Builder

Step‑wise construction of complex objects; immutable end product.

```ts
class QueryBuilder {
  constructor() {
    this._sel = "*";
    this._tbl = "";
    this._where = [];
  }
  select(cols) {
    this._sel = cols.join(",");
    return this;
  }
  from(t) {
    this._tbl = t;
    return this;
  }
  where(c) {
    this._where.push(c);
    return this;
  }
  build() {
    return `SELECT ${this._sel} FROM ${this._tbl} WHERE ${this._where.join(
      " AND "
    )}`;
  }
}
const sql = new QueryBuilder()
  .select(["id", "name"])
  .from("users")
  .where("active=1")
  .build();
```

**Use**: complex configuration/queries; HTTP requests.

### 5) Prototype

Clone existing objects instead of constructing from scratch.

```js
const proto = {
  greet() {
    return `hi ${this.name}`;
  },
};
const user = Object.assign(Object.create(proto), { name: "Vikas" });
```

**Use**: object cloning, performance when creation is expensive.

---

## Structural Patterns

### 1) Adapter

Convert one interface to another clients expect.

```ts
// Legacy payment API vs new interface
class LegacyPay {
  send(amount) {
    /* ... */
  }
}
class PaymentAdapter {
  constructor(legacy) {
    this.legacy = legacy;
  }
  pay(total) {
    this.legacy.send(total);
  }
}
```

**Use**: integrating legacy libs; browser vs server APIs.

### 2) Bridge

Separate abstraction from implementation so both vary independently.

```ts
interface Renderer {
  drawCircle(x: number, y: number, r: number): void;
}
class CanvasRenderer implements Renderer {
  /* ... */
}
class SvgRenderer implements Renderer {
  /* ... */
}
class Circle {
  constructor(
    private r: Renderer,
    private x: number,
    private y: number,
    private rad: number
  ) {}
  draw() {
    this.r.drawCircle(this.x, this.y, this.rad);
  }
}
```

**Use**: different rendering backends, database drivers.

### 3) Composite

Tree structures where clients treat individual and groups uniformly.

```ts
interface Node {
  size(): number;
}
class File implements Node {
  constructor(private bytes: number) {}
  size() {
    return this.bytes;
  }
}
class Folder implements Node {
  constructor(private children: Node[]) {}
  size() {
    return this.children.reduce((a, c) => a + c.size(), 0);
  }
}
```

**Use**: DOM, filesystem, scene graphs.

### 4) Decorator

Attach responsibilities dynamically without subclassing.

```ts
interface Service {
  handle(req: any): any;
}
class BaseService implements Service {
  handle(r) {
    return { ok: true, data: r };
  }
}
class LoggingDecorator implements Service {
  constructor(private s: Service) {}
  handle(r) {
    console.time("svc");
    const res = this.s.handle(r);
    console.timeEnd("svc");
    return res;
  }
}
const svc = new LoggingDecorator(new BaseService());
```

**Use**: logging, caching, auth wrappers.

### 5) Facade

Provide a simple interface over a complex subsystem.

```ts
class VideoEncoderFacade {
  constructor(private ffmpeg) {}
  async encode(input: string) {
    /* orchestrate many ffmpeg steps */ return await this.ffmpeg.run([
      "-i",
      input,
      "-preset",
      "fast",
    ]);
  }
}
```

**Use**: simplify complex libs (FFmpeg, AWS SDK flows).

### 6) Flyweight

Share intrinsic state to support large numbers of fine‑grained objects.

```js
// Cache glyph objects by character
class GlyphFactory {
  cache = new Map();
  get(ch) {
    if (!this.cache.has(ch)) this.cache.set(ch, { ch });
    return this.cache.get(ch);
  }
}
```

**Use**: rendering text, UI icons, map tiles.

### 7) Proxy

Surrogate that controls access to another object.

```ts
class Api {
  async getUser(id) {
    /* fetch */
  }
}
class CachingProxy {
  constructor(private api: Api, private cache = new Map()) {}
  async getUser(id) {
    if (this.cache.has(id)) return this.cache.get(id);
    const v = await this.api.getUser(id);
    this.cache.set(id, v);
    return v;
  }
}
```

**Use**: caching, lazy loading, rate limiting, security.

---

## Behavioral Patterns

### 1) Chain of Responsibility

Pass request along a chain until one handles it.

```ts
abstract class Handler {
  next?: Handler;
  setNext(h: Handler) {
    this.next = h;
    return h;
  }
  handle(r) {
    return this.next?.handle(r);
  }
}
class Auth extends Handler {
  handle(r) {
    if (!r.user) throw new Error("401");
    return super.handle(r);
  }
}
class Validate extends Handler {
  handle(r) {
    if (!r.body) throw new Error("400");
    return super.handle(r);
  }
}
class Process extends Handler {
  handle(r) {
    return { ok: true };
  }
}
const pipeline = new Auth().setNext(new Validate()).setNext(new Process());
```

**Use**: Express/Koa middleware, validation pipelines.

### 2) Command

Encapsulate a request as an object (undo/redo, queues).

```ts
interface Command {
  execute(): void;
  undo(): void;
}
class AddTodo implements Command {
  constructor(private store, private text) {}
  execute() {
    this.store.add(this.text);
  }
  undo() {
    this.store.remove(this.text);
  }
}
```

### 3) Interpreter

Define grammar and interpret sentences.

```ts
// Tiny filter language: "status:open AND tag:bug"
// Parse tokens → AST → evaluate over items (omitted parser details)
```

**Use**: search filters, rules engines.

### 4) Iterator

Sequential access without exposing internals.

```ts
function* range(start: number, end: number) {
  for (let i = start; i < end; i++) yield i;
}
for (const n of range(0, 3)) {
  /* 0,1,2 */
}
```

### 5) Mediator

Central object encapsulates how peers interact.

```ts
class ChatRoom {
  users = new Set();
  broadcast(from, msg) {
    for (const u of this.users) if (u !== from) u.receive(msg);
  }
}
```

**Use**: UI widgets communication, CQRS buses.

### 6) Memento

Capture and restore object state (undo).

```ts
class Editor {
  constructor(public text = "") {}
  save() {
    return this.text;
  }
  restore(s) {
    this.text = s;
  }
}
```

### 7) Observer

One‑to‑many notify on state change.

```ts
class Observable {
  observers = new Set();
  subscribe(fn) {
    this.observers.add(fn);
    return () => this.observers.delete(fn);
  }
  next(v) {
    this.observers.forEach((fn) => fn(v));
  }
}
const obs = new Observable();
const unsub = obs.subscribe((v) => console.log(v));
obs.next(42);
unsub();
```

**Use**: RxJS streams, event emitters, UI state.

### 8) State

Object changes behavior when internal state changes.

```ts
class TrafficLight {
  constructor(private state = "red") {}
  next() {
    this.state =
      this.state === "red"
        ? "green"
        : this.state === "green"
        ? "yellow"
        : "red";
  }
  canGo() {
    return this.state === "green";
  }
}
```

### 9) Strategy

Family of algorithms, interchangeable at runtime.

```ts
const strategies = {
  quick: (a) => a.sort(),
  numeric: (a) => a.sort((x, y) => x - y),
};
function sort(arr, mode = "quick") {
  return strategies[mode]([...arr]);
}
```

### 10) Template Method

Define algorithm skeleton; defer steps to subclasses.

```ts
abstract class Job {
  run() {
    this.before();
    this.execute();
    this.after();
  }
  protected before() {}
  protected after() {}
  abstract execute(): void;
}
class ImportJob extends Job {
  execute() {
    /* ... */
  }
}
```

### 11) Visitor

Add operations to object structure without changing classes.

```ts
interface Node {
  accept(v: any): void;
}
class NumberNode implements Node {
  constructor(public v: number) {}
  accept(v) {
    v.visitNumber(this);
  }
}
class PrintVisitor {
  visitNumber(n) {
    console.log(n.v);
  }
}
```

---

## JavaScript‑Native/Architectural Patterns

### Module & Revealing Module

```js
const cart = (function () {
  const items = [];
  function add(i) {
    items.push(i);
  }
  function total() {
    return items.reduce((a, c) => a + c.price, 0);
  }
  return { add, total }; // revealing module exposes only what’s needed
})();
```

### Pub/Sub vs Observer

- **Observer**: subject holds subscribers and notifies directly.
- **Pub/Sub**: broker mediates; publishers and subscribers are decoupled by a topic/event bus (e.g., Node `EventEmitter`, RxJS `Subject`, Kafka/NATS in distributed systems).

### MVC/MVP/MVVM

- **MVC** (Express controllers + services + views).
- **MVVM** (Angular/React with state → view via bindings; ViewModel/Hooks).
- Choose based on framework conventions; keep controllers thin and move logic to services.

### Dependency Injection (DI)

- Angular has DI built-in; in Node use factories or containers (InversifyJS/TSyringe).
- Promotes testability by injecting abstractions.

### Middleware (Pipeline)

- Express/Koa/Axios implement **Chain of Responsibility** for cross‑cutting concerns (auth, logging, rate limits).

### Reactor / Event Loop

- Node’s event loop + non‑blocking I/O: design services with **callbacks/promises/async** and **backpressure** (streams) to scale.

---

## Async & Concurrency Patterns in JS

- **Promises & async/await** → structure async flows.
- **Promise.all / allSettled / race** → coordination patterns.
- **Queues/Workers** (BullMQ, RabbitMQ) → offload long tasks → **Command** jobs.
- **Streams** for backpressure; **circuit breaker**/**retry with jitter** for resilience; **Bulkhead** & **Timeout** patterns in microservices.

---

## Pattern Selection Cheatsheet

- Too many constructors/flags → **Factory/Builder**.
- Many wrappers adding features → **Decorator/Proxy**.
- Need simplified API → **Facade**.
- Incompatible APIs → **Adapter**.
- Variant algorithms → **Strategy**.
- Many steps w/ hooks → **Template Method**.
- Pipeline processing with early exit → **Chain of Responsibility**.
- Reactive UI/events → **Observer/PubSub**.

---

## Testing & Maintainability Tips

- Prefer **interfaces/abstract types** and inject dependencies → easier mocks.
- Keep patterns **small and local**; avoid over‑engineering.
- Add **unit tests** per role: e.g., strategies get their own test suite.
- **Measure** before adopting performance patterns (Flyweight, Caching Proxy).

---

## Anti‑Patterns to Avoid

- **God Object / Manager** doing everything.
- **Singleton abuse** leading to hidden coupling.
- **Primitive Obsession** (use value objects/types).
- **Excessive Inheritance**—prefer composition.
- **Shotgun Surgery** from poor cohesion—refactor to Facade/Builder/Strategy.

---

## Further Reading

- _Design Patterns: Elements of Reusable Object-Oriented Software_ (GoF).
- _Head First Design Patterns_ (Java examples; concepts map to JS).
- _Refactoring_ by Martin Fowler.
- MDN: Modules, Classes, Promises; Node.js docs on EventEmitter & Streams.

---

### Quick Reference Table

| Category   | Pattern                  | When to Use                                 |
| ---------- | ------------------------ | ------------------------------------------- |
| Creational | Singleton                | One instance needed; shared config          |
| Creational | Factory/Abstract Factory | Many related implementations; hide creation |
| Creational | Builder                  | Complex stepwise creation                   |
| Creational | Prototype                | Clone existing objects                      |
| Structural | Adapter                  | Incompatible interfaces                     |
| Structural | Bridge                   | Vary abstraction & implementation           |
| Structural | Composite                | Tree structures (DOM, FS)                   |
| Structural | Decorator                | Add responsibilities at runtime             |
| Structural | Facade                   | Simplify complex subsystems                 |
| Structural | Flyweight                | Large number of similar objects             |
| Structural | Proxy                    | Control access (cache, auth)                |
| Behavioral | Chain of Responsibility  | Pipeline processing/middleware              |
| Behavioral | Command                  | Encapsulate requests; undo/redo             |
| Behavioral | Interpreter              | Parse mini-languages/filters                |
| Behavioral | Iterator                 | Traverse without exposing internals         |
| Behavioral | Mediator                 | Centralize object interactions              |
| Behavioral | Memento                  | Snapshots/undo                              |
| Behavioral | Observer                 | Event/reactive systems                      |
| Behavioral | State                    | Behavior changes with state                 |
| Behavioral | Strategy                 | Switchable algorithms                       |
| Behavioral | Template Method          | Algorithm skeleton w/ hooks                 |
| Behavioral | Visitor                  | New ops over existing structure             |

---

## Real‑World Examples (Quick Recipes)

> Drop‑in snippets you can adapt to Node.js/React/Angular services.

### 1) Chain of Responsibility – Express/Koa Middleware Pipeline

```ts
import express, { Request, Response, NextFunction } from "express";
const app = express();

// Each middleware decides to handle or pass forward
const auth = (req: Request, res: Response, next: NextFunction) => {
  if (!req.headers.authorization) return res.status(401).send("Unauthorized");
  next();
};
const validate = (req: Request, res: Response, next: NextFunction) => {
  if (!req.query.id) return res.status(400).send("Missing id");
  next();
};
const handler = (req: Request, res: Response) =>
  res.json({ ok: true, id: req.query.id });

app.get("/api/resource", auth, validate, handler);
app.listen(3000);
```

### 2) Proxy – Caching Wrapper for Fetch

```ts
class Api {
  async getUser(id: string) {
    const r = await fetch(`https://api.example.com/users/${id}`);
    return r.json();
  }
}
class CachingProxy {
  constructor(
    private api = new Api(),
    private cache = new Map<string, any>(),
    private ttlMs = 10_000
  ) {}
  async getUser(id: string) {
    const hit = this.cache.get(id);
    if (hit && hit.exp > Date.now()) return hit.data;
    const data = await this.api.getUser(id);
    this.cache.set(id, { data, exp: Date.now() + this.ttlMs });
    return data;
  }
}
```

### 3) Decorator – Add Logging and Metrics Around a Service

```ts
interface Service {
  handle(payload: any): Promise<any>;
}
class BaseService implements Service {
  async handle(p) {
    return { ok: true, p };
  }
}
class WithLogging implements Service {
  constructor(private inner: Service) {}
  async handle(p: any) {
    console.time("svc");
    try {
      return await this.inner.handle(p);
    } finally {
      console.timeEnd("svc");
    }
  }
}
const svc: Service = new WithLogging(new BaseService());
```

### 4) Strategy – Pluggable Pricing/Sorting Logic

```ts
type Cart = { items: { price: number; qty: number }[] };
const pricing = {
  standard: (c: Cart) => c.items.reduce((a, i) => a + i.price * i.qty, 0),
  discount10: (c: Cart) => 0.9 * pricing.standard(c),
  tiered: (c: Cart) => {
    const s = pricing.standard(c);
    return s > 1000 ? s * 0.85 : s;
  },
};
function checkout(cart: Cart, mode: keyof typeof pricing = "standard") {
  return pricing[mode](cart);
}
```

### 5) Factory/Builder – HTTP Client with Environment‑Based Variants

```ts
interface Http {
  get(url: string): Promise<any>;
}
class FetchHttp implements Http {
  async get(u) {
    return (await fetch(u)).json();
  }
}
class MockHttp implements Http {
  async get() {
    return { mock: true };
  }
}
function httpFactory(env: "prod" | "test"): Http {
  return env === "prod" ? new FetchHttp() : new MockHttp();
}

class RequestBuilder {
  private url = "";
  private params: Record<string, string> = {};
  withUrl(u: string) {
    this.url = u;
    return this;
  }
  query(k: string, v: string) {
    this.params[k] = v;
    return this;
  }
  build() {
    const q = new URLSearchParams(this.params).toString();
    return `${this.url}?${q}`;
  }
}
const request = new RequestBuilder()
  .withUrl("https://api.example.com/users")
  .query("active", "1")
  .build();
```

### 6) Adapter – Swap Storage Backends (Local vs S3)

```ts
interface Storage {
  put(key: string, bytes: Uint8Array): Promise<void>;
}
class LocalFsStorage implements Storage {
  async put(key, bytes) {
    /* fs.writeFile */
  }
}
class S3Lib {
  async upload(opts: { Key: string; Body: Uint8Array }) {
    /* ... */
  }
}
class S3Adapter implements Storage {
  constructor(private s3 = new S3Lib()) {}
  async put(key: string, bytes: Uint8Array) {
    await this.s3.upload({ Key: key, Body: bytes });
  }
}
// use any Storage without changing calling code
```

### 7) Facade – Simplify a Complex AWS Flow

```ts
class ReportFacade {
  constructor(
    private s3: Storage /* adapter above */,
    private gen: (id: string) => Promise<Uint8Array>
  ) {}
  async generateAndUpload(userId: string) {
    const pdf = await this.gen(userId); // internally messy (db calls, html->pdf)
    await this.s3.put(`reports/${userId}.pdf`, pdf); // single simple call outside
    return `reports/${userId}.pdf`;
  }
}
```

### 8) State – Order Lifecycle

```ts
type OrderStatus = "created" | "paid" | "shipped" | "delivered";
class Order {
  constructor(public status: OrderStatus = "created") {}
  pay() {
    if (this.status !== "created") throw Error("Invalid");
    this.status = "paid";
  }
  ship() {
    if (this.status !== "paid") throw Error("Invalid");
    this.status = "shipped";
  }
  deliver() {
    if (this.status !== "shipped") throw Error("Invalid");
    this.status = "delivered";
  }
}
```

### 9) Command – Undo/Redo for a Store

```ts
interface Command {
  execute(): void;
  undo(): void;
}
class Store {
  items: string[] = [];
  add(t: string) {
    this.items.push(t);
  }
  remove(t: string) {
    this.items = this.items.filter((x) => x !== t);
  }
}
class AddTodo implements Command {
  constructor(private s: Store, private t: string) {}
  execute() {
    this.s.add(this.t);
  }
  undo() {
    this.s.remove(this.t);
  }
}
class Invoker {
  hist: Command[] = [];
  run(c: Command) {
    c.execute();
    this.hist.push(c);
  }
  undo() {
    const c = this.hist.pop();
    c?.undo();
  }
}
```

### 10) Iterator – Async Pagination Helper

```ts
async function* paginate(
  fetchPage: (cursor?: string) => Promise<{ items: any[]; cursor?: string }>
) {
  let cursor: string | undefined = undefined;
  do {
    const { items, cursor: next } = await fetchPage(cursor);
    yield* items;
    cursor = next;
  } while (cursor);
}
```

### 11) Observer / Pub‑Sub – EventEmitter & RxJS

```ts
import { EventEmitter } from "events";
const bus = new EventEmitter();
bus.on("user.created", (u) => console.log("welcome", u.email));
bus.emit("user.created", { email: "vikas@example.com" });
```

```ts
// RxJS flavor (Angular/Node)
import { Subject } from "rxjs";
const subject = new Subject<number>();
const sub = subject.subscribe((v) => console.log("got", v));
subject.next(1);
subject.next(2);
sub.unsubscribe();
```

### 12) Flyweight – Map Markers/Icon Cache

```ts
class IconFactory {
  private cache = new Map<string, HTMLImageElement>();
  get(src: string) {
    if (!this.cache.has(src)) {
      const img = new Image();
      img.src = src;
      this.cache.set(src, img);
    }
    return this.cache.get(src)!;
  }
}
// many markers share same Image instance to save memory
```

### 13) Composite – React Component Trees Treated Uniformly

```tsx
// Composite via children
function Panel({ children }: { children: React.ReactNode }) {
  return <section className="panel">{children}</section>;
}
// Clients compose Panels of Panels or Leaves uniformly
```

### 14) Template Method – Job Skeleton with Hooks

```ts
abstract class Job {
  async run() {
    await this.before();
    await this.execute();
    await this.after();
  }
  protected async before() {}
  protected async after() {}
  protected abstract execute(): Promise<void>;
}
class ImportUsers extends Job {
  protected async execute() {
    /* read csv -> validate -> upsert */
  }
}
```

### 15) Dependency Injection – InversifyJS (Node)

```ts
import "reflect-metadata";
import { Container, injectable, inject } from "inversify";
const TYPES = { Http: Symbol("Http"), UserService: Symbol("UserService") };

interface Http {
  get(u: string): Promise<any>;
}
@injectable()
class FetchHttp implements Http {
  async get(u) {
    return (await fetch(u)).json();
  }
}
@injectable()
class UserService {
  constructor(@inject(TYPES.Http) private http: Http) {}
  list() {
    return this.http.get("/users");
  }
}

const di = new Container();
di.bind<Http>(TYPES.Http).to(FetchHttp);
di.bind<UserService>(TYPES.UserService).to(UserService);
const svc = di.get<UserService>(TYPES.UserService);
```

---

## How These Map to Frontend/Backend

- **Frontend (React/Angular)**: Strategy for sorting/filtering, Observer (RxJS) for streams, State for complex UI flows (wizards), Decorator (HOCs/Custom hooks) for cross‑cutting concerns, Composite is intrinsic to component trees, Facade services to wrap REST/GraphQL.
- **Backend (Node/Microservices)**: CoR for middleware, Proxy for caching/rate‑limit, Circuit Breaker/Retry (resilience), Command for job queues, Builder for queries and requests, Adapter for switching providers (DBs, storage, payments).

> **Tip**: Start simple. When change pressure appears in a specific area (creation/structure/behavior), refactor just that hotspot toward the right pattern.
