# Arrays — index fast, movement expensive

**One-minute answer:** An abstract array supports indexed access; a conventional packed array uses a contiguous block, making index lookup `O(1)` and middle insert/delete `O(n)` because elements move. A dynamic array keeps _length_ and _capacity_; when full it reallocates, making append `O(1)` **amortized**, not guaranteed per call. JavaScript's `Array` is a language abstraction, not a guarantee of contiguous, equal-size storage in every engine.

## See why

```text
Packed 4-byte values, base 1000: [10, 20, 30, 40]
addresses:                      1000 1004 1008 1012
value at i=3:                   base + 3 * 4 = 1012

insert 99 at i=1: [10, 20, 30, 40] -> [10, _, 20, 30, 40] -> [10, 99, 20, 30, 40]
```

The address formula is a **model for typed/static contiguous arrays**. JS objects/heterogeneous/sparse arrays can have different physical layouts; the observed cost of a JS operation depends on the engine and elements.

## Why amortized append is cheap

If capacity doubles `1 → 2 → 4 → 8`, occasional appends copy all previous values. Over `n` appends, copies total less than `2n` (geometric series); total `O(n)`, so **`O(1)` amortized per append**, with a single resize still `O(n)`.

| Operation                        | Cost (dynamic packed-array model)          | Note                                         |
| -------------------------------- | ------------------------------------------ | -------------------------------------------- |
| Read/write by index              | `O(1)`                                     | index must be in bounds                      |
| Scan for value                   | `O(n)`                                     | sorted data can use binary search `O(log n)` |
| Append                           | `O(1)` amortized; `O(n)` resize worst case | may grow capacity                            |
| Remove last                      | `O(1)`                                     | compact shrink strategy may vary             |
| Insert/delete at front or middle | `O(n)`                                     | move suffix                                  |
| Reverse in place                 | `O(n)` time, `O(1)` extra space            | swap symmetric positions                     |

**Architecture lens:** Packed arrays have good locality and low per-item overhead. Prefer them for scan-heavy analytics and UI lists. Do **not** reflexively replace a JS array with a linked list just because front insertion is `O(n)`—pointer allocation, GC and cache locality can dominate; benchmark the actual workload. For frequent key lookup, build a `Map` index. For a FIFO queue, use a head-index/deque instead of repeated `shift()`.

## Patterns that reuse the same invariant

- **Two pointers:** slow writes the next valid element; fast scans. Sorted deduplication: prefix `[0, slow)` is unique, `O(n)` time / `O(1)` extra space.
- **Binary search:** sorted input; discard half each step. Beware off-by-one and duplicates; state whether you want _any_ match or the first/last.
- **Prefix sums:** `prefix[i+1] = prefix[i] + a[i]`; interval `[l,r)` is `prefix[r] - prefix[l]`. `O(n)` build, `O(1)` query, `O(n)` extra space; updates cost `O(n)` unless using a Fenwick/segment tree.
- **Sliding window:** move boundaries while maintaining a condition; use when intervals and monotonic updates make repeated work avoidable.

See [four worked examples](./1.arrayExample.md), [runnable JS drills](./2.arrayExample.js), [Python notebook](./array.ipynb), [core questions](../coreQuestion.md) and [advanced problems](../advance_ds_question.md).

**Recall without notes:** Why is the _worst_ append `O(n)`? What is the prefix invariant during deduplication? What must be true before binary search works?
