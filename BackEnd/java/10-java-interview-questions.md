# Java Interview Questions — 80 Must-Know Q&A

> For experienced developers (Node.js / Python background) targeting senior/architect-level Java roles.
> Answers are intentionally crisp (2-5 lines). Use this as a rapid revision sheet.

---

## Section 1: Core Java (Q1-Q15)

### Q1. What is the difference between JDK, JRE, and JVM?

| Component | What it is |
|-----------|-----------|
| **JVM** | Abstract machine that executes bytecode. Platform-specific. |
| **JRE** | JVM + core libraries. Enough to *run* Java programs. |
| **JDK** | JRE + compiler (`javac`), debugger, and dev tools. Needed to *develop* Java programs. |

---

### Q2. Why is Java platform-independent?

**Answer:** Java source is compiled to **bytecode** (`.class` files), not native machine code. The JVM on each OS interprets or JIT-compiles that bytecode into platform-specific instructions at runtime. The bytecode is the same everywhere; only the JVM differs per platform — hence "write once, run anywhere."

---

### Q3. What is the difference between `==` and `.equals()`?

| Operator | Compares | Typical use |
|----------|----------|-------------|
| `==` | Reference identity (same object in memory) | Primitives, enum comparison |
| `.equals()` | Logical/content equality (overridable) | Strings, wrapper classes, domain objects |

`new String("a") == new String("a")` is `false`; `.equals()` is `true`.

---

### Q4. Why is `String` immutable in Java? What is the string pool?

**Answer:** Immutability allows **string pooling** — the JVM keeps a cache of string literals in a special heap area so identical literals share one object, saving memory. It also makes strings **thread-safe** and safe for use as `HashMap` keys (hashCode is cached). The pool is stored in the JVM's **metaspace** (Java 8+).

---

### Q5. What are the access modifiers and their scope?

| Modifier | Class | Package | Subclass | World |
|----------|:-----:|:-------:|:--------:|:-----:|
| `public` | Y | Y | Y | Y |
| `protected` | Y | Y | Y | N |
| *default* (no keyword) | Y | Y | N | N |
| `private` | Y | N | N | N |

---

### Q6. What is the difference between `abstract class` and `interface`?

| Feature | Abstract class | Interface (Java 8+) |
|---------|---------------|---------------------|
| Instantiation | No | No |
| Constructors | Yes | No |
| State (fields) | Instance variables allowed | Only `public static final` constants |
| Methods | Abstract + concrete | Abstract + `default` + `static` + `private` |
| Inheritance | Single (`extends`) | Multiple (`implements`) |
| Use when | Shared state/base behavior | Capability contract / mix-in |

---

### Q7. Explain method overloading vs overriding.

| Aspect | Overloading | Overriding |
|--------|-------------|------------|
| Binding | Compile-time (static) | Runtime (dynamic / polymorphism) |
| Signature | Same name, different params | Same name + same params |
| Class | Same class or subclass | Subclass only |
| Return type | Can differ | Must be same or covariant |
| Access | Can differ | Cannot be more restrictive |

---

### Q8. What is the `final` keyword used for?

| Applied to | Effect |
|-----------|--------|
| **Variable** | Value cannot be reassigned (constant reference for objects). |
| **Method** | Cannot be overridden by subclasses. |
| **Class** | Cannot be extended. Example: `String`, `Integer`. |

A `final` reference variable can still have its internal state mutated — `final List` can still be `.add()`ed to.

---

### Q9. What are wrapper classes? What is autoboxing?

**Answer:** Wrapper classes (`Integer`, `Double`, `Boolean`, etc.) wrap primitives so they can be used in collections and generics. **Autoboxing** is the compiler automatically converting `int` to `Integer` (and vice versa — **unboxing**). Beware: unboxing a `null` wrapper throws `NullPointerException`, and autoboxing in tight loops causes unnecessary object creation.

---

### Q10. What is the `static` keyword? Can you override static methods?

**Answer:** `static` makes a member belong to the **class**, not an instance. Static methods are resolved at compile time via the reference type. You **cannot override** them — if a subclass declares the same signature, it **hides** (shadows) the parent's method. Static fields are shared across all instances (class-level state).

---

### Q11. What is the `this` and `super` keyword?

| Keyword | Purpose |
|---------|---------|
| `this` | Refers to the current instance. Used to disambiguate fields from params, call another constructor (`this()`). |
| `super` | Refers to the parent class. Used to call parent constructor (`super()`), access overridden methods or hidden fields. |

Both `this()` and `super()` must be the **first statement** in a constructor.

---

### Q12. What is constructor chaining?

**Answer:** Calling one constructor from another using `this()` (same class) or `super()` (parent class). It eliminates duplicate initialization logic. Execution always reaches `Object()` at the top of the chain. If you write no explicit `super()`, the compiler inserts a no-arg `super()` automatically.

---

### Q13. What is the difference between shallow copy and deep copy?

| Type | Behavior |
|------|----------|
| **Shallow** | Copies field values — object references still point to the *same* objects on the heap. |
| **Deep** | Recursively clones all referenced objects so the copy is fully independent. |

`Object.clone()` performs a shallow copy by default. For deep copy, override `clone()` or use serialization / copy constructors.

---

### Q14. What is the `Object` class? Name its important methods.

**Answer:** `Object` is the root superclass of every Java class. Key methods:

| Method | Purpose |
|--------|---------|
| `equals()` | Logical equality |
| `hashCode()` | Hash for hash-based collections |
| `toString()` | String representation |
| `clone()` | Shallow copy (requires `Cloneable`) |
| `getClass()` | Runtime class metadata |
| `wait()` / `notify()` / `notifyAll()` | Thread coordination on the object's monitor |
| `finalize()` | Deprecated cleanup hook (removed in Java 18) |

---

### Q15. What are enums in Java? How are they different from constants?

**Answer:** Enums are full-fledged classes with a fixed set of instances. Unlike `static final int` constants, enums are **type-safe**, can have fields, methods, and constructors, and work with `switch` statements. They implicitly extend `java.lang.Enum`, so they cannot extend another class. Each enum constant is a singleton instance.

---

## Section 2: Collections & Generics (Q16-Q25)

### Q16. What is the Collections hierarchy?

```
Iterable
 └── Collection
      ├── List   → ArrayList, LinkedList, Vector
      ├── Set    → HashSet, LinkedHashSet, TreeSet
      └── Queue  → PriorityQueue, ArrayDeque, LinkedList

Map (separate hierarchy)
 └── HashMap, LinkedHashMap, TreeMap, ConcurrentHashMap, Hashtable
```

`Map` does **not** extend `Collection`.

---

### Q17. ArrayList vs LinkedList — when to use which?

| Criteria | ArrayList | LinkedList |
|----------|-----------|------------|
| Backing structure | Dynamic array | Doubly-linked list |
| Random access (`get(i)`) | O(1) | O(n) |
| Insert/delete at head | O(n) (shift) | O(1) |
| Memory overhead | Lower (contiguous) | Higher (node pointers) |
| Best for | Read-heavy, index-based access | Frequent insert/remove at ends |

In practice, `ArrayList` wins almost always due to CPU cache locality.

---

### Q18. HashMap internals: how does it work?

**Answer:** Internally an **array of buckets**. To put a key: compute `hashCode()`, apply a spread function, index into the array. If the bucket is empty, store the entry. If occupied, chain entries in a **linked list** (or a **red-black tree** when the chain exceeds 8 nodes, Java 8+). Default capacity is 16; load factor is 0.75 — when exceeded, the map **rehashes** (doubles capacity).

---

### Q19. What happens when two keys have the same hashCode?

**Answer:** This is a **hash collision**. Both entries land in the same bucket. `HashMap` stores them in a linked list within that bucket. On `get()`, it walks the chain calling `equals()` on each key to find the right entry. When the chain length exceeds **8**, it converts to a **red-black tree** (O(log n) lookup instead of O(n)).

---

### Q20. HashMap vs ConcurrentHashMap?

| Feature | HashMap | ConcurrentHashMap |
|---------|---------|-------------------|
| Thread-safe | No | Yes |
| Null keys/values | 1 null key, many null values | Neither allowed |
| Locking | None | Segment/bucket-level (CAS + `synchronized`) |
| Iterator | Fail-fast | Weakly consistent |
| Performance (single thread) | Faster | Slightly slower |

---

### Q21. HashSet vs TreeSet vs LinkedHashSet?

| Implementation | Order | Null | Time (add/contains) |
|---------------|-------|------|---------------------|
| `HashSet` | No order guarantee | 1 null | O(1) |
| `LinkedHashSet` | Insertion order | 1 null | O(1) |
| `TreeSet` | Sorted (natural / comparator) | No null | O(log n) |

All enforce uniqueness via `equals()` + `hashCode()` (or `compareTo()` for `TreeSet`).

---

### Q22. What is the `equals()` and `hashCode()` contract?

**Answer:** If `a.equals(b)` is `true`, then `a.hashCode() == b.hashCode()` **must** be `true`. The reverse is not required (collisions are allowed). Breaking this contract corrupts hash-based collections — objects become unfindable in `HashMap`/`HashSet`. Always override **both together**. Use `Objects.hash()` or IDE generators.

---

### Q23. What are Generics? What is type erasure?

**Answer:** Generics add compile-time type safety to collections and classes (`List<String>`). **Type erasure** means the compiler removes all generic type info after compilation — at runtime, `List<String>` and `List<Integer>` are both just `List`. This is why you cannot do `new T()` or `instanceof T`. It exists for backward compatibility with pre-Java-5 code.

---

### Q24. What is the PECS principle?

**Answer:** **P**roducer **E**xtends, **C**onsumer **S**uper.

| Wildcard | Use when | Example |
|----------|----------|---------|
| `<? extends T>` | Reading (producing) items from a structure | `List<? extends Number>` — safe to read as `Number` |
| `<? super T>` | Writing (consuming) items into a structure | `List<? super Integer>` — safe to add `Integer` |

If you both read and write, use an exact type — no wildcard.

---

### Q25. What are fail-fast and fail-safe iterators?

| Type | Behavior | Examples |
|------|----------|----------|
| **Fail-fast** | Throws `ConcurrentModificationException` if collection is modified during iteration. | `ArrayList`, `HashMap` iterators |
| **Fail-safe** | Works on a snapshot or allows concurrent modification; no exception. | `CopyOnWriteArrayList`, `ConcurrentHashMap` iterators |

Fail-safe iterators may not reflect the latest changes.

---

## Section 3: Java 8+ Features (Q26-Q35)

### Q26. What are lambda expressions?

**Answer:** Anonymous function syntax for implementing **functional interfaces** (single abstract method). `(params) -> expression` or `(params) -> { statements; }`. Lambdas capture effectively-final local variables from the enclosing scope. They replaced verbose anonymous inner classes and enabled the Stream API and functional programming style in Java.

---

### Q27. What are the key functional interfaces?

| Interface | Signature | Use case |
|-----------|-----------|----------|
| `Function<T,R>` | `R apply(T t)` | Transform input to output |
| `Predicate<T>` | `boolean test(T t)` | Filter / condition check |
| `Consumer<T>` | `void accept(T t)` | Side-effect operation (e.g., logging) |
| `Supplier<T>` | `T get()` | Lazy value provider / factory |
| `UnaryOperator<T>` | `T apply(T t)` | Transform, same type in and out |
| `BiFunction<T,U,R>` | `R apply(T t, U u)` | Two-input transformation |

All live in `java.util.function`.

---

### Q28. Explain the Stream API pipeline.

**Answer:** A stream pipeline has three stages: **Source** (collection, array, generator), **Intermediate** operations (lazy — `filter`, `map`, `sorted`, `distinct`, `flatMap`), and a **Terminal** operation (triggers execution — `collect`, `forEach`, `reduce`, `count`, `findFirst`). Streams are **single-use**, not data structures — they do not store elements. Intermediate ops return a new stream; terminal ops produce a result or side-effect.

---

### Q29. What is `Optional` and how do you use it correctly?

**Answer:** A container that may or may not hold a non-null value. Use it as a **return type** to signal "might be absent" instead of returning `null`. Prefer `map()`, `orElse()`, `orElseGet()`, `ifPresent()` over `get()`. **Do not** use `Optional` as a field, method parameter, or in collections — it was designed for return values only. Never call `get()` without `isPresent()` or use `orElseThrow()`.

---

### Q30. What are method references?

**Answer:** Shorthand for lambdas that just call an existing method.

| Kind | Syntax | Lambda equivalent |
|------|--------|-------------------|
| Static | `Math::max` | `(a,b) -> Math.max(a,b)` |
| Instance (bound) | `str::toUpperCase` | `() -> str.toUpperCase()` |
| Instance (unbound) | `String::length` | `s -> s.length()` |
| Constructor | `ArrayList::new` | `() -> new ArrayList<>()` |

---

### Q31. What is the difference between `map()` and `flatMap()`?

| Method | Input function returns | Result |
|--------|----------------------|--------|
| `map()` | A single value `R` | `Stream<R>` — one-to-one mapping |
| `flatMap()` | A `Stream<R>` | `Stream<R>` — flattens nested streams into one |

Use `flatMap()` when each element maps to **zero or more** results (e.g., a list of lists). Think of it as map + flatten.

---

### Q32. When should you use parallel streams?

**Answer:** Only when: the data source supports efficient splitting (`ArrayList`, arrays — not `LinkedList`), the operation is CPU-bound and stateless, and the dataset is **large enough** to offset the fork/join overhead. Avoid parallel streams for I/O-bound work, operations with shared mutable state, or when ordering matters. Benchmark before committing — the common `ForkJoinPool` is shared across the JVM.

---

### Q33. What are Records?

**Answer:** Introduced in Java 16, records are **immutable data carriers** with auto-generated `equals()`, `hashCode()`, `toString()`, and accessor methods. `record Point(int x, int y) {}` replaces 30+ lines of boilerplate. Records are `final`, cannot extend other classes (but can implement interfaces), and their fields are `private final`. Think of them as Java's answer to Kotlin data classes or Python `@dataclass`.

---

### Q34. What are Sealed classes?

**Answer:** Introduced in Java 17, sealed classes restrict which classes can extend them using `permits`. `sealed class Shape permits Circle, Rectangle {}`. Subclasses must be `final`, `sealed`, or `non-sealed`. This gives exhaustive pattern matching in `switch` and models closed type hierarchies — the compiler knows all subtypes at compile time.

---

### Q35. What is `var` and when should you use it?

**Answer:** Local variable type inference (Java 10+). The compiler infers the type: `var list = new ArrayList<String>()`. Only for **local variables** with initializers — not fields, method params, or return types. Use when the type is obvious from the right-hand side. Avoid when it reduces readability (e.g., `var x = service.process()` hides the return type).

---

## Section 4: Concurrency (Q36-Q45)

### Q36. How do you create a thread in Java?

**Answer:** Three main ways: (1) extend `Thread` and override `run()`, (2) implement `Runnable` and pass to `new Thread(runnable)`, (3) implement `Callable<V>` and submit to an `ExecutorService`. Prefer `Runnable`/`Callable` with executor pools over raw `Thread` — it decouples task from execution policy and enables thread reuse.

---

### Q37. What is the difference between `Runnable` and `Callable`?

| Feature | `Runnable` | `Callable<V>` |
|---------|-----------|---------------|
| Return value | `void` | Returns `V` via `Future` |
| Checked exceptions | Cannot throw | Can throw |
| Submit to | `Thread` or `ExecutorService` | `ExecutorService` only |

Use `Callable` when you need a result or must propagate checked exceptions.

---

### Q38. What does `synchronized` do?

**Answer:** Acquires the **intrinsic lock** (monitor) of the specified object, ensuring that only one thread executes the synchronized block/method at a time. It provides both **mutual exclusion** and **memory visibility** (changes made inside are visible to the next thread that enters). Can be applied to methods (locks `this` or `ClassName.class` for static) or explicit blocks (`synchronized(obj) {}`).

---

### Q39. What is `volatile`?

**Answer:** A field modifier that guarantees **visibility** — every read sees the latest write from any thread (no CPU cache staleness). It does **not** provide atomicity for compound operations like `count++`. Use `volatile` for simple flags (e.g., `volatile boolean running`). For atomic increments, use `AtomicInteger` or `synchronized`.

---

### Q40. What is a deadlock? How do you prevent it?

**Answer:** Two or more threads each hold a lock and wait for a lock held by the other, so none can proceed. Prevention strategies: (1) always acquire locks in a **consistent global order**, (2) use `tryLock()` with timeouts (`ReentrantLock`), (3) avoid nested locks when possible, (4) use higher-level concurrency utilities (`ConcurrentHashMap`, `ExecutorService`). Detect with thread dumps or `jstack`.

---

### Q41. What is `ExecutorService`?

**Answer:** A higher-level replacement for manually managing threads. It manages a thread pool and accepts `Runnable`/`Callable` tasks. Factory methods: `Executors.newFixedThreadPool(n)`, `newCachedThreadPool()`, `newSingleThreadExecutor()`. Returns `Future<V>` for async results. Always `shutdown()` when done. In production, prefer `ThreadPoolExecutor` with explicit queue and rejection policy over convenience factory methods.

---

### Q42. What is `CompletableFuture`?

**Answer:** An async programming API (Java 8+) similar to JavaScript `Promise`. Supports chaining (`thenApply`, `thenCompose`, `thenAccept`), combining (`allOf`, `anyOf`), and exception handling (`exceptionally`, `handle`). Runs on `ForkJoinPool.commonPool()` by default or a custom executor. Enables non-blocking pipelines without callback hell.

| JS Promise | CompletableFuture |
|------------|-------------------|
| `.then()` | `.thenApply()` / `.thenCompose()` |
| `.catch()` | `.exceptionally()` |
| `Promise.all()` | `CompletableFuture.allOf()` |

---

### Q43. What are Virtual Threads (Java 21)?

**Answer:** Lightweight threads managed by the JVM, not the OS. You can spawn millions without exhausting OS thread limits. They are ideal for **I/O-bound** tasks (HTTP calls, DB queries). Created via `Thread.ofVirtual().start(runnable)` or `Executors.newVirtualThreadPerTaskExecutor()`. They use **carrier threads** (platform threads) underneath and unmount during blocking I/O. Think of them as Java's answer to Go goroutines.

---

### Q44. What is the difference between `ConcurrentHashMap` and `Collections.synchronizedMap()`?

| Aspect | `synchronizedMap` | `ConcurrentHashMap` |
|--------|-------------------|---------------------|
| Locking | Single lock on entire map | Bucket-level CAS + fine-grained locks |
| Read concurrency | Blocked during writes | Lock-free reads |
| Iteration | Must manually synchronize | Weakly consistent, no exception |
| Null keys/values | Allowed | Not allowed |
| Performance | Poor under contention | High throughput |

---

### Q45. What are atomic variables?

**Answer:** Classes in `java.util.concurrent.atomic` (`AtomicInteger`, `AtomicLong`, `AtomicReference`, etc.) that provide **lock-free, thread-safe** operations using CPU **CAS (Compare-And-Swap)** instructions. Methods like `incrementAndGet()`, `compareAndSet()`, `getAndUpdate()` are atomic without `synchronized`. Use them for counters, flags, and simple shared state.

---

## Section 5: JVM & Memory (Q46-Q52)

### Q46. Explain JVM memory areas.

| Area | Stores | Thread scope |
|------|--------|-------------|
| **Heap** | Objects, arrays | Shared |
| **Stack** | Frames (local vars, operand stack, method calls) | Per-thread |
| **Metaspace** | Class metadata, method bytecode (replaced PermGen in Java 8) | Shared |
| **PC Register** | Address of current instruction | Per-thread |
| **Native Method Stack** | Native (JNI) method frames | Per-thread |

---

### Q47. What is garbage collection? How does generational GC work?

**Answer:** GC automatically reclaims memory occupied by unreachable objects. **Generational hypothesis**: most objects die young. The heap is divided into **Young Gen** (Eden + Survivor spaces) and **Old Gen**. New objects go to Eden; surviving minor GCs promote to Survivor, then Old Gen. Minor GCs (Young) are fast and frequent; Major/Full GCs (Old) are slower and less frequent.

---

### Q48. What is the difference between stack and heap?

| Stack | Heap |
|-------|------|
| Stores primitives + object references | Stores actual objects |
| Per-thread, LIFO | Shared across threads |
| Fast allocation/deallocation | Managed by GC |
| Fixed size (`-Xss`), `StackOverflowError` on overflow | Configurable (`-Xms`, `-Xmx`), `OutOfMemoryError` on overflow |
| Automatically freed when method returns | Freed when no references remain |

---

### Q49. What are GC roots?

**Answer:** The starting points the GC uses to determine which objects are **reachable** (alive). GC roots include: local variables in active stack frames, static fields of loaded classes, active threads, JNI references, and objects used by `synchronized` monitors. Any object not reachable from a GC root (directly or transitively) is eligible for collection.

---

### Q50. What GC algorithms does Java offer?

| Collector | Type | Best for |
|-----------|------|----------|
| **Serial** | Single-threaded, stop-the-world | Small apps, single-core |
| **Parallel (Throughput)** | Multi-threaded STW | Batch processing, max throughput |
| **G1** (default since Java 9) | Region-based, concurrent | General purpose, balanced latency/throughput |
| **ZGC** | Concurrent, ultra-low pause (<1ms) | Large heaps, latency-sensitive |
| **Shenandoah** | Concurrent compaction | Low-latency (RedHat) |

---

### Q51. What is a memory leak in Java? Common causes?

**Answer:** Objects that are still referenced but never used again, preventing GC from reclaiming them. Common causes: (1) static collections growing unbounded, (2) unclosed resources (connections, streams), (3) listeners/callbacks not deregistered, (4) inner classes holding references to outer class, (5) custom `ClassLoader` issues. Diagnose with heap dumps + tools like Eclipse MAT or VisualVM.

---

### Q52. What JVM tuning flags should you know?

| Flag | Purpose |
|------|---------|
| `-Xms` / `-Xmx` | Initial / max heap size |
| `-Xss` | Thread stack size |
| `-XX:+UseG1GC` / `-XX:+UseZGC` | Select GC algorithm |
| `-XX:MaxGCPauseMillis=200` | Target max GC pause (G1) |
| `-XX:+HeapDumpOnOutOfMemoryError` | Dump heap on OOM for post-mortem |
| `-XX:MetaspaceSize` | Initial metaspace size |
| `-Xlog:gc*` | GC logging (Java 9+ unified logging) |

---

## Section 6: Exception Handling (Q53-Q57)

### Q53. Checked vs unchecked exceptions?

| Type | Superclass | Compile-time check | Examples |
|------|-----------|-------------------|----------|
| **Checked** | `Exception` (not `RuntimeException`) | Must catch or declare `throws` | `IOException`, `SQLException` |
| **Unchecked** | `RuntimeException` | No requirement | `NullPointerException`, `IllegalArgumentException` |
| **Error** | `Error` | Should not catch | `OutOfMemoryError`, `StackOverflowError` |

Modern practice favors unchecked exceptions for application logic; checked for recoverable I/O operations.

---

### Q54. What is try-with-resources?

**Answer:** Syntax (Java 7+) that auto-closes any resource implementing `AutoCloseable` when the `try` block exits (normally or via exception). `try (var conn = getConnection()) { ... }`. Eliminates boilerplate `finally` blocks. If both the try body and `close()` throw, the close exception is added as a **suppressed** exception (retrievable via `getSuppressed()`).

---

### Q55. Can you catch multiple exceptions in one catch block?

**Answer:** Yes, since Java 7: `catch (IOException | SQLException e) { ... }`. The variable `e` is implicitly `final`. The exceptions must not be in a parent-child relationship (catching `Exception | IOException` is a compile error since `IOException` is already a subtype of `Exception`). This reduces duplicate catch logic.

---

### Q56. What is the difference between `throw` and `throws`?

| Keyword | Purpose | Where used |
|---------|---------|------------|
| `throw` | Actually throws an exception object | Inside method body: `throw new IllegalArgumentException("bad")` |
| `throws` | Declares that a method *may* throw checked exceptions | Method signature: `void read() throws IOException` |

---

### Q57. Should you create custom exceptions? When?

**Answer:** Yes, when you need domain-specific error semantics that standard exceptions do not convey (e.g., `InsufficientFundsException`, `UserNotFoundException`). Extend `RuntimeException` for unchecked or `Exception` for checked. Include meaningful messages and relevant context fields. Avoid creating an exception per error — group related errors under a common custom exception with an error code or enum.

---

## Section 7: Spring Boot (Q58-Q65)

### Q58. What is Spring Boot and how does it differ from Spring?

**Answer:** Spring Boot is an **opinionated layer** on top of the Spring Framework that eliminates boilerplate XML/Java configuration. It provides **auto-configuration**, an embedded server (Tomcat/Jetty), starter dependencies, and production-ready features (actuator, health checks). Spring is the core DI/AOP framework; Spring Boot is the fast-start convention-over-configuration wrapper.

---

### Q59. What is Dependency Injection? Types?

**Answer:** DI is an IoC pattern where the container provides dependencies instead of the class creating them. Spring supports three types:

| Type | Annotation | Recommended? |
|------|-----------|-------------|
| **Constructor** | `@Autowired` on constructor (optional if single) | Yes — immutable, testable |
| **Setter** | `@Autowired` on setter | For optional dependencies |
| **Field** | `@Autowired` on field directly | No — hard to test, hides dependencies |

---

### Q60. What are bean scopes?

| Scope | Lifecycle |
|-------|-----------|
| `singleton` (default) | One instance per Spring container |
| `prototype` | New instance per injection / request |
| `request` | One per HTTP request (web only) |
| `session` | One per HTTP session (web only) |
| `application` | One per `ServletContext` |

Injecting a `prototype` into a `singleton` gives the same prototype instance — use `ObjectProvider` or `@Lookup` to get a fresh one each time.

---

### Q61. What is auto-configuration?

**Answer:** Spring Boot scans the classpath and automatically configures beans based on what libraries are present. For example, if `spring-boot-starter-data-jpa` and an H2 driver are on the classpath, it auto-configures a `DataSource`, `EntityManagerFactory`, and transaction manager. Driven by `@EnableAutoConfiguration` and `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`. Override with explicit bean definitions or `application.properties`.

---

### Q62. How does `@ControllerAdvice` work?

**Answer:** A global exception handler for all `@Controller`/`@RestController` classes. Methods annotated with `@ExceptionHandler` inside a `@ControllerAdvice` class catch exceptions thrown by any controller. You can also use `@ModelAttribute` and `@InitBinder` globally. Combine with `ResponseEntityExceptionHandler` for consistent error response formatting across the API.

---

### Q63. What is Spring Data JPA? How do query methods work?

**Answer:** An abstraction over JPA/Hibernate that generates repository implementations from interfaces. Extend `JpaRepository<Entity, ID>` and declare methods like `findByEmailAndStatus(String email, Status status)` — Spring parses the method name and generates the JPQL query at startup. For complex queries, use `@Query("SELECT u FROM User u WHERE ...")`. Supports pagination (`Pageable`), sorting, and projections.

---

### Q64. What is the difference between `@Component`, `@Service`, `@Repository`?

| Annotation | Semantic meaning | Extra behavior |
|-----------|-----------------|----------------|
| `@Component` | Generic Spring-managed bean | None |
| `@Service` | Business/service layer | None (documentation only) |
| `@Repository` | Data access layer | Automatic **exception translation** (SQL exceptions to Spring's `DataAccessException`) |

All three are `@Component` specializations and are picked up by component scanning.

---

### Q65. How do you test a Spring Boot application?

| Layer | Tools / Annotations |
|-------|-------------------|
| **Unit** (no Spring) | JUnit 5 + Mockito — mock dependencies, test logic |
| **Slice** (partial context) | `@WebMvcTest` (controllers), `@DataJpaTest` (repos), `@WebFluxTest` |
| **Integration** (full context) | `@SpringBootTest` + `@AutoConfigureMockMvc` or `TestRestTemplate` |
| **Contract** | Spring Cloud Contract or Pact |

Use `@MockBean` to replace beans in the context. Keep unit tests fast; integration tests focused.

---

## Section 8: Spring Security (Q66-Q72)

### Q66. How does Spring Security work internally?

**Answer:** It inserts a **filter chain** (`SecurityFilterChain`) into the servlet filter pipeline. Each request passes through filters like `UsernamePasswordAuthenticationFilter`, `BearerTokenAuthenticationFilter`, `ExceptionTranslationFilter`, `AuthorizationFilter`. The `AuthenticationManager` delegates to `AuthenticationProvider`s which use `UserDetailsService` to load user data. The result is stored in the `SecurityContextHolder` (ThreadLocal).

---

### Q67. How do you configure JWT authentication?

**Answer:** (1) Disable session creation (`SessionCreationPolicy.STATELESS`). (2) Add a custom `OncePerRequestFilter` that extracts the JWT from the `Authorization: Bearer` header, validates it (signature, expiration), and sets the `Authentication` in `SecurityContextHolder`. (3) Configure the `SecurityFilterChain` to add this filter before `UsernamePasswordAuthenticationFilter`. Use libraries like `jjwt` or `nimbus-jose-jwt` for token parsing.

---

### Q68. What is the difference between `@PreAuthorize` and `@Secured`?

| Feature | `@PreAuthorize` | `@Secured` |
|---------|----------------|-----------|
| SpEL support | Yes — `@PreAuthorize("hasRole('ADMIN') and #id == principal.id")` | No |
| Expressions | Role, permission, method args, custom | Role names only |
| Flexibility | High | Low |
| Enable via | `@EnableMethodSecurity` | `@EnableMethodSecurity(securedEnabled = true)` |

Prefer `@PreAuthorize` for its expressiveness.

---

### Q69. When should you enable/disable CSRF?

**Answer:** **Enable** CSRF protection for browser-based apps that use cookies/sessions (the default). **Disable** for stateless REST APIs that use JWT/token auth in headers — no cookies means no CSRF risk. Disable via `http.csrf(csrf -> csrf.disable())`. If your API is consumed by both browsers (with cookies) and mobile clients, consider token-based CSRF (double-submit cookie pattern).

---

### Q70. How do you implement CORS?

**Answer:** Three approaches: (1) `@CrossOrigin` on a controller or method for fine-grained control. (2) Global config via `WebMvcConfigurer.addCorsMappings()` for all endpoints. (3) In the `SecurityFilterChain` via `http.cors(cors -> cors.configurationSource(...))` — required when Spring Security is active, as the security filter chain runs before MVC. Define allowed origins, methods, headers, and max age.

---

### Q71. How do you store passwords securely?

**Answer:** Never store plain text. Use `BCryptPasswordEncoder` (Spring Security's default recommendation) which applies a **salt + adaptive hash**. Register it as a `@Bean` of type `PasswordEncoder`. Spring Security automatically uses it during authentication. `BCrypt` is intentionally slow (configurable strength/rounds) to resist brute-force attacks. Alternatives: `Argon2PasswordEncoder`, `SCryptPasswordEncoder`.

---

### Q72. What is OAuth2 and how does Spring support it?

**Answer:** OAuth2 is an authorization framework that lets users grant third-party apps limited access without sharing credentials. Roles: Resource Owner, Client, Authorization Server, Resource Server. Spring provides: `spring-boot-starter-oauth2-client` (login with Google/GitHub), `spring-boot-starter-oauth2-resource-server` (validate JWT tokens from an auth server). Configure via `application.yml` with provider/issuer URIs. For your own auth server, use **Spring Authorization Server**.

---

## Section 9: Design & Architecture (Q73-Q80)

### Q73. Name the SOLID principles with one-liner explanations.

| Principle | Meaning |
|-----------|---------|
| **S** - Single Responsibility | A class should have only one reason to change. |
| **O** - Open/Closed | Open for extension, closed for modification. |
| **L** - Liskov Substitution | Subtypes must be substitutable for their base types without breaking behavior. |
| **I** - Interface Segregation | Many specific interfaces are better than one general-purpose interface. |
| **D** - Dependency Inversion | Depend on abstractions, not concretions. High-level modules should not depend on low-level modules. |

---

### Q74. What is the Singleton pattern? How does Spring implement it?

**Answer:** Ensures a class has exactly one instance. In classic Java: private constructor + static instance (use enum for thread safety). In Spring, the **default bean scope is singleton** — one instance per application context, managed by the container. Spring's singleton is per-container, not per-classloader like the GoF pattern. No need for double-checked locking — the container handles it.

---

### Q75. What is the Strategy pattern? Where is it used in Java/Spring?

**Answer:** Defines a family of interchangeable algorithms behind a common interface. The client delegates to the strategy without knowing the implementation. In Java: `Comparator` is a strategy for sorting. In Spring: inject different implementations of an interface by qualifier or profile — e.g., switching between `S3StorageService` and `LocalStorageService` via `@Profile`.

---

### Q76. What is the Observer pattern? Spring's implementation?

**Answer:** A subject notifies multiple observers when its state changes (pub-sub). In Spring: publish domain events via `ApplicationEventPublisher.publishEvent(event)` and listen with `@EventListener` or `@TransactionalEventListener` methods. Events are synchronous by default; add `@Async` for async. Decouples producers from consumers within the same application context.

---

### Q77. What is the Template Method pattern?

**Answer:** Defines the skeleton of an algorithm in a base class, deferring specific steps to subclasses. The base class calls abstract/hook methods that subclasses override. In Spring/Java: `JdbcTemplate` (handles connection/exception boilerplate, you supply the SQL + mapper), `HttpServlet` (`service()` dispatches to `doGet()`/`doPost()`), `AbstractApplicationContext.refresh()`.

---

### Q78. What is the Proxy pattern? How does `@Transactional` use it?

**Answer:** A proxy wraps a target object to add behavior (logging, security, transactions) without modifying the target. Spring creates **AOP proxies** (JDK dynamic proxy for interfaces, CGLIB subclass proxy for classes) around beans annotated with `@Transactional`. The proxy intercepts the method call, begins a transaction, delegates to the real method, and commits/rolls back. This is why calling `@Transactional` methods from within the same class bypasses the proxy and does not apply transactions.

---

### Q79. What is the Builder pattern? Why is it popular in Java?

**Answer:** Separates object construction from representation, allowing step-by-step creation of complex objects. Popular because Java lacks named/default parameters (unlike Python/Kotlin). `StringBuilder`, `HttpClient.newBuilder()`, and Lombok's `@Builder` are common examples. Produces immutable objects with readable construction: `User.builder().name("A").email("b").build()`.

---

### Q80. What anti-patterns should you avoid?

| Anti-pattern | Problem |
|-------------|---------|
| **God class** | One class does everything — violates SRP |
| **Service locator** | Hides dependencies; prefer DI |
| **Anemic domain model** | Entities are data bags; all logic in services |
| **Catching `Exception`/`Throwable`** | Swallows unexpected errors, hides bugs |
| **Premature optimization** | Complex code for unproven performance gains |
| **Circular dependencies** | A depends on B depends on A — redesign with events or interfaces |
| **N+1 queries** | Lazy loading in loops — use `JOIN FETCH` or `@EntityGraph` |
| **Distributed monolith** | Microservices with tight coupling — worst of both worlds |

---

## Self-Test Checklist

Before your interview, make sure you can confidently explain each of these:

- [ ] JVM memory model: heap, stack, metaspace, and how GC works
- [ ] `HashMap` internals: hashing, buckets, collisions, tree-ification
- [ ] `equals()` and `hashCode()` contract and what breaks when violated
- [ ] Generics, type erasure, and PECS
- [ ] Stream API: lazy evaluation, intermediate vs terminal, when to parallelize
- [ ] `CompletableFuture` chaining and error handling
- [ ] `synchronized` vs `volatile` vs `AtomicInteger`
- [ ] Virtual threads vs platform threads and when to use each
- [ ] Checked vs unchecked exceptions and modern best practices
- [ ] Spring bean lifecycle: instantiation, dependency injection, `@PostConstruct`, destroy
- [ ] Spring Security filter chain and how JWT auth is wired
- [ ] `@Transactional` proxy behavior and why self-invocation skips it
- [ ] SOLID principles with real Spring/Java examples
- [ ] Singleton, Strategy, Observer, Proxy patterns in Spring context
- [ ] Difference between `@Component`, `@Service`, `@Repository`, `@Controller`
- [ ] Spring Data JPA query derivation and `@Query`
- [ ] GC algorithms: G1 vs ZGC, when to pick which
- [ ] Common JVM tuning flags for production
- [ ] OAuth2 roles and Spring's support for client + resource server
- [ ] Anti-patterns: N+1 queries, god class, circular dependencies

---

*Last updated: 2025. Keep answers short, keep concepts deep.*