# Collections and Generics

> Java Collections Framework + Generics — compact revision for experienced developers.

---

## 1. Collections Hierarchy

```
Iterable<T>
  └── Collection<T>
        ├── List<T>
        │     ├── ArrayList      (resizable array)
        │     ├── LinkedList     (doubly-linked list, also implements Deque)
        │     └── Vector/Stack   (legacy synchronized — avoid)
        ├── Set<T>
        │     ├── HashSet        (hash table, unordered)
        │     ├── LinkedHashSet  (insertion order preserved)
        │     └── TreeSet        (sorted, red-black tree)
        └── Queue<T> / Deque<T>
              ├── PriorityQueue  (min-heap)
              └── ArrayDeque     (resizable array — stack + queue)

Map<K,V>  (NOT part of Collection)
  ├── HashMap            (hash table, unordered)
  ├── LinkedHashMap      (insertion/access order)
  ├── TreeMap            (sorted by key, red-black tree)
  └── ConcurrentHashMap  (thread-safe, lock striping)
```

Key point: `Map` does not extend `Collection`. `LinkedList` implements both `List` and `Deque`.

---

## 2. List Implementations

| Feature | ArrayList | LinkedList | Vector |
|---|---|---|---|
| Backing structure | Resizable array | Doubly-linked list | Resizable array |
| `get(i)` | **O(1)** | O(n) | O(1) |
| `add(end)` | **O(1)** amortized | **O(1)** | O(1) |
| `add(i)` / `remove(i)` | O(n) shift | **O(1)** if at node | O(n) |
| `contains` | O(n) | O(n) | O(n) |
| Thread-safe | No | No | Yes (synchronized) |
| Use when | Default choice, random access | Frequent insert/remove at ends | Never (legacy) |

**Default rule:** Use `ArrayList` unless you have a measured reason not to.

```java
// Creation
List<String> list = new ArrayList<>();          // mutable
List<String> fixed = List.of("a", "b", "c");   // immutable (Java 9+)
List<String> from  = new ArrayList<>(List.of("x", "y"));

// Common operations
list.add("item");               // append
list.add(0, "first");           // insert at index
list.get(0);                    // O(1) access
list.set(1, "updated");         // replace at index
list.remove("item");            // by value
list.remove(0);                 // by index
list.contains("first");         // linear search
list.indexOf("updated");        // first occurrence, -1 if absent
list.subList(0, 2);             // view (not a copy)

// Iteration
for (String s : list) { }                          // for-each
list.forEach(System.out::println);                  // lambda
list.stream().filter(s -> s.length() > 3).toList(); // stream (Java 16+)

// Sort
list.sort(Comparator.naturalOrder());
list.sort(Comparator.comparing(String::length).reversed());
```

---

## 3. Set Implementations

| Feature | HashSet | LinkedHashSet | TreeSet |
|---|---|---|---|
| Order | None | **Insertion order** | **Sorted** (natural/comparator) |
| Null support | One null | One null | No null (throws NPE) |
| Backing | HashMap | LinkedHashMap | TreeMap (red-black tree) |
| `add` / `contains` / `remove` | **O(1)** avg | **O(1)** avg | **O(log n)** |
| Thread-safe | No | No | No |
| Use when | Uniqueness check | Unique + order preserved | Sorted unique set |

```java
Set<String> set = new HashSet<>();
set.add("java");
set.add("java");    // ignored — duplicate
set.contains("java"); // true, O(1)
set.remove("java");

// Sorted set
TreeSet<Integer> sorted = new TreeSet<>(List.of(5, 1, 3));
sorted.first();   // 1
sorted.last();    // 5
sorted.headSet(3); // [1]  — elements < 3
sorted.tailSet(3); // [3, 5] — elements >= 3
```

---

## 4. Map Implementations

| Feature | HashMap | LinkedHashMap | TreeMap | ConcurrentHashMap |
|---|---|---|---|---|
| Order | None | **Insertion/access** | **Sorted by key** | None |
| Null key | One | One | No | **No** |
| Null values | Yes | Yes | No | **No** |
| `put` / `get` | **O(1)** avg | **O(1)** avg | **O(log n)** | **O(1)** avg |
| Thread-safe | No | No | No | **Yes** |

### How HashMap Works Internally

```
1. hashCode() → bucket index  (array of Node[])
2. Bucket stores a linked list of entries (key-value pairs)
3. When a bucket has >= 8 entries → converts to red-black tree (O(log n))
4. When bucket shrinks to <= 6 → converts back to linked list
```

- **Initial capacity:** 16 buckets.
- **Load factor:** 0.75 — rehash (double capacity) when 75% full.
- Rehashing is expensive: O(n). Pre-size if you know the count: `new HashMap<>(expectedSize * 4/3 + 1)`.

### hashCode() and equals() Contract

| Rule | What it means |
|---|---|
| `a.equals(b)` implies `a.hashCode() == b.hashCode()` | Equal objects must have the same hash |
| Same hash does NOT imply equals | Hash collisions are allowed |
| Override both or neither | Violating this breaks HashMap/HashSet |

If you override `equals()` but not `hashCode()`, two "equal" objects land in different buckets and HashMap treats them as distinct.

```java
Map<String, Integer> map = new HashMap<>();

// Basic operations
map.put("age", 30);
map.get("age");                  // 30
map.getOrDefault("name", "N/A"); // "N/A"
map.containsKey("age");          // true
map.remove("age");

// Compute patterns (avoid null checks)
map.computeIfAbsent("count", k -> 0);     // set if missing
map.computeIfPresent("count", (k, v) -> v + 1);
map.merge("count", 1, Integer::sum);       // increment or init to 1

// Iteration
map.forEach((k, v) -> System.out.println(k + "=" + v));
for (Map.Entry<String, Integer> e : map.entrySet()) {
    e.getKey(); e.getValue();
}
```

---

## 5. Queue and Deque

| Type | Implementation | Ordering | Use for |
|---|---|---|---|
| `Queue<T>` | `ArrayDeque` | FIFO | BFS, task scheduling |
| `Queue<T>` | `PriorityQueue` | Min-heap (natural order) | Priority processing |
| `Deque<T>` | `ArrayDeque` | FIFO + LIFO | Stack and queue replacement |

**Prefer `ArrayDeque` over `Stack` (legacy) and over `LinkedList` for queue/stack use.**

| Operation | Queue method (throws) | Queue method (returns null) |
|---|---|---|
| Insert | `add(e)` | `offer(e)` |
| Remove head | `remove()` | `poll()` |
| Examine head | `element()` | `peek()` |

```java
// Queue (FIFO)
Deque<String> queue = new ArrayDeque<>();
queue.offer("first");
queue.offer("second");
queue.poll();   // "first"
queue.peek();   // "second"

// Stack (LIFO) — use Deque, not Stack class
Deque<String> stack = new ArrayDeque<>();
stack.push("bottom");
stack.push("top");
stack.pop();    // "top"
stack.peek();   // "bottom"

// PriorityQueue (min-heap)
PriorityQueue<Integer> pq = new PriorityQueue<>();
pq.offer(30);
pq.offer(10);
pq.offer(20);
pq.poll();  // 10 (smallest first)

// Max-heap
PriorityQueue<Integer> maxPq = new PriorityQueue<>(Comparator.reverseOrder());
```

---

## 6. Choosing the Right Collection

| Need | Use | Why |
|---|---|---|
| Ordered, index access | `ArrayList` | O(1) random access, cache-friendly |
| Frequent insert/remove at ends | `ArrayDeque` | O(1) at head/tail, less GC than LinkedList |
| Unique elements | `HashSet` | O(1) add/contains |
| Unique + insertion order | `LinkedHashSet` | O(1) with predictable order |
| Sorted unique elements | `TreeSet` | O(log n), always sorted |
| Key-value pairs | `HashMap` | O(1) avg lookup |
| Key-value + insertion order | `LinkedHashMap` | O(1) with predictable order |
| Sorted key-value | `TreeMap` | O(log n), sorted by key |
| Thread-safe map | `ConcurrentHashMap` | Lock striping, no full lock |
| FIFO processing | `ArrayDeque` | Faster than LinkedList |
| Priority processing | `PriorityQueue` | Min-heap |
| Thread-safe queue | `ConcurrentLinkedQueue` | Lock-free |

---

## 7. Utility Classes

### Collections

```java
Collections.sort(list);                          // natural order
Collections.sort(list, Comparator.reverseOrder());
Collections.unmodifiableList(list);              // read-only wrapper
Collections.synchronizedList(new ArrayList<>());  // thread-safe wrapper
Collections.frequency(list, "item");             // count occurrences
Collections.singletonList("only");               // immutable single-element
Collections.emptyList();                         // immutable empty
Collections.reverse(list);
Collections.shuffle(list);
Collections.min(list);
Collections.max(list);
```

### Arrays

```java
Arrays.sort(arr);                       // in-place sort
Arrays.sort(arr, Comparator.reverseOrder()); // reverse (Integer[], not int[])
Arrays.binarySearch(arr, key);          // array must be sorted
Arrays.asList("a", "b", "c");          // fixed-size List backed by array
Arrays.stream(arr);                     // IntStream / Stream<T>
Arrays.fill(arr, 0);                   // fill all elements
Arrays.copyOf(arr, newLength);         // copy with new length
Arrays.equals(arr1, arr2);            // deep equality check
```

**Pitfall:** `Arrays.asList()` returns a fixed-size list. You cannot `add()` or `remove()`. Wrap it: `new ArrayList<>(Arrays.asList(...))`.

---

## 8. Generics

### Why Generics

Without generics you cast everything and discover type errors at runtime. Generics move that check to compile time.

```java
// Without generics — unsafe
List raw = new ArrayList();
raw.add("text");
String s = (String) raw.get(0);  // cast required, ClassCastException risk

// With generics — safe
List<String> typed = new ArrayList<>();
typed.add("text");
String s = typed.get(0);         // no cast needed
```

### Generic Class and Method

```java
// Generic class
public class Box<T> {
    private T value;
    public void set(T value) { this.value = value; }
    public T get() { return value; }
}
Box<String> box = new Box<>();
box.set("hello");

// Generic method
public static <T> T first(List<T> list) {
    return list.isEmpty() ? null : list.get(0);
}
String f = first(List.of("a", "b")); // T inferred as String
```

### Bounded Types

```java
// Upper bound — T must implement Comparable
public static <T extends Comparable<T>> T max(List<T> list) {
    return list.stream().max(Comparator.naturalOrder()).orElseThrow();
}

// Multiple bounds
public static <T extends Serializable & Comparable<T>> void process(T item) { }
```

### Wildcards and PECS

| Wildcard | Meaning | Mnemonic |
|---|---|---|
| `?` | Unknown type | Read as Object, cannot write |
| `? extends T` | T or subtype | **Producer** — read from it |
| `? super T` | T or supertype | **Consumer** — write to it |

**PECS = Producer Extends, Consumer Super.**

```java
// Producer — read items out of the collection
void printAll(List<? extends Number> nums) {
    for (Number n : nums) System.out.println(n); // safe to read as Number
}
printAll(List.of(1, 2, 3));         // List<Integer> OK
printAll(List.of(1.0, 2.0));       // List<Double> OK

// Consumer — put items into the collection
void addInts(List<? super Integer> dest) {
    dest.add(1);   // safe to write Integer
    dest.add(2);
}
addInts(new ArrayList<Number>());  // List<Number> OK
addInts(new ArrayList<Object>());  // List<Object> OK
```

### Type Erasure

Generics are a compile-time feature only. At runtime, `List<String>` becomes `List<Object>`.

| Allowed | Not Allowed (due to erasure) |
|---|---|
| `new ArrayList<String>()` | `new T()` |
| `list instanceof List` | `list instanceof List<String>` |
| `List<String>` variable | `new T[]` (generic array creation) |

### Diamond Operator (Java 7+)

```java
// Compiler infers type arguments from the left side
Map<String, List<Integer>> map = new HashMap<>();  // no need to repeat types
```

### Common Pitfalls

```java
List<int> nope;             // primitives not allowed — use List<Integer>
T[] arr = new T[10];        // cannot create generic array
if (obj instanceof T) {}    // cannot check generic type at runtime
List<String> != List<Object> // generics are invariant, not covariant
```

---

## 9. Immutable Collections (Java 9+)

```java
List<String>  list = List.of("a", "b", "c");
Set<String>   set  = Set.of("x", "y", "z");
Map<String, Integer> map = Map.of("a", 1, "b", 2);
Map<String, Integer> big = Map.ofEntries(
    Map.entry("a", 1),
    Map.entry("b", 2)
);
```

| Behavior | Detail |
|---|---|
| Immutable | `add()`, `put()`, `remove()` throw `UnsupportedOperationException` |
| Null-hostile | Null elements/keys/values throw `NullPointerException` |
| No duplicates | `Set.of` / `Map.of` throw `IllegalArgumentException` on duplicates |
| Serializable | Yes |

**Mutable copy:** `new ArrayList<>(List.of("a", "b"))`.

---

## 10. Quick Recall

| # | Point |
|---|---|
| 1 | `ArrayList` is the default List; O(1) get, O(1) amortized add. |
| 2 | `HashMap` uses array of buckets; linked list converts to tree at 8 nodes. |
| 3 | Override both `hashCode()` and `equals()` or neither. |
| 4 | HashMap load factor is 0.75; rehashes at 75% capacity. |
| 5 | `HashSet` is backed by a `HashMap` internally. |
| 6 | `ArrayDeque` replaces both `Stack` and `LinkedList` for stack/queue use. |
| 7 | `ConcurrentHashMap` uses lock striping, not a single lock; no null keys/values. |
| 8 | PECS: Producer Extends, Consumer Super. |
| 9 | Type erasure removes generics at runtime; you cannot do `new T()` or `instanceof T`. |
| 10 | `List.of()` / `Set.of()` / `Map.of()` are immutable and null-hostile (Java 9+). |
| 11 | `Arrays.asList()` returns a fixed-size list; wrap it in `ArrayList` for mutability. |
| 12 | `TreeSet` / `TreeMap` use red-black trees; O(log n) ops, no nulls, always sorted. |

---

*Next: [03 — Streams and Functional Programming](03-streams-and-functional-programming.md)*
