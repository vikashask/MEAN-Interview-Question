# Java Design Patterns -- Architect-Level Revision Guide

> For experienced Node.js/Python devs learning Java patterns.
> Java's strict type system (interfaces, abstract classes, generics) makes patterns more explicit than dynamic languages.
> Spring Framework itself is a pattern showcase: DI, Proxy, Template Method, Factory, Observer -- all baked in.

---

## 1. Why Patterns Matter in Java

| Reason                         | Detail                                                                        |
| ------------------------------ | ----------------------------------------------------------------------------- |
| Type system enforces contracts | Interfaces and abstract classes give patterns compile-time safety             |
| Spring is patterns             | You already use 10+ patterns daily if you use Spring Boot                     |
| Interview vocabulary           | Architect interviews expect you to name, compare, and justify pattern choices |
| Refactoring language           | "Extract a Strategy" or "Wrap with Decorator" is precise, shared shorthand    |

---

## 2. Creational Patterns

### Singleton

One instance globally. Java: `private` constructor + static access; Spring beans are singletons by default.

```java
// Enum singleton -- simplest, thread-safe, serialization-safe
public enum AppConfig {
    INSTANCE;
    private final Map<String, String> props = new HashMap<>();
    public String get(String key) { return props.get(key); }
}
// Usage: AppConfig.INSTANCE.get("db.url");
```

| When to use | Config holders, connection pools, caches                          |
| ----------- | ----------------------------------------------------------------- |
| In Spring   | `@Component` is singleton by default -- you rarely write your own |
| Pitfall     | Mutable singletons + multithreading = bugs                        |

### Factory Method

Define an interface for creating objects; subclasses decide which concrete class to instantiate.

```java
public class NotificationFactory {
    public Notification create(String type) {
        return switch (type) {
            case "email" -> new EmailNotification();
            case "sms"   -> new SmsNotification();
            default      -> throw new IllegalArgumentException(type);
        };
    }
}
```

| When to use | Object creation logic varies by type/config                              |
| ----------- | ------------------------------------------------------------------------ |
| In Spring   | `BeanFactory` is the core factory; `@Bean` methods are factory methods   |
| vs JS       | In JS you'd just use a plain function; Java formalizes with an interface |

### Abstract Factory

Factory of factories -- create families of related objects without specifying concrete classes.

```java
public interface UIFactory {
    Button createButton();
    TextField createTextField();
}
public class DarkThemeFactory implements UIFactory {
    public Button createButton()       { return new DarkButton(); }
    public TextField createTextField()  { return new DarkTextField(); }
}
```

| When to use | Multiple product families that must stay consistent        |
| ----------- | ---------------------------------------------------------- |
| In Spring   | `FactoryBean<T>` lets you control bean instantiation logic |

### Builder

Construct complex objects step by step. Extremely common in Java (compensates for no named parameters).

```java
// With Lombok -- one annotation does it all
@Builder @Value
public class Person {
    String name;
    int age;
    String email;
}
// Usage: Person.builder().name("Alice").age(30).email("a@b.com").build();
```

```java
// Manual builder (interview-ready)
public class Person {
    private final String name;
    private final int age;
    private Person(Builder b) { this.name = b.name; this.age = b.age; }
    public static class Builder {
        private String name; private int age;
        public Builder name(String n) { this.name = n; return this; }
        public Builder age(int a)     { this.age = a; return this; }
        public Person build()         { return new Person(this); }
    }
}
```

| When to use | >3 constructor params, optional fields, immutable objects          |
| ----------- | ------------------------------------------------------------------ |
| In Spring   | `WebClient.builder()`, Spring Security DSL, `UriComponentsBuilder` |
| Lombok      | `@Builder` + `@Value` = immutable builder in 5 lines               |

### Prototype

Clone existing objects instead of creating from scratch.

```java
public class ServerConfig implements Cloneable {
    String host; int port; Map<String, String> props;
    @Override
    public ServerConfig clone() {
        ServerConfig copy = new ServerConfig();
        copy.host = this.host; copy.port = this.port;
        copy.props = new HashMap<>(this.props); // deep copy
        return copy;
    }
}
```

| When to use | Expensive object creation; need copies with slight modifications |
| ----------- | ---------------------------------------------------------------- |
| In Spring   | `@Scope("prototype")` -- new instance per injection point        |
| Pitfall     | `clone()` default is shallow copy; must deep-copy mutable fields |

---

## 3. Structural Patterns

### Adapter

Convert one interface to another so incompatible classes can work together.

```java
public class LegacyPrinter { void printText(String s) { /*...*/ } }
public interface Printer { void print(String s); }

public class PrinterAdapter implements Printer {
    private final LegacyPrinter legacy = new LegacyPrinter();
    public void print(String s) { legacy.printText(s); }
}
```

| When to use | Integrating third-party libs, legacy code migration                                 |
| ----------- | ----------------------------------------------------------------------------------- |
| In Spring   | `HandlerAdapter` adapts different handler types to `DispatcherServlet`              |
| In JDK      | `Arrays.asList()` adapts array to `List`; `InputStreamReader` adapts bytes to chars |

### Decorator

Add behavior dynamically by wrapping objects -- same interface, enhanced functionality.

```java
// Classic JDK I/O -- decorators stacking
BufferedReader br = new BufferedReader(     // decorator 2
    new InputStreamReader(                  // decorator 1
        new FileInputStream("data.txt")));  // base
```

```java
// Custom decorator
public class LoggingService implements OrderService {
    private final OrderService delegate;
    public LoggingService(OrderService d) { this.delegate = d; }
    public void place(Order o) {
        log.info("Placing order {}", o.getId());
        delegate.place(o);
    }
}
```

| When to use    | Cross-cutting concerns without modifying original class         |
| -------------- | --------------------------------------------------------------- |
| In Spring      | `BeanPostProcessor` wraps/decorates beans during initialization |
| vs Inheritance | Decorator composes at runtime; inheritance is compile-time      |

### Proxy

Control access to an object -- add lazy init, security, logging, transactions.

```java
// JDK dynamic proxy (interface-based)
OrderService proxy = (OrderService) Proxy.newProxyInstance(
    OrderService.class.getClassLoader(),
    new Class[]{OrderService.class},
    (obj, method, args) -> {
        log.info("Before: {}", method.getName());
        Object result = method.invoke(realService, args);
        log.info("After: {}", method.getName());
        return result;
    });
```

| When to use  | AOP, lazy loading, access control, remote calls                            |
| ------------ | -------------------------------------------------------------------------- |
| In Spring    | `@Transactional`, `@Async`, `@Cacheable` all create proxies (JDK or CGLIB) |
| JDK vs CGLIB | JDK proxy = interface-based; CGLIB = subclass-based (no interface needed)  |

### Facade

Simplified interface to a complex subsystem -- hide wiring details.

```java
// Without facade: caller juggles Connection, Statement, ResultSet, try-catch
// With facade (Spring's JdbcTemplate):
List<User> users = jdbcTemplate.query(
    "SELECT * FROM users WHERE active = ?",
    new BeanPropertyRowMapper<>(User.class), true);
```

| When to use | Simplify complex APIs, provide a clean entry point          |
| ----------- | ----------------------------------------------------------- |
| In Spring   | `JdbcTemplate`, `RestTemplate`, `WebClient` are all facades |

### Composite

Treat individual objects and compositions uniformly -- tree structures.

```java
public interface FileSystemNode { long getSize(); }

public class File implements FileSystemNode {
    private long size;
    public long getSize() { return size; }
}
public class Directory implements FileSystemNode {
    private List<FileSystemNode> children = new ArrayList<>();
    public long getSize() {
        return children.stream().mapToLong(FileSystemNode::getSize).sum();
    }
}
```

| When to use | Tree-like structures: menus, org charts, file systems |
| ----------- | ----------------------------------------------------- |
| In JDK      | `java.awt.Component` / `Container`                    |

### Bridge

Decouple abstraction from implementation so both can vary independently.

```java
// Shape has-a Color; both hierarchies evolve independently
public abstract class Shape {
    protected Color color;
    abstract void draw();
}
public interface Color { String fill(); }
// Square + Red, Square + Blue -- no class explosion
```

| When to use | Prevent class explosion from multiple independent dimensions         |
| ----------- | -------------------------------------------------------------------- |
| In JDK      | JDBC `DriverManager` (abstraction) + vendor drivers (implementation) |

---

## 4. Behavioral Patterns

### Strategy

Swap algorithms at runtime by injecting different implementations.

```java
// JDK: Comparator IS a strategy
names.stream().sorted(Comparator.comparingInt(String::length)).toList();

// Spring: inject strategy by qualifier
@Service("stripe")  class StripePayment implements PaymentStrategy { /*...*/ }
@Service("paypal")  class PaypalPayment implements PaymentStrategy { /*...*/ }
@Autowired @Qualifier("stripe") PaymentStrategy payment;
```

| When to use | Multiple algorithms for same task; avoid if/else chains    |
| ----------- | ---------------------------------------------------------- |
| In Spring   | Inject all: `@Autowired List<PaymentStrategy> strategies`  |
| vs JS       | In JS you'd pass a function; Java wraps it in an interface |

### Observer

Pub-sub: when one object changes, dependents are notified.

```java
public class OrderPlacedEvent extends ApplicationEvent {
    private final String orderId;
    public OrderPlacedEvent(Object src, String id) { super(src); this.orderId = id; }
}

@Component
public class NotificationListener {
    @EventListener
    public void onOrderPlaced(OrderPlacedEvent e) {
        log.info("Notify for order: {}", e.getOrderId());
    }
}
```

| When to use | Decouple event producers from consumers                       |
| ----------- | ------------------------------------------------------------- |
| In Spring   | `ApplicationEventPublisher.publishEvent()` + `@EventListener` |
| Async       | Add `@Async` to listener for non-blocking                     |

### Template Method

Define algorithm skeleton in a base class; subclasses override specific steps.

```java
public abstract class DataProcessor {
    public final void process() {  // final -- subclasses can't change flow
        readData();
        transform();
        writeData();
    }
    abstract void readData();
    abstract void transform();
    abstract void writeData();
}
public class CsvProcessor extends DataProcessor {
    void readData()  { /* parse CSV */ }
    void transform() { /* clean rows */ }
    void writeData() { /* write to DB */ }
}
```

| When to use | Fixed algorithm structure with variable steps                  |
| ----------- | -------------------------------------------------------------- |
| In Spring   | `JdbcTemplate.execute()`, `RestTemplate`, `AbstractController` |

### Iterator

Traverse a collection without exposing its internal structure.

```java
List<String> items = List.of("a", "b", "c");
for (String s : items) { /* enhanced for-loop uses Iterator under the hood */ }

Iterator<String> it = items.iterator();
while (it.hasNext()) { System.out.println(it.next()); }
```

| When to use | Any sequential traversal; Java Streams are an evolution |
| ----------- | ------------------------------------------------------- |
| In JDK      | `Iterator<T>`, `Iterable<T>`, `Spliterator<T>`          |

### Command

Encapsulate a request as an object -- decouple sender from executor.

```java
ExecutorService pool = Executors.newFixedThreadPool(4);
pool.submit(() -> processOrder(orderId));   // lambda = command
pool.submit(() -> sendEmail(userId));       // another command
pool.shutdown();
```

| When to use | Task queues, undo/redo, macro recording        |
| ----------- | ---------------------------------------------- |
| In JDK      | `Runnable`, `Callable<T>`, `CompletableFuture` |

### Chain of Responsibility

Pass request through a chain of handlers; each decides to process or pass along.

```java
public abstract class Handler {
    private Handler next;
    public Handler setNext(Handler h) { this.next = h; return h; }
    public void handle(Request req) {
        if (!canHandle(req) && next != null) next.handle(req);
    }
    abstract boolean canHandle(Request req);
}
// AuthHandler -> RateLimitHandler -> LoggingHandler -> Controller
```

| When to use | Middleware-style processing (like Express middleware)         |
| ----------- | ------------------------------------------------------------- |
| In Spring   | Security `FilterChain`, Servlet `Filter`, Spring Interceptors |

### State

Object behavior changes when its internal state changes -- avoids massive switch blocks.

```java
public interface OrderState {
    void next(OrderContext ctx);
    void cancel(OrderContext ctx);
}
public class PendingState implements OrderState {
    public void next(OrderContext ctx)   { ctx.setState(new ShippedState()); }
    public void cancel(OrderContext ctx) { ctx.setState(new CancelledState()); }
}
// OrderContext delegates to current state; no if/else chains
```

| When to use | Entities with well-defined state transitions (orders, workflows)             |
| ----------- | ---------------------------------------------------------------------------- |
| vs Strategy | Strategy = caller chooses algorithm; State = object changes its own behavior |

---

## 5. Patterns in Spring Boot -- Summary Table

| Pattern         | Where in Spring                | Example                           |
| --------------- | ------------------------------ | --------------------------------- |
| Singleton       | Default bean scope             | `@Component`, `@Service`          |
| Factory         | `BeanFactory`, `FactoryBean`   | `@Bean` methods                   |
| Proxy           | AOP, `@Transactional`          | CGLIB / JDK dynamic proxy         |
| Template Method | `JdbcTemplate`, `RestTemplate` | `execute()`, `exchange()`         |
| Observer        | `ApplicationEvent`             | `@EventListener`                  |
| Strategy        | Multiple implementations       | `@Qualifier`, `List<T>` injection |
| Decorator       | `BeanPostProcessor`            | Bean wrapping at init             |
| Chain of Resp.  | Security filter chain          | `OncePerRequestFilter`            |
| Builder         | Security DSL, `WebClient`      | `.builder().baseUrl(...).build()` |
| Adapter         | `HandlerAdapter`               | Maps handler types to servlet     |
| Prototype       | `@Scope("prototype")`          | New instance per injection        |
| Facade          | `JdbcTemplate`, `WebClient`    | Hides JDBC / HTTP complexity      |

---

## 6. Anti-Patterns to Avoid

| Anti-Pattern           | What Goes Wrong                                | Fix                                         |
| ---------------------- | ---------------------------------------------- | ------------------------------------------- |
| God Object             | One class does everything; 2000+ lines         | Split by Single Responsibility              |
| Service Locator        | Hides dependencies; hard to test               | Use constructor injection (DI)              |
| Anemic Domain Model    | Entities are just data bags; logic in services | Move behavior into domain objects           |
| Over-Engineering       | Pattern for every 3-line function              | Apply patterns when complexity justifies it |
| Singleton Abuse        | Global mutable state; testing nightmare        | Prefer DI-managed singletons                |
| Copy-Paste Inheritance | Duplicate code across subclasses               | Extract to Template Method or Strategy      |

---

## 7. Pattern Selection Cheatsheet

```
Need ONE instance?                    --> Singleton
Need to create objects by type?       --> Factory Method
Need families of related objects?     --> Abstract Factory
Need complex object construction?     --> Builder
Need to clone existing objects?       --> Prototype
Need to adapt incompatible APIs?      --> Adapter
Need to add behavior dynamically?     --> Decorator
Need access control / lazy loading?   --> Proxy
Need to simplify a complex API?       --> Facade
Need tree structures?                 --> Composite
Need swappable algorithms?            --> Strategy
Need event notification?              --> Observer
Need fixed algorithm, variable steps? --> Template Method
Need middleware / filter pipeline?    --> Chain of Responsibility
Need to encapsulate actions?          --> Command
Need state-dependent behavior?        --> State
```

---

## 8. Quick Recall

| #   | Pattern          | One-Liner Recall                                                         |
| --- | ---------------- | ------------------------------------------------------------------------ |
| 1   | Singleton        | Enum singleton is safest; Spring beans are singleton by default          |
| 2   | Factory          | `switch` on type to return subclass; `@Bean` is a factory method         |
| 3   | Abstract Factory | Factory that returns factories; think theme-based UI kits                |
| 4   | Builder          | Fluent API with `return this`; Lombok `@Builder` eliminates boilerplate  |
| 5   | Prototype        | `clone()` with deep copy; `@Scope("prototype")` for non-singleton beans  |
| 6   | Adapter          | Wraps incompatible interface; `Arrays.asList()` is a JDK adapter         |
| 7   | Decorator        | Same interface, added behavior; Java I/O streams are textbook decorators |
| 8   | Proxy            | Same interface, controlled access; `@Transactional` creates a proxy      |
| 9   | Facade           | One clean method hides 10 ugly ones; `JdbcTemplate` over raw JDBC        |
| 10  | Strategy         | `Comparator` is a strategy; inject impls with `@Qualifier`               |
| 11  | Observer         | `@EventListener` for decoupled pub-sub inside Spring                     |
| 12  | Template Method  | Base class defines flow, subclass fills steps; `JdbcTemplate.execute()`  |
| 13  | Chain of Resp.   | Like Express middleware; Spring Security filter chain                    |
| 14  | Command          | `Runnable` is a command; lambdas make it concise                         |
| 15  | State            | Replace state-based `if/else` with State objects; great for workflows    |

---

## 9. Creational vs Structural vs Behavioral -- At a Glance

| Category   | Focus                    | Patterns                                                                      |
| ---------- | ------------------------ | ----------------------------------------------------------------------------- |
| Creational | **Object creation**      | Singleton, Factory, Abstract Factory, Builder, Prototype                      |
| Structural | **Object composition**   | Adapter, Decorator, Proxy, Facade, Composite, Bridge                          |
| Behavioral | **Object communication** | Strategy, Observer, Template Method, Iterator, Command, Chain of Resp., State |

---

> Patterns are tools, not goals. If you can solve the problem cleanly without a pattern, do that.
> The best code uses patterns so naturally you don't even notice them.
