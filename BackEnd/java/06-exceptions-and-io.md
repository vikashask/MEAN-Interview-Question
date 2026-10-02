# Exceptions and I/O

> Java's compile-time exception checking is the biggest shift from JS/Python. I/O is verbose but predictable once you learn the stream/reader split and NIO.2.

---

## 1. Exception Hierarchy

```
Throwable
├── Error (don't catch — JVM is dying)
│   ├── OutOfMemoryError
│   ├── StackOverflowError
│   └── VirtualMachineError
└── Exception
    ├── Checked (must handle or declare)
    │   ├── IOException
    │   ├── SQLException
    │   ├── FileNotFoundException
    │   └── InterruptedException
    └── RuntimeException (unchecked — compiler ignores)
        ├── NullPointerException
        ├── ArrayIndexOutOfBoundsException
        ├── IllegalArgumentException
        ├── ClassCastException
        ├── ArithmeticException
        └── UnsupportedOperationException
```

Key rule: if it extends `Exception` but NOT `RuntimeException`, it is checked.

---

## 2. Checked vs Unchecked

| Aspect              | Checked                                  | Unchecked (RuntimeException)            |
|----------------------|------------------------------------------|-----------------------------------------|
| Compiler enforced?   | Yes -- must `catch` or `throws`          | No                                      |
| Represents           | Recoverable external failures            | Programming bugs                        |
| Examples             | `IOException`, `SQLException`            | `NullPointerException`, `ClassCastException` |
| When to use (custom) | Caller can reasonably recover            | Caller made a mistake                   |
| JS/Python equivalent | None -- those languages have no concept  | All exceptions in JS/Python are unchecked |

```java
// Checked — compiler forces you to handle it
public String readFile(Path p) throws IOException {   // <-- must declare
    return Files.readString(p);
}

// Unchecked — compiler says nothing
public int divide(int a, int b) {
    return a / b;  // ArithmeticException if b == 0, but no declaration needed
}
```

---

## 3. Exception Handling Patterns

### try-catch-finally

```java
FileReader fr = null;
try {
    fr = new FileReader("data.txt");
    // read...
} catch (FileNotFoundException e) {
    log.error("File missing: {}", e.getMessage());
} finally {
    if (fr != null) fr.close();  // always runs — old-school cleanup
}
```

### try-with-resources (Java 7+) -- preferred

Resource must implement `AutoCloseable`. Closes automatically, even on exception. Equivalent to Python's `with` statement.

```java
try (var reader = new BufferedReader(new FileReader("data.txt"));
     var writer = new BufferedWriter(new FileWriter("out.txt"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        writer.write(line);
        writer.newLine();
    }
}  // both closed here automatically, in reverse order
```

### Multi-catch (Java 7+)

```java
try {
    riskyOperation();
} catch (IOException | SQLException e) {   // single block for multiple types
    log.error("Operation failed", e);       // e is effectively final
}
```

### throws declaration

```java
// Propagate checked exceptions up the call stack
public void process() throws IOException, ParseException {
    // ...
}
```

### Custom exceptions

```java
// Checked — extend Exception
public class OrderNotFoundException extends Exception {
    public OrderNotFoundException(String id) {
        super("Order not found: " + id);
    }
}

// Unchecked — extend RuntimeException
public class InvalidConfigException extends RuntimeException {
    public InvalidConfigException(String key) {
        super("Bad config key: " + key);
    }
}
```

### Best practices

| Practice                      | Why                                                    |
|-------------------------------|--------------------------------------------------------|
| Catch specific exceptions     | `catch (Exception e)` hides bugs                       |
| Don't swallow exceptions      | Empty catch blocks lose diagnostic info                 |
| Throw early, catch late       | Validate inputs at entry; handle at the boundary        |
| Log with context              | Include IDs, params -- not just `e.getMessage()`        |
| Use custom exceptions         | Encapsulate domain errors with meaningful types         |
| Prefer unchecked for APIs     | Checked exceptions leak implementation details          |

---

## 4. Common Anti-Patterns

```java
// 1. Catching too broadly
try { ... } catch (Exception e) { ... }      // hides bugs, catches RuntimeExceptions too

// 2. Swallowing exceptions
try { ... } catch (IOException e) { }        // silent failure — worst pattern

// 3. Exceptions for control flow
try {                                        // use Optional or conditional checks instead
    int val = Integer.parseInt(input);
} catch (NumberFormatException e) {
    val = defaultValue;
}

// 4. Log-and-rethrow (causes double-logging up the stack)
catch (IOException e) {
    log.error("Failed", e);
    throw e;                                 // pick one: log OR rethrow, not both
}

// 5. Throwing Exception instead of specific type
public void process() throws Exception { }   // tells caller nothing useful
```

---

## 5. Java I/O Streams

Two families: **byte streams** (binary) and **character streams** (text). Always wrap in buffered variants.

| Class Family    | Base Classes                    | Buffered Wrapper                    | Use For          |
|-----------------|---------------------------------|-------------------------------------|------------------|
| Byte streams    | `InputStream` / `OutputStream`  | `BufferedInputStream` / `BufferedOutputStream` | Binary (images, serialized objects) |
| Character streams | `Reader` / `Writer`           | `BufferedReader` / `BufferedWriter` | Text (UTF-aware) |

### Read file line-by-line (classic)

```java
try (var br = new BufferedReader(new FileReader("data.csv"))) {
    String line;
    while ((line = br.readLine()) != null) {
        process(line);
    }
}
```

### Files utility class (Java 7+) -- modern approach

```java
// Read entire file as String (Java 11+)
String content = Files.readString(Path.of("data.txt"));

// Read all lines into List
List<String> lines = Files.readAllLines(Path.of("data.txt"), StandardCharsets.UTF_8);

// Write string to file
Files.writeString(Path.of("out.txt"), content, StandardOpenOption.CREATE);

// Lazy stream of lines (for large files)
try (Stream<String> stream = Files.lines(Path.of("huge.log"))) {
    stream.filter(l -> l.contains("ERROR"))
          .forEach(System.out::println);
}
```

---

## 6. NIO (Java NIO.2)

### Path vs File

| Aspect     | `java.io.File` (legacy)        | `java.nio.file.Path` (Java 7+)          |
|------------|--------------------------------|------------------------------------------|
| Immutable  | No                             | Yes                                      |
| Error info | Returns `false` on failure     | Throws descriptive exceptions            |
| Resolve    | `new File(parent, child)`      | `parent.resolve(child)`                  |
| Preferred  | No                             | Yes -- always use `Path`                 |

```java
Path p = Path.of("/Users", "app", "config.json");   // factory method
Path resolved = p.getParent().resolve("backup.json");
boolean exists = Files.exists(p);
```

### Files operations cheat sheet

```java
Files.copy(src, dst, StandardCopyOption.REPLACE_EXISTING);
Files.move(src, dst, StandardCopyOption.ATOMIC_MOVE);
Files.delete(path);                          // throws if missing
Files.deleteIfExists(path);                  // returns boolean
Files.createDirectories(Path.of("a/b/c"));   // mkdir -p
long size = Files.size(path);
```

### Channel and Buffer (high-performance)

Used for non-blocking I/O and memory-mapped files. Rarely needed in typical applications.

```java
try (FileChannel ch = FileChannel.open(path, StandardOpenOption.READ)) {
    ByteBuffer buf = ByteBuffer.allocate(1024);
    while (ch.read(buf) > 0) {
        buf.flip();       // switch from write-mode to read-mode
        // process buf...
        buf.clear();
    }
}
```

### WatchService (file system events)

```java
WatchService watcher = FileSystems.getDefault().newWatchService();
Path dir = Path.of("./watched");
dir.register(watcher, ENTRY_CREATE, ENTRY_MODIFY, ENTRY_DELETE);

while (true) {
    WatchKey key = watcher.take();   // blocks until event
    for (WatchEvent<?> event : key.pollEvents()) {
        System.out.println(event.kind() + ": " + event.context());
    }
    key.reset();
}
```

### When to use what

| Scenario                    | Use                                        |
|-----------------------------|--------------------------------------------|
| Read/write text files       | `Files.readString()` / `Files.writeString()` |
| Large file, line-by-line    | `Files.lines()` (Stream) or `BufferedReader` |
| Binary / image copy         | `Files.copy()` or `InputStream` + buffer   |
| High-throughput server I/O  | NIO `Channel` + `Buffer` + `Selector`      |
| File system watching        | `WatchService`                             |

---

## 7. Serialization

### Java built-in (legacy)

```java
public class User implements Serializable {
    private static final long serialVersionUID = 1L;  // version control for deserialization
    private String name;
    private transient String password;                 // excluded from serialization
}
```

| Concept            | Detail                                                        |
|--------------------|---------------------------------------------------------------|
| `Serializable`     | Marker interface (no methods) -- enables `ObjectOutputStream` |
| `serialVersionUID` | If class changes and UID doesn't match, deserialization fails |
| `transient`        | Field is skipped during serialization (nulled on deserialize) |
| Security risk      | Deserializing untrusted data can execute arbitrary code       |

### Modern alternatives -- prefer these

| Library            | Format         | Notes                                    |
|--------------------|----------------|------------------------------------------|
| Jackson            | JSON           | Industry standard, annotation-driven     |
| Gson               | JSON           | Simpler API, Google                      |
| Protocol Buffers   | Binary         | Schema-first, cross-language, compact    |
| Avro               | Binary / JSON  | Schema evolution, Hadoop ecosystem       |

```java
// Jackson example
ObjectMapper mapper = new ObjectMapper();
String json = mapper.writeValueAsString(user);         // serialize
User u = mapper.readValue(json, User.class);           // deserialize
```

Rule of thumb: never use Java's built-in serialization for new code. Use Jackson for REST APIs, Protobuf for inter-service communication.

---

## 8. Quick Recall

| #  | Point                                                                       |
|----|-----------------------------------------------------------------------------|
| 1  | `Throwable` -> `Error` (don't catch) + `Exception` (handle)                |
| 2  | Checked = extends `Exception`; Unchecked = extends `RuntimeException`       |
| 3  | Checked must be caught or declared with `throws` -- compiler enforced       |
| 4  | `try-with-resources` auto-closes `AutoCloseable` -- always prefer this      |
| 5  | Multi-catch: `catch (A \| B e)` -- single block, multiple exception types   |
| 6  | Byte streams (`InputStream`) for binary; `Reader` for text -- always buffer |
| 7  | `Files.readString()` / `Files.lines()` -- modern file I/O since Java 11/7  |
| 8  | Use `Path` not `File`; use `Files` utility for all file operations          |
| 9  | NIO Channels + Buffers for high-perf; `WatchService` for FS events          |
| 10 | `transient` excludes fields from serialization                              |
| 11 | Never use Java serialization for new code -- use Jackson or Protobuf        |
| 12 | Throw early (validate inputs), catch late (at service boundaries)           |
