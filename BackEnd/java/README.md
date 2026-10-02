# Java Mastery Guide

> **For:** Experienced developers (Node.js / Python background) moving to Java  
> **Goal:** Concise, deep, architect-level revision — not a textbook  
> **Format:** Tables, one-liners, code snapshots, recall summaries

---

## File Index

| # | File | What It Covers | Read Time |
|---|------|---------------|-----------|
| 01 | [Core Java & OOP](01-core-and-oop.md) | JVM ecosystem, syntax, types, OOP, access control, SOLID | 15 min |
| 02 | [Collections & Generics](02-collections-and-generics.md) | List / Set / Map / Queue hierarchy, Generics, wildcards, when to pick what | 12 min |
| 03 | [Modern Java (8–21)](03-modern-java-features.md) | Lambdas, Streams, Optional, Records, Sealed classes, Pattern matching, `var` | 12 min |
| 04 | [Concurrency](04-concurrency.md) | Threads, synchronized, volatile, ExecutorService, CompletableFuture, Virtual Threads | 12 min |
| 05 | [JVM & Memory](05-jvm-and-memory.md) | JVM architecture, Garbage Collection, class loading, tuning flags | 10 min |
| 06 | [Exceptions & I/O](06-exceptions-and-io.md) | Checked vs Unchecked, try-with-resources, NIO, Serialization | 8 min |
| 07 | [Spring Boot Essentials](07-spring-boot-essentials.md) | DI, annotations, REST, JPA, profiles, actuator, testing | 15 min |
| 08 | [Spring Security & Auth](08-spring-security.md) | SecurityFilterChain, JWT, OAuth2, CORS, method security, best practices | 12 min |
| 09 | [Design Patterns in Java](09-design-patterns.md) | Creational / Structural / Behavioral — Java idioms, when to use | 12 min |
| 10 | [Interview Questions](10-java-interview-questions.md) | 60+ must-know Qs with crisp answers for rapid revision | 20 min |
| — | [program/](program/) | Classic algorithm examples (Binary Search, Selection Sort, etc.) | reference |

**Total focused reading: ~2 hours** (skip what you already know)

---

## Learning Order

```
Week 1                    Week 2                     Week 3
┌─────────────────┐      ┌──────────────────┐       ┌─────────────────────┐
│ 01 Core & OOP   │─────▶│ 03 Modern Java   │──────▶│ 07 Spring Boot      │
│ 02 Collections  │      │ 04 Concurrency   │       │ 08 Spring Security  │
│ 06 Exceptions   │      │ 05 JVM & Memory  │       │ 09 Design Patterns  │
└─────────────────┘      └──────────────────┘       └─────────────────────┘
                                                            │
                                                            ▼
                                                    ┌─────────────────────┐
                                                    │ 10 Interview Qs     │
                                                    │    (revision loop)  │
                                                    └─────────────────────┘
```

---

## Coming from Node.js / Python?

| You know this | Java equivalent | Key difference |
|---------------|-----------------|----------------|
| `let` / `const` | `var` (Java 10+), `final` | Java is statically typed; `var` is local inference only |
| `{}` object literal | `Map<K,V>` or a class | No ad-hoc objects; everything is a class |
| `[1,2,3]` array | `int[]` or `List<Integer>` | Primitives vs wrappers; arrays are fixed-size |
| `async/await` | `CompletableFuture`, Virtual Threads (21+) | No event loop; real OS threads (or virtual threads) |
| `npm` | Maven / Gradle | `pom.xml` = `package.json`; `mvn` = `npm` |
| `class` (prototype) | `class` (true OOP) | Interfaces, abstract classes, access modifiers matter |
| `try/catch` | `try/catch` + **checked exceptions** | Compiler forces you to handle or declare some exceptions |
| `null` | `null` + `Optional<T>` | `NullPointerException` is Java's biggest trap; use `Optional` |
| Duck typing | Generics + interfaces | Type safety at compile time; no runtime surprises |
| `Express` / `Flask` | Spring Boot | Annotation-driven; DI built-in; opinionated conventions |
| `.env` | `application.yml` + profiles | Externalized config with precedence rules |

---

## One-Liner Recall (Pin This)

| Topic | Remember This |
|-------|--------------|
| JVM | "Write once, run anywhere" — bytecode on a virtual machine |
| OOP | "4 pillars: Encapsulate, Abstract, Inherit, Polymorph" |
| Collections | "List = ordered, Set = unique, Map = key→value, Queue = FIFO" |
| Generics | "Compile-time safety, erased at runtime" |
| Streams | "Pipeline: source → intermediate ops → terminal op (lazy until terminal)" |
| Optional | "A box that may be empty — never call `.get()` without checking" |
| Threads | "synchronized = mutual exclusion; volatile = visibility; Atomic = lock-free" |
| GC | "Don't manage memory; tune GC pauses instead" |
| Spring DI | "@Component marks the bean, @Autowired injects it, Spring wires the graph" |
| JWT | "Stateless auth: encode claims, sign, verify on every request" |

---

## Quick Setup (macOS)

```bash
# Install Java (latest LTS)
brew install openjdk@21
export JAVA_HOME=$(/usr/libexec/java_home -v 21)

# Verify
java -version
javac -version

# Create a Spring Boot project
# Visit https://start.spring.io or:
brew install springboot   # Spring Boot CLI
spring init --dependencies=web,data-jpa,security my-app
cd my-app && ./mvnw spring-boot:run
```

---

*Last updated: 2025*
