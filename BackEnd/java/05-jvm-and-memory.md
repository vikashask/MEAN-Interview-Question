# JVM Architecture and Memory Management

> Architect-level revision sheet. Not a textbook. Skim, recall, move on.

---

## 1. JVM Architecture Overview

```
.java  -->  javac  -->  .class (bytecode)
                            |
                +-----------v--------------------------+
                |           JVM                        |
                |                                      |
                |   Class Loader Subsystem             |
                |     (Load -> Link -> Initialize)     |
                |               |                      |
                |               v                      |
                |   Runtime Data Areas                 |
                |   +-------+--------+--------------+  |
                |   | Heap  | Stack  | Method Area  |  |
                |   |       | (per   | (Metaspace)  |  |
                |   |       | thread)|              |  |
                |   +-------+--------+--------------+  |
                |   | PC Register | Native Method  |  |
                |   | (per thread)| Stack          |  |
                |   +-------------+----------------+  |
                |               |                      |
                |               v                      |
                |   Execution Engine                   |
                |   (Interpreter + JIT + GC)           |
                +--------------------------------------+
```

The JVM is a specification, not a single implementation. HotSpot (Oracle/OpenJDK) is the dominant one. GraalVM is the notable alternative.

---

## 2. Memory Areas

| Area | Stores | Shared? | Managed By | Key Facts |
|------|--------|---------|------------|-----------|
| **Heap** | Objects, arrays | Yes (all threads) | GC | Divided into Young + Old gen. OOM if full. |
| **Stack** | Frames: locals, operand stack, return addr | No (per thread) | Auto (LIFO) | Fixed size (`-Xss`). `StackOverflowError` if deep. |
| **Method Area / Metaspace** | Class metadata, static fields, constant pool | Yes | GC (partial) | Off-heap native memory since Java 8. No more `PermGen`. |
| **PC Register** | Address of current instruction | No (per thread) | JVM | Undefined for native methods. |
| **Native Method Stack** | JNI call frames | No (per thread) | OS | Mirrors Java stack for native code. |

**Heap layout (generational):**

```
+---------------------------+--------------------+
|        Young Gen          |     Old Gen        |
| +-----+------+------+    |   (Tenured)        |
| |Eden | S0   | S1   |    |                    |
| +-----+------+------+    |                    |
+---------------------------+--------------------+
```

Objects allocate in Eden. Survivors get copied between S0/S1. Long-lived objects promote to Old Gen.

---

## 3. Class Loading

### Three Phases

| Phase | What Happens |
|-------|-------------|
| **Loading** | Reads `.class` bytecode, creates `Class` object in Method Area |
| **Linking** | **Verify** (bytecode correctness) -> **Prepare** (allocate static vars, default values) -> **Resolve** (symbolic refs to direct refs) |
| **Initialization** | Runs `<clinit>` -- static blocks, static field assignments |

### ClassLoader Hierarchy

```
Bootstrap ClassLoader        (rt.jar, core libs -- native C++)
       |
Platform / Extension CL     (jre/lib/ext -- Java 9+ platform modules)
       |
Application ClassLoader     (classpath -- your code)
       |
Custom ClassLoaders          (app servers, OSGi, plugin systems)
```

**Parent delegation model:** A classloader first delegates to its parent before attempting to load itself. This prevents core classes (like `java.lang.String`) from being overridden by user code.

### Common Errors

| Error | Cause | When |
|-------|-------|------|
| `ClassNotFoundException` | Class not found on classpath | Runtime, checked (`Class.forName()`) |
| `NoClassDefFoundError` | Class was available at compile time, missing at runtime | Runtime, unchecked (linkage failure) |

---

## 4. Garbage Collection

### Core Concept: Mark and Sweep

1. **Mark** -- traverse from GC roots, mark all reachable objects as alive
2. **Sweep** -- reclaim memory of unmarked (unreachable) objects
3. **Compact** (optional) -- defragment heap to avoid fragmentation

### GC Roots

Anything the GC considers a "starting point" for reachability:

- Local variables on thread stacks
- Active threads themselves
- Static references in loaded classes
- JNI references

### Generational Collection

| Event | Scope | Speed | Frequency | Notes |
|-------|-------|-------|-----------|-------|
| **Minor GC** | Young Gen only | Fast (ms) | Frequent | Copies survivors between S0/S1, promotes old objects |
| **Major GC** | Old Gen | Slow | Infrequent | Usually triggers stop-the-world pause |
| **Full GC** | Entire heap + Metaspace | Slowest | Rare | Avoid in production if possible |

### GC Algorithms Comparison

| GC | Flag | Best For | Pause | Throughput | Notes |
|----|------|----------|-------|------------|-------|
| **Serial** | `-XX:+UseSerialGC` | Small apps, single core | Long | Okay | Single-threaded GC |
| **Parallel** | `-XX:+UseParallelGC` | Batch jobs, throughput | Medium | High | Multi-threaded, default pre-Java 9 |
| **G1** | `-XX:+UseG1GC` | General purpose | Predictable | Good | Default since Java 9. Region-based. |
| **ZGC** | `-XX:+UseZGC` | Ultra-low latency | Sub-ms | Good | Concurrent, scalable to TB heaps. Java 15+ prod. |
| **Shenandoah** | `-XX:+UseShenandoahGC` | Low latency | Sub-ms | Good | Concurrent compaction. OpenJDK only. |

**G1 key idea:** Divides heap into equal-sized regions (~2048). Collects "garbage-first" regions with most reclaimable space. Aims for a target pause time (`-XX:MaxGCPauseMillis`).

**`System.gc()`** -- a suggestion, not a command. The JVM can ignore it. Never rely on it. Disable with `-XX:+DisableExplicitGC`.

---

## 5. JIT Compilation

The JVM starts by interpreting bytecode, then compiles hot code paths to native machine code at runtime.

### How It Works

```
Bytecode --> Interpreter (slow, immediate)
                |
          method called N times?
                |
                v
         JIT Compiler (compile to native code, cache it)
                |
                v
         Native execution (fast, subsequent calls)
```

### C1 vs C2 Compilers

| Compiler | Alias | Optimizations | Compile Speed | Code Quality |
|----------|-------|---------------|---------------|--------------|
| **C1** | Client | Basic: inlining, simple opts | Fast | Good |
| **C2** | Server | Aggressive: escape analysis, vectorization | Slow | Best |

**Tiered compilation** (default since Java 8): Start with C1 for quick warmup, promote hot methods to C2 for maximum optimization.

### Key JIT Optimizations

| Optimization | What It Does |
|-------------|-------------|
| **Inlining** | Replaces method call with method body. Eliminates call overhead. |
| **Escape Analysis** | If an object does not escape a method, allocate it on the stack (no GC needed). |
| **Loop Unrolling** | Reduces loop overhead by expanding iterations. |
| **Dead Code Elimination** | Removes code that has no effect on output. |
| **Devirtualization** | Converts virtual (polymorphic) calls to direct calls when only one implementation exists. |

---

## 6. Memory Tuning Flags

| Flag | Purpose | Example | Default |
|------|---------|---------|---------|
| `-Xms` | Initial heap size | `-Xms512m` | JVM-dependent |
| `-Xmx` | Maximum heap size | `-Xmx2g` | 1/4 of physical RAM |
| `-Xss` | Thread stack size | `-Xss512k` | 512k-1m (platform) |
| `-XX:+UseG1GC` | Select GC algorithm | -- | Default since Java 9 |
| `-XX:MaxGCPauseMillis` | Target GC pause | `-XX:MaxGCPauseMillis=200` | 200ms (G1) |
| `-XX:NewRatio` | Old/Young gen ratio | `-XX:NewRatio=2` | 2 (Old is 2x Young) |
| `-XX:MetaspaceSize` | Initial metaspace | `-XX:MetaspaceSize=256m` | ~21m |
| `-XX:MaxMetaspaceSize` | Cap metaspace growth | `-XX:MaxMetaspaceSize=512m` | Unlimited |
| `-XX:+HeapDumpOnOutOfMemoryError` | Dump heap on OOM | -- | Off |
| `-XX:HeapDumpPath` | Dump file location | `-XX:HeapDumpPath=/tmp/dump.hprof` | Working dir |
| `-XX:+PrintGCDetails` | GC logging (pre-9) | -- | Off |
| `-Xlog:gc*` | Unified GC logging (9+) | `-Xlog:gc*:file=gc.log` | Off |

**Rule of thumb:** Set `-Xms` equal to `-Xmx` in production to avoid heap resizing overhead.

---

## 7. Common Memory Problems

| Problem | Error | Typical Cause | Fix |
|---------|-------|---------------|-----|
| Heap exhaustion | `OutOfMemoryError: Java heap space` | Object leak, dataset too large for heap | Increase `-Xmx`, fix leak, use streaming |
| Metaspace exhaustion | `OutOfMemoryError: Metaspace` | Classloader leak, too many generated classes | Fix classloader lifecycle, set `-XX:MaxMetaspaceSize` |
| Stack overflow | `StackOverflowError` | Infinite/deep recursion | Convert to iteration, increase `-Xss` |
| Native memory leak | Process RSS grows, no Java OOM | JNI leak, direct buffers, thread explosion | Monitor with NMT (`-XX:NativeMemoryTracking`) |
| GC thrashing | App stalls, Full GC in logs | Heap too small, promotion failure | Tune heap size, check for leaks |

### Memory Leak Patterns

- **Static collections** -- `static List<>` that grows forever
- **Unclosed resources** -- streams, connections not closed (use try-with-resources)
- **Listener/callback accumulation** -- registered but never deregistered
- **ThreadLocal misuse** -- values not removed in thread pools
- **Classloader leaks** -- common in app servers during hot redeploy

---

## 8. Profiling and Diagnostic Tools

| Tool | Type | Use Case |
|------|------|----------|
| `jps` | CLI | List running JVM processes |
| `jstack <pid>` | CLI | Thread dump -- deadlock detection, stuck threads |
| `jmap -heap <pid>` | CLI | Heap summary, histogram |
| `jmap -dump:format=b,file=dump.hprof <pid>` | CLI | Heap dump for offline analysis |
| `jstat -gcutil <pid> 1000` | CLI | GC stats every 1s -- live monitoring |
| `jconsole` | GUI | Basic MBean/memory/thread monitoring |
| `VisualVM` | GUI | Profiling, heap analysis, thread monitoring |
| `JDK Flight Recorder (JFR)` | Built-in | Low-overhead production profiling (start with `-XX:StartFlightRecording`) |
| `JDK Mission Control (JMC)` | GUI | Analyze JFR recordings |
| `async-profiler` | External | CPU/allocation profiling with flame graphs |
| `Eclipse MAT` | External | Heap dump analysis, leak suspect reports |

**Production tip:** Always enable JFR in production. Overhead is under 2%. Use: `-XX:StartFlightRecording=duration=0s,filename=recording.jfr,settings=profile`.

---

## 9. Quick Recall

| # | Point |
|---|-------|
| 1 | JVM converts bytecode to native code at runtime. It is a spec, not a single product. |
| 2 | Heap is shared and GC'd. Stack is per-thread and auto-managed (LIFO). |
| 3 | Metaspace replaced PermGen in Java 8. It lives in native memory, not the heap. |
| 4 | Class loading uses parent delegation: child asks parent first, loads only if parent cannot. |
| 5 | GC roots = stack locals + static refs + JNI refs + active threads. Unreachable from roots = garbage. |
| 6 | Young Gen GC (minor) is fast and frequent. Old Gen GC (major/full) is slow and stop-the-world. |
| 7 | G1 is the default GC since Java 9. ZGC and Shenandoah target sub-millisecond pauses. |
| 8 | JIT compiles hot methods to native code. Tiered compilation uses C1 first, then C2. |
| 9 | Escape analysis can allocate objects on the stack instead of the heap -- no GC overhead. |
| 10 | Set `-Xms` = `-Xmx` in production. Always enable `-XX:+HeapDumpOnOutOfMemoryError`. |
| 11 | `ClassNotFoundException` is checked (classpath issue). `NoClassDefFoundError` is unchecked (was there at compile, gone at runtime). |
| 12 | JFR is free, low-overhead, production-safe profiling built into the JDK. Use it. |

---
