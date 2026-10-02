# Modern Java Features (Java 8 -- 21)

> Concise revision guide for experienced developers. Not a textbook.

---

## 1. Java Version Feature Map

| Version    | Year | Key Features                                                                                  |
| ---------- | ---- | --------------------------------------------------------------------------------------------- |
| **8** LTS  | 2014 | Lambdas, Streams, Optional, default methods, `java.time`, `CompletableFuture`                 |
| **9**      | 2017 | Modules (JPMS), `List.of()` / `Set.of()` / `Map.of()`, JShell, private interface methods      |
| **10**     | 2018 | `var` (local variable type inference)                                                         |
| **11** LTS | 2018 | New `String` methods, `HttpClient`, single-file execution (`java App.java`), `var` in lambdas |
| **14**     | 2020 | Records (preview), Switch expressions (final), `NullPointerException` messages                |
| **15**     | 2020 | Text blocks (final), Sealed classes (preview), Hidden classes                                 |
| **16**     | 2021 | Records (final), Pattern matching for `instanceof` (final)                                    |
| **17** LTS | 2021 | Sealed classes (final), enhanced pseudo-random generators                                     |
| **21** LTS | 2023 | Virtual Threads, Pattern matching for `switch`, Record patterns, Sequenced Collections        |

---

## 2. Lambda Expressions (Java 8)

A lambda is an anonymous function targeting a **functional interface** (single abstract method / SAM).

```java
(a, b) -> a + b                    // expression body -- return is implicit
(String s) -> { return s.trim(); } // block body -- explicit return required
() -> System.out.println("hi")     // no params
x -> x * 2                         // single param -- parens optional
```

### Built-in Functional Interfaces

| Interface           | Signature      | Purpose                   | Example                            |
| ------------------- | -------------- | ------------------------- | ---------------------------------- |
| `Runnable`          | `() -> void`   | Fire-and-forget task      | `() -> log("done")`                |
| `Supplier<T>`       | `() -> T`      | Lazy value provider       | `() -> UUID.randomUUID()`          |
| `Consumer<T>`       | `T -> void`    | Side-effect operation     | `s -> System.out.println(s)`       |
| `Function<T,R>`     | `T -> R`       | Transform input to output | `s -> s.length()`                  |
| `Predicate<T>`      | `T -> boolean` | Test / filter             | `s -> s.isEmpty()`                 |
| `UnaryOperator<T>`  | `T -> T`       | Same-type transform       | `s -> s.toUpperCase()`             |
| `BiFunction<T,U,R>` | `(T,U) -> R`   | Two-arg transform         | `(a,b) -> a + b`                   |
| `Comparator<T>`     | `(T,T) -> int` | Ordering                  | `(a,b) -> a.length() - b.length()` |

### Method References

| Kind               | Syntax                | Lambda Equivalent          |
| ------------------ | --------------------- | -------------------------- |
| Static method      | `Integer::parseInt`   | `s -> Integer.parseInt(s)` |
| Instance (bound)   | `str::toUpperCase`    | `() -> str.toUpperCase()`  |
| Instance (unbound) | `String::toUpperCase` | `s -> s.toUpperCase()`     |
| Constructor        | `ArrayList::new`      | `() -> new ArrayList<>()`  |

### vs JS Arrow Functions

| Java Lambda                        | JS Arrow Function             |
| ---------------------------------- | ----------------------------- |
| Must target a functional interface | Standalone value              |
| Cannot capture mutable local vars  | Captures anything via closure |
| No `this` binding issues           | `this` is lexically scoped    |

---

## 3. Streams API (Java 8)

Pipeline: **source** -> **intermediate ops** (lazy) -> **terminal op** (triggers execution).

```java
list.stream()              // from Collection
Stream.of("a", "b", "c")  // from values
Arrays.stream(arr)         // from array
IntStream.range(0, 10)     // primitive stream 0..9
list.parallelStream()      // parallel stream
```

### Intermediate Operations (lazy -- nothing runs until terminal op)

| Op               | Signature                  | Purpose                                  |
| ---------------- | -------------------------- | ---------------------------------------- |
| `filter`         | `Predicate<T>`             | Keep elements matching condition         |
| `map`            | `Function<T,R>`            | Transform each element                   |
| `flatMap`        | `Function<T, Stream<R>>`   | 1-to-many transform, flatten             |
| `sorted`         | `Comparator<T>` (optional) | Sort elements                            |
| `distinct`       | --                         | Remove duplicates (uses `equals`)        |
| `peek`           | `Consumer<T>`              | Debug side-effect, does not alter stream |
| `limit` / `skip` | `long`                     | Take / skip first N elements             |

### Terminal Operations (trigger execution)

| Op                                    | Returns              | Purpose                                                   |
| ------------------------------------- | -------------------- | --------------------------------------------------------- |
| `collect`                             | `R`                  | Mutable reduction (to list, map, etc.)                    |
| `toList()`                            | `List<T>`            | **Java 16+** shorthand for `collect(Collectors.toList())` |
| `forEach`                             | `void`               | Side-effect per element                                   |
| `reduce`                              | `Optional<T>` or `T` | Fold elements into single value                           |
| `count`                               | `long`               | Count elements                                            |
| `findFirst` / `findAny`               | `Optional<T>`        | First element / any (non-deterministic in parallel)       |
| `anyMatch` / `allMatch` / `noneMatch` | `boolean`            | Short-circuit predicate tests                             |

### Collectors

```java
.collect(Collectors.toList())                            // ArrayList
.collect(Collectors.toSet())                             // HashSet
.collect(Collectors.toMap(User::id, User::name))         // HashMap
.collect(Collectors.joining(", "))                       // String concatenation
.collect(Collectors.groupingBy(User::department))        // Map<K, List<V>>
.collect(Collectors.partitioningBy(u -> u.age() > 30))   // Map<Boolean, List<T>>
.collect(Collectors.summarizingInt(User::age))            // sum, avg, min, max, count
```

### Practical Examples

```java
// Filter + map + collect
List<String> emails = users.stream()
    .filter(User::isActive).map(User::email).distinct().toList();

// GroupBy
Map<String, List<User>> byDept = users.stream()
    .collect(Collectors.groupingBy(User::department));

// Reduce
int total = orders.stream().mapToInt(Order::amount).sum();

// FlatMap -- flatten nested lists
List<String> allTags = posts.stream()
    .flatMap(p -> p.getTags().stream()).distinct().sorted().toList();
```

### Parallel Streams

| Use When                        | Avoid When                                   |
| ------------------------------- | -------------------------------------------- |
| Large datasets (10K+ elements)  | Small collections                            |
| CPU-bound, stateless operations | I/O-bound work (use virtual threads instead) |
| Order doesn't matter            | Order-dependent logic                        |
| No shared mutable state         | Shared mutable state / side-effects          |

---

## 4. Optional (Java 8)

Explicit container for a value that may or may not be present. Replaces `null` returns.

```java
Optional.of(value)           // throws NPE if value is null
Optional.ofNullable(value)   // empty if null
Optional.empty()             // explicitly empty
```

### Safe Access

```java
opt.ifPresent(v -> log(v));                       // do something if present
opt.orElse("default");                            // value or fallback
opt.orElseGet(() -> computeDefault());            // value or lazy fallback
opt.orElseThrow(() -> new NotFoundException());   // value or throw
opt.map(String::toUpperCase);                     // transform if present
opt.flatMap(this::findById);                      // chain Optionals
opt.filter(s -> s.length() > 3);                  // conditional unwrap
opt.ifPresentOrElse(v -> use(v), () -> logMiss());// Java 9+
opt.or(() -> Optional.of("backup"));              // Java 9+ fallback Optional
```

### Anti-Patterns

```java
if (opt.isPresent()) { return opt.get(); }     // BAD: defeats the purpose
void process(Optional<String> name) { ... }    // BAD: Optional as parameter
class User { Optional<String> nickname; }      // BAD: Optional as field
Optional<User> findById(long id) { ... }       // GOOD: Optional as return type
```

### vs JS Optional Chaining

| Java Optional                                  | JS `?.`                 |
| ---------------------------------------------- | ----------------------- |
| Explicit wrapper object                        | Language-level syntax   |
| `opt.map(u -> u.address()).map(a -> a.city())` | `user?.address?.city`   |
| Encourages functional pipelines                | Simple property access  |
| Return type contract                           | No contract enforcement |

---

## 5. Records (Java 16)

Immutable data carriers. Compiler generates: canonical constructor, accessors, `equals`, `hashCode`, `toString`.

```java
record Point(int x, int y) {}

var p = new Point(3, 4);
p.x();           // 3 (accessor -- not getX)
p.toString();    // Point[x=3, y=4]

// Custom validation via compact constructor
record Range(int lo, int hi) {
    Range { if (lo > hi) throw new IllegalArgumentException("lo > hi"); }
}

// Additional methods allowed
record User(String name, String email) {
    String domain() { return email.substring(email.indexOf('@') + 1); }
}
```

**Constraints**: all fields `final`; cannot extend classes (implicitly extends `Record`); can implement interfaces; no additional instance fields.

### Cross-Language Comparison

| Java `record`         | Python `@dataclass`                       | JS / TS                      |
| --------------------- | ----------------------------------------- | ---------------------------- |
| Immutable by default  | Mutable by default (`frozen=True` opt-in) | Plain object (fully mutable) |
| Compiler-generated    | Decorator-generated                       | Manual or library            |
| `equals` by value     | `eq=True` by default                      | Reference equality           |
| Cannot extend classes | Can extend / be extended                  | Prototype chain              |

---

## 6. Sealed Classes (Java 17)

Restrict which classes can extend/implement a type. Enables exhaustive pattern matching.

```java
sealed interface Shape permits Circle, Rectangle, Triangle {}
record Circle(double radius) implements Shape {}
record Rectangle(double w, double h) implements Shape {}
final class Triangle implements Shape { /* ... */ }
```

Subclasses must be `final`, `sealed`, or `non-sealed`.

```java
// Exhaustive switch -- no default needed
double area(Shape s) {
    return switch (s) {
        case Circle c    -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.w() * r.h();
        case Triangle t  -> computeTriArea(t);
    };
}
```

Use when: domain has a **closed** set of subtypes (AST nodes, state machines, command types).

---

## 7. Pattern Matching

### instanceof Pattern (Java 16)

```java
// Old: explicit cast
if (obj instanceof String) { String s = (String) obj; s.length(); }

// New: cast + bind in one step
if (obj instanceof String s) { s.length(); }

// Works with && (but not ||)
if (obj instanceof String s && s.length() > 5) { ... }
```

### Switch Pattern (Java 21)

```java
String describe(Object obj) {
    return switch (obj) {
        case Integer i  -> "int: " + i;
        case String s   -> "str: " + s;
        case int[] arr  -> "array len " + arr.length;
        case null       -> "null";
        default         -> "other";
    };
}
```

### Record Patterns (Java 21)

```java
record Point(int x, int y) {}
record Line(Point start, Point end) {}

// Nested deconstruction
String fmt(Object obj) {
    return switch (obj) {
        case Line(Point(var x1, var y1), Point(var x2, var y2))
            -> "(%d,%d)->(%d,%d)".formatted(x1, y1, x2, y2);
        default -> "unknown";
    };
}
```

### Guarded Patterns

```java
switch (obj) {
    case String s when s.length() > 10 -> "long string";
    case String s                      -> "short string";
    default                            -> "not a string";
}
```

---

## 8. Text Blocks (Java 15)

Multi-line string literals using triple quotes.

```java
// Old
String json = "{\n  \"name\": \"Alice\",\n  \"age\": 30\n}";

// New
String json = """
        {
          "name": "Alice",
          "age": 30
        }
        """;

// With formatting (no interpolation -- use .formatted())
String msg = """
        Hello, %s! You have %d messages.
        """.formatted(name, count);
```

**Incidental whitespace**: compiler strips common leading whitespace (determined by closing `"""`).

| Java Text Blocks                      | JS Template Literals     |
| ------------------------------------- | ------------------------ |
| `"""..."""`                           | `` `...` ``              |
| No interpolation (use `.formatted()`) | `${expr}` interpolation  |
| Strips incidental whitespace          | Preserves all whitespace |

---

## 9. `var` Keyword (Java 10)

Local variable type inference. The variable is still **statically typed**.

```java
var list = new ArrayList<String>();   // inferred as ArrayList<String>
var stream = list.stream();           // inferred as Stream<String>
var entry = Map.entry("k", 1);       // inferred as Map.Entry<String, Integer>

// Java 11: var in lambda parameters (enables annotations)
list.forEach((@NonNull var item) -> process(item));
```

| Use                                              | Avoid                                                |
| ------------------------------------------------ | ---------------------------------------------------- |
| `var map = new HashMap<String, List<Integer>>()` | `var result = service.process(data)` -- type unclear |
| `var entry : map.entrySet()` in for-each         | `var x = flag ? getA() : getB()` -- ambiguous        |
| Complex generic types                            | Public API signatures (fields, params, returns)      |

**Not the same as JS `var`**: Java `var` is compile-time inference with full static typing. JS `var` is function-scoped dynamic binding. Closer to TypeScript type inference or Kotlin `val`.

---

## 10. New String Methods (Java 11+)

| Method                               | Version | What It Does                                                   |
| ------------------------------------ | ------- | -------------------------------------------------------------- |
| `isBlank()`                          | 11      | `true` if empty or only whitespace                             |
| `strip()`                            | 11      | Unicode-aware trim (unlike `trim()`)                           |
| `stripLeading()` / `stripTrailing()` | 11      | Strip one side only                                            |
| `lines()`                            | 11      | Returns `Stream<String>` split by line terminators             |
| `repeat(n)`                          | 11      | `"ab".repeat(3)` -> `"ababab"`                                 |
| `indent(n)`                          | 12      | Adjusts indentation by `n` spaces                              |
| `transform(fn)`                      | 12      | Apply function: `"hello".transform(String::toUpperCase)`       |
| `formatted(args)`                    | 15      | Instance version of `String.format`: `"%s=%d".formatted(k, v)` |

---

## 11. java.time API (Java 8)

Immutable, thread-safe replacements for `Date` and `Calendar`.

| Class           | Represents              | Example                                | Use When                        |
| --------------- | ----------------------- | -------------------------------------- | ------------------------------- |
| `LocalDate`     | Date without time       | `2024-03-15`                           | Birthdays, due dates            |
| `LocalTime`     | Time without date       | `14:30:00`                             | Store hours, alarms             |
| `LocalDateTime` | Date + time, no zone    | `2024-03-15T14:30`                     | Timestamps in known context     |
| `ZonedDateTime` | Date + time + zone      | `2024-03-15T14:30+05:30[Asia/Kolkata]` | Cross-timezone scheduling       |
| `Instant`       | Machine timestamp (UTC) | `2024-03-15T09:00:00Z`                 | Logging, DB timestamps, APIs    |
| `Duration`      | Time-based amount       | `PT2H30M`                              | Timeouts, elapsed time          |
| `Period`        | Date-based amount       | `P1Y2M3D`                              | Age calculation, billing cycles |

```java
LocalDate today = LocalDate.now();
LocalDate next = today.plusDays(30);
long daysBetween = ChronoUnit.DAYS.between(start, end);
ZonedDateTime zdt = ZonedDateTime.now(ZoneId.of("America/New_York"));
Instant instant = Instant.now();

// Formatting and parsing
DateTimeFormatter fmt = DateTimeFormatter.ofPattern("dd-MMM-yyyy HH:mm");
String formatted = LocalDateTime.now().format(fmt);  // "15-Mar-2024 14:30"
LocalDate d = LocalDate.parse("15-Mar-2024", DateTimeFormatter.ofPattern("dd-MMM-yyyy"));
```

### Why Not `Date` / `Calendar`

| Problem        | `java.util.Date`                | `java.time`                     |
| -------------- | ------------------------------- | ------------------------------- |
| Mutability     | Mutable (not thread-safe)       | Immutable                       |
| Month indexing | 0-based (Jan = 0)               | 1-based (Jan = 1)               |
| API clarity    | `getYear()` returns year - 1900 | `getYear()` returns actual year |
| Timezone       | No timezone concept             | Explicit zone handling          |

---

## 12. Virtual Threads (Java 21)

Lightweight threads managed by the JVM, not the OS. One process can run millions.

```java
// Create and start
Thread.startVirtualThread(() -> handleRequest());

// Executor -- one virtual thread per task
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 100_000).forEach(i ->
        executor.submit(() -> fetchUrl(urls.get(i)))
    );
}  // auto-waits for all tasks on close

// Structured concurrency (preview)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var user  = scope.fork(() -> fetchUser(id));
    var order = scope.fork(() -> fetchOrder(id));
    scope.join().throwIfFailed();
    return new Response(user.get(), order.get());
}
```

| Aspect              | Platform Thread  | Virtual Thread            |
| ------------------- | ---------------- | ------------------------- |
| Mapped to           | OS thread (1:1)  | JVM-managed (M:N)         |
| Memory              | ~1 MB stack each | ~few KB each              |
| Max practical count | Thousands        | Millions                  |
| Best for            | CPU-bound work   | I/O-bound / blocking work |
| Pooling needed      | Yes              | No (create per task)      |

---

## 13. Sequenced Collections (Java 21)

New interfaces adding first/last access to ordered collections.

```java
collection.getFirst();  collection.getLast();     // SequencedCollection
collection.addFirst(e); collection.addLast(e);
collection.reversed();                            // reversed view
map.firstEntry();       map.lastEntry();          // SequencedMap
map.pollFirstEntry();   map.reversed();
```

---

## 14. Quick Recall

| #   | Topic                   | One-Liner                                                                          |
| --- | ----------------------- | ---------------------------------------------------------------------------------- |
| 1   | Lambda                  | Anonymous function targeting a SAM interface: `(x) -> x + 1`                       |
| 2   | `Function<T,R>`         | Takes `T`, returns `R` -- the workhorse functional interface                       |
| 3   | Stream pipeline         | Source -> lazy intermediates -> terminal op triggers execution                     |
| 4   | `flatMap`               | One-to-many mapping that flattens nested streams/optionals                         |
| 5   | `Collectors.groupingBy` | SQL `GROUP BY` equivalent: returns `Map<K, List<V>>`                               |
| 6   | Optional                | Return type wrapper for nullable values; never use as field or param               |
| 7   | `orElseGet` vs `orElse` | `orElseGet` is lazy (supplier); `orElse` always evaluates fallback                 |
| 8   | Record                  | `record Foo(int x){}` -- immutable DTO with generated equals/hashCode/toString     |
| 9   | Sealed class            | `sealed class X permits A, B` -- closed hierarchy for exhaustive switches          |
| 10  | Pattern matching        | `instanceof String s` binds variable; switch patterns deconstruct records          |
| 11  | Text block              | `"""..."""` -- multi-line string, strips common indent, no interpolation           |
| 12  | `var`                   | Compile-time type inference for locals only; still statically typed                |
| 13  | `java.time`             | `Instant` for machine time, `LocalDate` for human dates, `ZonedDateTime` for zones |
| 14  | Virtual Threads         | Lightweight JVM threads for I/O-bound work; don't pool them, create per task       |
| 15  | Method reference        | `Class::method` -- shorthand for lambda when it just delegates to existing method  |

---

_Last updated: 2025-06_
