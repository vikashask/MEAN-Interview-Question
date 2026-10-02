# Hash tables — fast lookup, not free lookup

**In one breath:** Hash a key to choose a bucket, then handle keys that land together. `Map`/`Set` usually give average `O(1)` get/set/has; worst-case collisions can be slower. Use them for membership, counts and indexes—not sorted ranges.

## Picture and invariant

```text
hash("Ada") -> bucket 3 -> ("Ada", 7)
hash("Eve") -> bucket 3 -> ("Ada", 7) -> ("Eve", 4)
```

A collision is normal; correctness requires checking **key equality**, not only the hash. Implementations may chain entries or probe other slots (open addressing). As load factor (`items / capacity`) increases, rehashing into more buckets restores typical speed; a resize costs `O(n)` occasionally.

| Operation | Expected / average | Worst theoretical | Notes |
| --- | --- | --- | --- |
| `get` / `has` / `set` / `delete` | `O(1)` | `O(n)` | Depends on hashing, load and collision handling |
| Iterate all entries | `O(n)` | `O(n)` | `Map` iteration follows insertion order in JS; not sorted order |
| Space | `O(n)` | `O(n)` | Buckets and entries cost more than a compact array |

**JS choice:** `Map` supports keys of any type, `Set` stores unique values, plain `Object` is useful for simple string-key records. JS key identity matters: separate object literals are different `Map` keys; `Set` uses SameValueZero (e.g., `NaN` matches `NaN`). The language does not promise a specific hash-table implementation for every engine; these costs are the conceptual model, not a spec guarantee.

```js
const counts = new Map();
for (const item of ['a', 'b', 'a']) counts.set(item, (counts.get(item) ?? 0) + 1);
// Map { 'a' => 2, 'b' => 1 }
const seen = new Set([1, 2, 2]); // Set { 1, 2 }
```

## Why this changes an algorithm

**Two Sum:** For each value `x`, ask if `target - x` was seen *before*; then record `x`. `O(n)` expected time, `O(n)` space. If the same index must not be reused, check before adding. For all distinct value-pairs, clarify whether duplicates count and deduplicate emitted pairs separately.

**At scale:** A local map is per-process and disappears on restart. A distributed cache adds serialization, network cost, invalidation and concurrency concerns; `O(1)` hash access does **not** imply `O(1)` end-to-end request latency. For sorted/range scans use a tree or sorted index instead.

**Recall:** What causes a collision? When does resize happen? Why won't `new Map([[{}, 1]]).get({})` find the entry?
