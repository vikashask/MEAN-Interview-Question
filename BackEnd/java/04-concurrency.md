# Java Concurrency — Architect-Level Revision Guide

> For experienced developers coming from Node.js/Python. Not a textbook — a recall sheet.

---

## 1. Threading Model: Java vs Node.js vs Python

| Aspect      | Java                             | Node.js                                        | Python (CPython)                                       |
| ----------- | -------------------------------- | ---------------------------------------------- | ------------------------------------------------------ |
| Model       | True multi-threading, OS threads | Single-threaded event loop + libuv worker pool | Multi-threaded but GIL serializes CPU work             |
| Parallelism | Yes — multiple cores natively    | No (single thread); `worker_threads` for CPU   | No real parallelism via threads; use `multiprocessing` |
| Concurrency | Threads, pools, virtual threads  | `async/await`, callbacks, Promises             | `asyncio`, threads (I/O only), `multiprocessing`       |
| Best for    | CPU + I/O bound workloads        | I/O bound, high-connection servers             | I/O bound (threads), CPU bound (multiprocessing)       |

**One-liner:** Java gives you real OS-level parallelism out of the box. Node fakes it with an event loop. Python's GIL makes threads useful only for I/O.

---

## 2. Thread Basics

```java
// 1. Extend Thread (tight coupling — avoid)
class MyThread extends Thread {
    public void run() { System.out.println("running"); }
}
new MyThread().start();

// 2. Implement Runnable (preferred — separates task from thread)
Runnable task = () -> System.out.println("running");
new Thread(task).start();

// 3. Implement Callable<T> (returns a value, throws checked exceptions)
Callable<Integer> callable = () -> 42;
Future<Integer> f = Executors.newSingleThreadExecutor().submit(callable);
int result = f.get(); // blocks until done
```

| Approach         | Returns value?    | Throws checked exception? | Use with ExecutorService? |
| ---------------- | ----------------- | ------------------------- | ------------------------- |
| `extends Thread` | No                | No                        | No                        |
| `Runnable`       | No                | No                        | Yes                       |
| `Callable<T>`    | Yes (`Future<T>`) | Yes                       | Yes                       |

### Thread Lifecycle

`NEW` -> `RUNNABLE` -> `RUNNING` -> `TERMINATED`. From RUNNABLE a thread can enter `BLOCKED` (waiting for lock), `WAITING` (wait/join), or `TIMED_WAITING` (sleep/timed-wait).

### Key Methods

| Method             | What it does                                                               |
| ------------------ | -------------------------------------------------------------------------- |
| `start()`          | Creates new OS thread, invokes `run()` — **always call this**              |
| `run()`            | Just a normal method call on the same thread — no concurrency              |
| `Thread.sleep(ms)` | Pauses current thread; does NOT release locks                              |
| `join()`           | Caller blocks until target thread finishes                                 |
| `interrupt()`      | Sets interrupt flag; sleeping/waiting threads throw `InterruptedException` |

### Daemon Threads

`t.setDaemon(true)` before `start()`. JVM exits when only daemon threads remain. Use for background services (GC, logging).

---

## 3. Synchronization

### `synchronized` Keyword

```java
// Method-level: locks on `this` (or Class object for static)
public synchronized void increment() { count++; }

// Block-level: finer control, locks on specified object
public void increment() {
    synchronized (this) { count++; }
}
```

Every Java object has an **intrinsic lock** (monitor). Only one thread holds it at a time.

### wait / notify / notifyAll

Must be called inside a `synchronized` block on the same object.

```java
// Producer-Consumer pattern (simplified)
synchronized (queue) {
    while (queue.isEmpty()) queue.wait();   // releases lock, waits
    item = queue.poll();
}

synchronized (queue) {
    queue.add(item);
    queue.notifyAll();                      // wakes all waiting threads
}
```

| Method        | Behavior                                      |
| ------------- | --------------------------------------------- |
| `wait()`      | Releases lock, thread sleeps until notified   |
| `notify()`    | Wakes one waiting thread (non-deterministic)  |
| `notifyAll()` | Wakes all waiting threads (preferred — safer) |

### Deadlock

Two threads each hold a lock the other needs. Classic ABBA problem.

```
Thread-1: locks A, then tries to lock B
Thread-2: locks B, then tries to lock A
// Both stuck forever
```

**Avoidance:** consistent lock ordering, `tryLock()` with timeout, avoid nested locks.

### ReentrantLock

```java
ReentrantLock lock = new ReentrantLock(true); // fair = true
lock.lock();
try {
    // critical section
} finally {
    lock.unlock(); // ALWAYS in finally
}

// Non-blocking attempt
if (lock.tryLock(1, TimeUnit.SECONDS)) {
    try { /* work */ } finally { lock.unlock(); }
}
```

| Feature               | `synchronized`    | `ReentrantLock`             |
| --------------------- | ----------------- | --------------------------- |
| Explicit unlock       | No (auto)         | Yes (`finally` block)       |
| `tryLock()` / timeout | No                | Yes                         |
| Fairness policy       | No                | Yes (constructor flag)      |
| Multiple conditions   | No (one wait-set) | Yes (`newCondition()`)      |
| Interruptible         | No                | Yes (`lockInterruptibly()`) |

### ReadWriteLock

`ReentrantReadWriteLock` — `readLock()` allows concurrent readers; `writeLock()` is exclusive. Use when reads vastly outnumber writes (caches, config).

---

## 4. volatile Keyword

`volatile` guarantees **visibility** across threads — reads always see the latest write. It does NOT guarantee atomicity.

```java
private volatile boolean running = true; // all threads see updates immediately

public void stop() { running = false; }  // safe — single writer, flag pattern
public void run() {
    while (running) { /* work */ }        // guaranteed to see stop()
}
```

| Aspect     | `volatile`           | `synchronized`                             |
| ---------- | -------------------- | ------------------------------------------ |
| Visibility | Yes                  | Yes                                        |
| Atomicity  | No                   | Yes                                        |
| Blocking   | No                   | Yes                                        |
| Use case   | Flags, status fields | Compound actions (`check-then-act`, `i++`) |

**Rule of thumb:** Use `volatile` for simple boolean flags with one writer. Use `synchronized` or atomics for anything else.

---

## 5. Atomic Classes

`java.util.concurrent.atomic` — lock-free, thread-safe operations using CAS (Compare-And-Swap).

```java
AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();           // atomic i++
counter.compareAndSet(5, 10);        // if value==5, set to 10
counter.getAndUpdate(x -> x * 2);    // atomic custom operation

AtomicReference<String> ref = new AtomicReference<>("initial");
ref.compareAndSet("initial", "updated");
```

| Class                          | Use case                                          |
| ------------------------------ | ------------------------------------------------- |
| `AtomicInteger` / `AtomicLong` | Counters, sequences                               |
| `AtomicBoolean`                | Flags                                             |
| `AtomicReference<T>`           | Lock-free reference swaps                         |
| `LongAdder`                    | High-contention counters (faster than AtomicLong) |

**CAS under the hood:** Read current value, compute new value, swap only if current hasn't changed. Retry on failure. No locking.

---

## 6. ExecutorService (Thread Pools)

Creating threads is expensive. Pools reuse a fixed set of threads and control concurrency.

| Factory Method              | Pool Behavior                            | Use Case                    |
| --------------------------- | ---------------------------------------- | --------------------------- |
| `newFixedThreadPool(n)`     | Exactly `n` threads, unbounded queue     | Known, stable workload      |
| `newCachedThreadPool()`     | 0 to unlimited threads, 60s idle timeout | Many short-lived tasks      |
| `newSingleThreadExecutor()` | 1 thread, tasks execute sequentially     | Sequential task guarantee   |
| `newScheduledThreadPool(n)` | `n` threads, supports delay/periodic     | Cron-like, polling, retries |

### Usage

```java
ExecutorService pool = Executors.newFixedThreadPool(4);

// Submit Runnable
pool.submit(() -> System.out.println("task"));

// Submit Callable — returns Future
Future<String> future = pool.submit(() -> fetchData());
String result = future.get();                    // blocks
String result = future.get(5, TimeUnit.SECONDS); // blocks with timeout

// Batch operations
List<Future<String>> results = pool.invokeAll(callables);  // waits for all
String fastest = pool.invokeAny(callables);                // first to finish
```

### Proper Shutdown

```java
pool.shutdown();                                    // stop accepting, finish queued
if (!pool.awaitTermination(60, TimeUnit.SECONDS))
    pool.shutdownNow();                             // interrupt running tasks
```

---

## 7. CompletableFuture (Java 8+)

Async programming without callback hell. **Direct parallel to JavaScript Promises.**

```java
CompletableFuture<String> cf = CompletableFuture.supplyAsync(() -> fetchData());
CompletableFuture<Void>   cf = CompletableFuture.runAsync(() -> doWork());
```

### Chaining

```java
CompletableFuture.supplyAsync(() -> getUserId())
    .thenApply(id -> fetchUser(id))           // map: T -> U
    .thenAccept(user -> log(user))            // consume: T -> void
    .exceptionally(ex -> { log(ex); return null; });
```

### Composition

```java
// Sequential: thenCompose (flatMap) — like Promise.then() returning a Promise
CompletableFuture<Order> order = getUserAsync()
    .thenCompose(user -> getOrderAsync(user));

// Parallel: thenCombine — wait for both, combine results
CompletableFuture<Summary> summary = priceAsync
    .thenCombine(stockAsync, (price, stock) -> new Summary(price, stock));

// Wait for all / any
CompletableFuture.allOf(cf1, cf2, cf3).join();
CompletableFuture.anyOf(cf1, cf2, cf3).thenAccept(first -> use(first));
```

### Error Handling

```java
cf.exceptionally(ex -> fallbackValue);        // recover from error
cf.handle((res, ex) -> ex != null ? fallback : transform(res)); // always runs
```

### CompletableFuture vs JavaScript Promise

| Java                     | JavaScript                     | Notes                  |
| ------------------------ | ------------------------------ | ---------------------- |
| `supplyAsync(() -> val)` | `new Promise(resolve => ...)`  | Start async work       |
| `thenApply(fn)`          | `.then(fn)`                    | Transform result       |
| `thenCompose(fn)`        | `.then(fn)` returning Promise  | Flatten nested futures |
| `thenCombine(other, fn)` | `Promise.all([a,b]).then(...)` | Combine two results    |
| `exceptionally(fn)`      | `.catch(fn)`                   | Error recovery         |
| `allOf(...)`             | `Promise.all(...)`             | Wait for all           |
| `anyOf(...)`             | `Promise.race(...)`            | First to complete      |
| `cf.join()`              | `await promise`                | Block until done       |

### Practical Example: Parallel API Calls

```java
var userFuture  = CompletableFuture.supplyAsync(() -> userService.get(id));
var orderFuture = CompletableFuture.supplyAsync(() -> orderService.get(id));

CompletableFuture.allOf(userFuture, orderFuture).join();

var profile = new Profile(userFuture.join(), orderFuture.join());
```

---

## 8. Concurrent Collections

| Collection              | Behavior                                                            | Use Case                                    |
| ----------------------- | ------------------------------------------------------------------- | ------------------------------------------- |
| `ConcurrentHashMap`     | Segment-level locking; lock-free reads                              | Shared mutable maps (default choice)        |
| `CopyOnWriteArrayList`  | Copy entire array on write; lock-free reads                         | Read-heavy, rare writes (listeners, config) |
| `LinkedBlockingQueue`   | Bounded/unbounded; `put()` blocks if full, `take()` blocks if empty | Producer-consumer                           |
| `ArrayBlockingQueue`    | Bounded, backed by array; fair ordering option                      | Bounded producer-consumer                   |
| `ConcurrentLinkedQueue` | Lock-free, unbounded, non-blocking                                  | High-throughput non-blocking queue          |
| `ConcurrentSkipListMap` | Concurrent sorted map                                               | Sorted concurrent access                    |

### Why Not `Collections.synchronizedMap()`?

| Aspect              | `synchronizedMap`                                    | `ConcurrentHashMap`                          |
| ------------------- | ---------------------------------------------------- | -------------------------------------------- |
| Lock granularity    | Entire map (one global lock)                         | Per-segment / per-bucket                     |
| Read concurrency    | Blocked by writers                                   | Lock-free reads                              |
| Compound operations | Not atomic (check-then-act unsafe)                   | Atomic: `putIfAbsent()`, `computeIfAbsent()` |
| Iterator            | Fail-fast (throws `ConcurrentModificationException`) | Weakly consistent (safe)                     |
| Performance         | Poor under contention                                | Excellent under contention                   |

---

## 9. Virtual Threads (Java 21)

Lightweight threads scheduled by the JVM, not the OS. Think **goroutines** or Node.js async — but with blocking code style.

### Creation

```java
// Direct creation
Thread.ofVirtual().start(() -> handleRequest());

// Named
Thread vt = Thread.ofVirtual().name("worker").unstarted(() -> task());
vt.start();

// Via ExecutorService (preferred for servers)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 100_000).forEach(i ->
        executor.submit(() -> blockingHttpCall(i))
    );
} // auto-shutdown on close
```

### When to Use vs When to Avoid

| Use (I/O bound)            | Avoid                                      |
| -------------------------- | ------------------------------------------ |
| HTTP calls, DB queries     | CPU-intensive computation                  |
| File I/O, network sockets  | `synchronized` blocks (causes **pinning**) |
| High-concurrency servers   | Thread-local heavy code                    |
| Microservice orchestration | When you need OS thread guarantees         |

**Pinning:** Virtual threads get pinned to carrier (OS) threads inside `synchronized` blocks. Use `ReentrantLock` instead to avoid this.

### Impact on Spring Boot

Spring Boot 3.2+: set `spring.threads.virtual.enabled=true`. Every request gets its own virtual thread. Blocking I/O (JDBC, RestTemplate) no longer wastes OS threads — millions of concurrent requests without reactive programming.

---

## 10. Common Concurrency Pitfalls

| Pitfall                                  | What Happens                                               | Fix                                                 |
| ---------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------- |
| **Race condition**                       | Multiple threads read/write shared state unsafely          | Synchronize, use atomics, or concurrent collections |
| **Deadlock**                             | Two+ threads waiting on each other's locks forever         | Consistent lock ordering, `tryLock()` with timeout  |
| **Starvation**                           | Thread never gets CPU time (low priority, unfair lock)     | Fair locks, avoid priority manipulation             |
| **Memory visibility**                    | Thread reads stale cached value                            | `volatile`, `synchronized`, atomics                 |
| **Thread-local + virtual threads**       | ThreadLocal accumulates across millions of virtual threads | Use scoped values (`ScopedValue` in Java 21+)       |
| **Forgetting to shutdown pool**          | App hangs on exit; threads keep running                    | Always `shutdown()` + `awaitTermination()`          |
| **Catching InterruptedException poorly** | Swallowing it breaks interrupt contract                    | Re-interrupt: `Thread.currentThread().interrupt()`  |

---

## 11. Quick Recall

| #   | One-Liner                                                                                                     |
| --- | ------------------------------------------------------------------------------------------------------------- |
| 1   | `start()` creates a new thread; `run()` is just a method call on the current thread.                          |
| 2   | Every Java object has an intrinsic lock (monitor) used by `synchronized`.                                     |
| 3   | `volatile` = visibility only. For `i++` you need `AtomicInteger` or `synchronized`.                           |
| 4   | `wait()`/`notify()` must be inside `synchronized` on the same object.                                         |
| 5   | `ReentrantLock` over `synchronized` when you need `tryLock()`, fairness, or multiple conditions.              |
| 6   | `ConcurrentHashMap` > `synchronizedMap` — finer locking, atomic compound ops, no fail-fast iterators.         |
| 7   | `CompletableFuture.supplyAsync()` is Java's `Promise`. `thenCompose` = flatMap, `thenCombine` = zip.          |
| 8   | Always shut down ExecutorService: `shutdown()` then `awaitTermination()` then `shutdownNow()`.                |
| 9   | Virtual threads (Java 21) are cheap; use for I/O-bound. Avoid `synchronized` (pinning) — use `ReentrantLock`. |
| 10  | Deadlock fix: always acquire locks in the same global order.                                                  |
| 11  | `CopyOnWriteArrayList` is perfect for read-heavy, write-rare scenarios (event listeners).                     |
| 12  | `LongAdder` outperforms `AtomicLong` under high contention — use for metrics/counters.                        |

---

_Last updated: 2025-01_
