# Java Core & OOP — Architect-Level Revision Guide

> For experienced developers (Node.js / Python background). Not a textbook — a recall tool.

---

## 1. JVM Ecosystem

| Component | One-Liner |
|-----------|-----------|
| **JDK** | Development kit: compiler (`javac`) + tools + JRE. What you install to *write* Java. |
| **JRE** | Runtime environment: JVM + core libraries. What you need to *run* Java. |
| **JVM** | Virtual machine that executes bytecode. Platform-specific, so your code doesn't have to be. |

### Compilation Pipeline

```
Source.java  -->  javac (compiler)  -->  Source.class (bytecode)  -->  JVM (interprets/JIT)  -->  Native execution
```

**Platform independence:** Java compiles to bytecode, not machine code. Each OS has its own JVM that translates bytecode to native instructions — "write once, run anywhere."

---

## 2. Java Syntax Essentials

### Entry Point

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

`public` = accessible everywhere, `static` = no object needed, `void` = returns nothing, `String[] args` = CLI arguments.

### Primitive Types

| Type | Size | Range / Notes | JS/Python Equivalent |
|------|------|---------------|----------------------|
| `byte` | 1 byte | -128 to 127 | -- |
| `short` | 2 bytes | -32,768 to 32,767 | -- |
| `int` | 4 bytes | -2^31 to 2^31 - 1 | `Number` (integer) |
| `long` | 8 bytes | -2^63 to 2^63 - 1 (suffix `L`) | `BigInt` |
| `float` | 4 bytes | ~7 decimal digits (suffix `f`) | -- |
| `double` | 8 bytes | ~15 decimal digits | `Number` (float) |
| `char` | 2 bytes | Single UTF-16 character (`'A'`) | `string[0]` |
| `boolean` | 1 bit* | `true` / `false` only | `boolean` / `bool` |

*JVM implementation may use 1 byte internally.

### Wrapper Classes and Autoboxing

| Primitive | Wrapper | Autoboxing Example |
|-----------|---------|--------------------|
| `int` | `Integer` | `Integer x = 5;` (auto-wrapped) |
| `double` | `Double` | `double d = new Double(3.14);` (auto-unwrapped) |
| `boolean` | `Boolean` | Required for generics: `List<Integer>`, not `List<int>` |
| `char` | `Character` | `Character c = 'A';` |

```java
Integer a = 127, b = 127;
a == b;        // true  — cached range [-128, 127]
Integer x = 128, y = 128;
x == y;        // false — different objects outside cache
x.equals(y);   // true  — always use this
```

### Strings

```java
String s = "hello";              // stored in string pool
String t = new String("hello");  // new heap object, bypasses pool
s == "hello";                    // true  — same pool reference
s == t;                          // false — different objects
s.equals(t);                     // true  — content comparison
```

- `String` is **immutable**. Every modification creates a new object.
- `StringBuilder` for mutable string building in loops (not thread-safe).
- `StringBuffer` is the thread-safe (synchronized) sibling — slower.

### `==` vs `.equals()` — The Biggest Java Trap

| Comparison | `==` | `.equals()` |
|------------|------|-------------|
| Primitives | Compares **value** | N/A (primitives aren't objects) |
| Objects | Compares **reference** (memory address) | Compares **content** (if overridden) |
| Rule | Use for primitives and `null` checks only | Use for all object comparisons |

### `final` Keyword

| Applied To | Effect |
|------------|--------|
| Variable | Value cannot be reassigned (like `const` in JS — but for primitives only; final object refs are still mutable internally) |
| Method | Cannot be overridden by subclasses |
| Class | Cannot be extended (`String`, `Integer` are final) |

### `static` Keyword

| Applied To | Meaning |
|------------|---------|
| Field | One copy shared across all instances (class-level variable) |
| Method | Called on the class, not an instance — cannot access `this` |
| Block | `static { ... }` runs once when the class is loaded |
| Nested Class | Inner class that doesn't need an outer class instance |

### Type Casting

```java
// Widening (automatic) — small to large, no data loss
int i = 100;
long l = i;          // int -> long, implicit

// Narrowing (explicit) — large to small, possible data loss
double d = 9.99;
int n = (int) d;     // 9 — truncated, cast required
```

### Arrays

```java
int[] nums = new int[5];              // declaration + size
int[] vals = {1, 2, 3, 4, 5};        // declaration + initialization
String[] names = new String[]{"A"};   // explicit type

Arrays.sort(nums);                    // in-place sort
Arrays.equals(a, b);                  // content comparison
Arrays.copyOf(nums, 10);             // copy with new length
Arrays.asList(vals);                  // convert to List (fixed-size)
```

---

## 3. Access Modifiers

| Modifier | Same Class | Same Package | Subclass (other pkg) | Everywhere |
|----------|:----------:|:------------:|:--------------------:|:----------:|
| `private` | Yes | -- | -- | -- |
| *(default)* | Yes | Yes | -- | -- |
| `protected` | Yes | Yes | Yes | -- |
| `public` | Yes | Yes | Yes | Yes |

**Recall:** Visibility expands left to right. Default (no keyword) = package-private. `protected` adds subclass access across packages.

---

## 4. OOP — The 4 Pillars

### 4.1 Encapsulation

> Bundling data (fields) and behavior (methods) together, restricting direct access.

```java
public class Account {
    private double balance;                       // hidden
    public double getBalance() { return balance; } // controlled access
    public void deposit(double amt) {
        if (amt > 0) this.balance += amt;         // validated mutation
    }
}
```

**Remember:** Private fields + public methods = encapsulation. It is the Java equivalent of closures hiding state in JS.

### 4.2 Abstraction

> Exposing *what* an object does, hiding *how* it does it.

```java
abstract class Shape {
    abstract double area();          // contract — no body
    String describe() { return "I am a shape"; } // concrete method allowed
}
class Circle extends Shape {
    double r;
    Circle(double r) { this.r = r; }
    double area() { return Math.PI * r * r; }    // must implement
}
```

**Remember:** Code against abstractions, not implementations. Same idea as coding to an interface in Node/Python.

#### Abstract Class vs Interface (quick comparison)

| Feature | Abstract Class | Interface |
|---------|---------------|-----------|
| Instantiate | No | No |
| Constructors | Yes | No |
| State (fields) | Instance variables allowed | Only `public static final` constants |
| Methods | Abstract + concrete | Abstract + `default` + `static` (Java 8+) |
| Inheritance | Single (`extends`) | Multiple (`implements`) |
| Use when | Shared state/code among related classes | Defining a capability/contract |

### 4.3 Inheritance

> A class acquires fields and methods of another class. Promotes code reuse.

```java
class Animal {
    String name;
    Animal(String name) { this.name = name; }
    void speak() { System.out.println("..."); }
}
class Dog extends Animal {
    Dog(String name) { super(name); }           // must call super
    @Override void speak() { System.out.println("Woof"); }
}
```

**Remember:** Java has no multiple class inheritance (diamond problem). Use interfaces for multiple type contracts. `super` accesses the parent — similar to Python's `super()`.

### 4.4 Polymorphism

> One interface, many implementations. An object behaves differently based on its actual type.

**Compile-time (Overloading):** Same method name, different parameter lists.

```java
class Calc {
    int add(int a, int b) { return a + b; }
    double add(double a, double b) { return a + b; }  // different signature
}
```

**Runtime (Overriding):** Subclass provides its own implementation of a parent method.

```java
Animal a = new Dog("Rex");   // reference type: Animal, object type: Dog
a.speak();                   // "Woof" — resolved at runtime (dynamic dispatch)
```

**Remember:** Overloading = compile-time, same class. Overriding = runtime, parent-child. Always use `@Override` to catch signature mistakes at compile time.

---

## 5. Interfaces vs Abstract Classes — Deep Dive

| Criteria | Abstract Class | Interface |
|----------|---------------|-----------|
| Keyword | `abstract class` | `interface` |
| Extend / Implement | `extends` (single) | `implements` (multiple) |
| Fields | Any access modifier, mutable | `public static final` only |
| Constructors | Yes | No |
| Abstract methods | Yes (use `abstract` keyword) | Yes (implicitly `public abstract`) |
| Concrete methods | Yes | `default` and `static` (Java 8+), `private` (Java 9+) |
| Multiple inheritance | No | Yes |
| **When to use** | IS-A relationship with shared state | CAN-DO capability / contract |

### Java 8+ Interface Features

```java
@FunctionalInterface                          // exactly one abstract method
interface Transformer<T> {
    T transform(T input);                     // the single abstract method

    default T identity(T input) {             // default method — has a body
        return input;
    }

    static void log(String msg) {             // static utility method
        System.out.println("LOG: " + msg);
    }
}
```

**Functional Interface:** Exactly one abstract method. Enables lambda expressions. Examples: `Runnable`, `Comparator<T>`, `Function<T,R>`.

---

## 6. SOLID Principles in Java

### S — Single Responsibility

> A class should have only one reason to change.

```java
// BAD: UserService handles auth + email + persistence
// GOOD:
class AuthService    { boolean login(String u, String p) { /*...*/ return true; } }
class EmailService   { void sendWelcome(String email)     { /*...*/ } }
class UserRepository { void save(User u)                  { /*...*/ } }
```

### O — Open/Closed

> Open for extension, closed for modification.

```java
interface Discount { double apply(double price); }
class SeasonalDiscount implements Discount {
    public double apply(double price) { return price * 0.9; }
}
// Add new discounts by adding classes, not modifying existing ones
```

### L — Liskov Substitution

> Subtypes must be substitutable for their base types without breaking behavior.

```java
class Bird         { void fly() { /*...*/ } }
class Sparrow extends Bird { }          // OK — can fly
// class Penguin extends Bird { }       // VIOLATION — penguins can't fly
// Fix: separate Flyable interface from Bird
```

### I — Interface Segregation

> Clients should not be forced to depend on methods they don't use.

```java
interface Printable  { void print(); }
interface Scannable  { void scan(); }
class BasicPrinter implements Printable { public void print() { /*...*/ } }
// BasicPrinter is not forced to implement scan()
```

### D — Dependency Inversion

> Depend on abstractions, not concretions. High-level modules should not depend on low-level modules.

```java
interface Repository { void save(Object o); }
class MySQLRepo implements Repository { public void save(Object o) { /*...*/ } }
class UserService {
    private final Repository repo;                 // depends on abstraction
    UserService(Repository repo) { this.repo = repo; } // injected
}
```

---

## 7. Key Java-Specific Concepts

### `this` Keyword — Java vs JavaScript

| Java `this` | JavaScript `this` |
|-------------|-------------------|
| Always refers to the current object instance | Depends on how the function is called |
| Determined at compile time | Determined at runtime |
| Cannot be rebound | Can be rebound with `call`, `apply`, `bind` |
| Used to disambiguate fields from params | Used to access object context |

```java
class User {
    String name;
    User(String name) { this.name = name; }  // this.field = parameter
}
```

### Constructor Chaining

```java
class Server {
    String host; int port;
    Server()                      { this("localhost", 8080); }  // calls below
    Server(String host)           { this(host, 8080); }         // calls below
    Server(String host, int port) { this.host = host; this.port = port; }
}
```

`this(...)` calls another constructor in the same class. `super(...)` calls the parent constructor. Both must be the first statement.

### `instanceof` Operator

```java
Object obj = "hello";
if (obj instanceof String s) {   // Java 16+ pattern matching
    System.out.println(s.length()); // s is already cast
}
```

Similar to Python's `isinstance()`. Since Java 16, pattern matching avoids the explicit cast.

### Enums — More Powerful Than JS/Python

```java
enum Status {
    ACTIVE("Active"), INACTIVE("Inactive"), BANNED("Banned");

    private final String label;
    Status(String label) { this.label = label; }
    public String getLabel() { return label; }
}
// Usage: Status.ACTIVE.getLabel() -> "Active"
// Enums can have fields, methods, constructors, and implement interfaces.
```

In JS/Python, enums are just constants. Java enums are full classes — type-safe, singleton-per-value, and can hold behavior.

### Inner Classes

| Type | Syntax | Access to Outer | Use Case |
|------|--------|-----------------|----------|
| Static Nested | `static class Inner {}` | Static members only | Grouping helper classes |
| Inner (Non-static) | `class Inner {}` | All members via `Outer.this` | Tightly coupled to outer instance |
| Anonymous | `new Interface() { ... }` | Enclosing scope (effectively final) | One-off implementations, event handlers |
| Local | Defined inside a method | Enclosing scope (effectively final) | Method-scoped helper |

```java
// Anonymous class — the pre-lambda way (still used)
Runnable r = new Runnable() {
    @Override public void run() { System.out.println("running"); }
};
// Lambda equivalent (Java 8+)
Runnable r2 = () -> System.out.println("running");
```

### The `Object` Class — Root of Everything

Every Java class implicitly extends `Object`. Key methods to override:

| Method | Purpose | Contract |
|--------|---------|----------|
| `toString()` | String representation | Override for meaningful logging/debugging |
| `equals(Object o)` | Content equality | Must be reflexive, symmetric, transitive, consistent |
| `hashCode()` | Hash for collections | **If `equals()` is overridden, `hashCode()` MUST be too** |

```java
@Override public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof User u)) return false;
    return Objects.equals(name, u.name) && age == u.age;
}
@Override public int hashCode() {
    return Objects.hash(name, age);
}
```

**The Contract:** Equal objects must have the same hash code. Same hash code does NOT guarantee equality (collisions exist). Breaking this contract corrupts `HashMap` / `HashSet` behavior.

---

## 8. Quick Recall

| # | Concept | One-Liner |
|---|---------|-----------|
| 1 | JVM | Executes bytecode; each OS has its own JVM, giving Java platform independence. |
| 2 | Primitives | 8 types, stored on stack, not objects. Use wrappers for generics. |
| 3 | `==` vs `.equals()` | `==` compares references for objects; `.equals()` compares content. Always use `.equals()` for objects. |
| 4 | `String` | Immutable, pooled. Use `StringBuilder` for concatenation in loops. |
| 5 | Access | `private` < default < `protected` < `public`. Default = package-private (no keyword). |
| 6 | `final` | Variable: constant. Method: no override. Class: no extend. |
| 7 | `static` | Belongs to the class, not the instance. Cannot access `this`. |
| 8 | Encapsulation | Private state + public API. Java's version of closure-based privacy. |
| 9 | Inheritance | Single class inheritance only. Use interfaces for multiple contracts. |
| 10 | Polymorphism | Overloading = compile-time (same class). Overriding = runtime (parent-child). |
| 11 | Interface vs Abstract | Interface = contract (multiple). Abstract class = partial implementation (single). |
| 12 | `equals`/`hashCode` | Override both or neither. Breaking the contract corrupts hash-based collections. |

---

*Next: [02 — Collections, Generics & Streams](./02-collections-generics-streams.md)*
