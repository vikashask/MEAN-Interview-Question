# Sorting — choose by guarantees and input

Read the [one-page decision map](../typeOfShorting.md) first. **Stable** means items with equal sort keys preserve their input order; **in-place** describes auxiliary storage (recursion still uses stack). Comparison sorting cannot guarantee better than `Ω(n log n)` for arbitrary distinct keys; counting/radix exploit additional structure in the keys.

| Sort                          | Best         | Average      | Worst        | Extra space                            | Stable (shown version)?               | Memory hook        |
| ----------------------------- | ------------ | ------------ | ------------ | -------------------------------------- | ------------------------------------- | ------------------ |
| Bubble (with early exit only) | `O(n)`       | `O(n²)`      | `O(n²)`      | `O(1)`                                 | yes                                   | swap neighbors     |
| Selection                     | `O(n²)`      | `O(n²)`      | `O(n²)`      | `O(1)`                                 | no                                    | pick minimum       |
| Insertion                     | `O(n)`       | `O(n²)`      | `O(n²)`      | `O(1)`                                 | yes                                   | sort cards in hand |
| Merge (array)                 | `O(n log n)` | `O(n log n)` | `O(n log n)` | `O(n)`                                 | yes **if equal keys take left first** | split and combine  |
| Quick (in-place partition)    | `O(n log n)` | `O(n log n)` | `O(n²)`      | `O(log n)` average stack, `O(n)` worst | no                                    | pivot partitions   |
| Heap                          | `O(n log n)` | `O(n log n)` | `O(n log n)` | `O(1)` auxiliary                       | no                                    | remove maximum     |
| Counting (stable output)      | `O(n+k)`     | `O(n+k)`     | `O(n+k)`     | `O(n+k)`                               | yes                                   | count integer keys |
| Radix (stable digit passes)   | `O(d(n+b))`  | same         | same         | `O(n+b)`                               | yes                                   | digits/base        |

`n` items, key range `k`, digits `d`, base `b`. Table describes standard algorithm variants, not a guarantee of every snippet below. [Quick_Sort.js](./quick_Sort.js) allocates `left` and `right` arrays instead of partitioning in place; its peak extra memory can be `O(n)` for balanced splits and `O(n²)` on a worst-case unbalanced recursion path (simultaneously retained copied arrays). [bubbleSort.js](./bubbleSort.js) has no early exit, so its best case is **`O(n²)`**. These distinctions are interview material.

## Understand a trace, not a wall of code

**Merge sort:** `[5,2,4,1] → [5,2] [4,1] → [2,5] [1,4] → [1,2,4,5]`. Split height `log n`; merge `n` items per level → `O(n log n)`. On equal keys, take the **left** item first to preserve stability. [Run merge implementation](./Merge_Sort.js).

**Quick sort:** Choose pivot 4 in `[6,3,8,2,9,4]`; partition to `[3,2,4,6,9,8]`, then recurse on both sides. Balanced splits: `O(n log n)`; last-element pivot on sorted data can make `O(n²)`. Pivot selection or introsort mitigates poor cases. [Run allocating quick sort](./quick_Sort.js).

**Heap sort:** Build max heap in `O(n)`; swap root with the end, shrink active heap, sift down `O(log n)` each time → total `O(n log n)`. The heap property is weaker than fully sorted order; see [heaps](../heaps.md).

**Insertion / selection / bubble:** see [insertion](./Insertion%20Sort%20Algorithm.js), [selection](./Selection%20Sort.js), [bubble](./bubbleSort.js). Insertion exploits nearly ordered input; selection minimizes swaps; bubble is mainly a teaching example. For general JS data prefer the built-in: `[10, 2].sort((a, b) => a - b)` (default sort is string-based). Built-in `sort` mutates its input; use `toSorted` where supported if you need a copy.

**Specialized sorts:** counting uses a bounded integer domain; radix requires a stable digit sort and a defined representation (the simple nonnegative decimal variant does not handle negatives without changes); bucket sort's expected speed assumes a suitable distribution; Shell/comb/cycle/pigeonhole have niche use cases and complexity depends on gap/distribution/range.

**Architecture lens:** Sorting a million records in memory, requesting `ORDER BY` from a DB index, and merging already sorted streams are different problems. State where data lives, memory limit, stability, pagination and latency targets. For just Top K, a heap may avoid sorting everything.

**Recall:** Why does merge need tie handling? What is the memory cost of the _actual_ quick sort sample? What assumption permits counting sort to beat the comparison bound?
