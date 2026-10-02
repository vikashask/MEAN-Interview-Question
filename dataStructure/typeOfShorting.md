# Sorting types — one-page decision map

For full traces and example files, use the [sorting guide](./shorting/index.md). Sorting is an **algorithm**, not a storage structure; what matters is the input contract, mutability, stability, memory budget and worst-case behavior.

| Situation                                             | Reasonable starting point   | Why                                                                             |
| ----------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------- |
| General JS application data                           | `arr.sort((a, b) => a - b)` | Built-in stable sort (modern JS), comparator required for numeric order         |
| Nearly sorted, small data                             | Insertion sort              | `O(n)` best case and low overhead                                               |
| Need stable worst-case `O(n log n)`                   | Merge sort                  | Uses `O(n)` extra space in common array form                                    |
| Average fast in-place partition                       | Quick sort                  | Can be `O(n²)` with bad pivots; recursion stack varies                          |
| Worst-case `O(n log n)`, constant extra array storage | Heap sort                   | Typically not stable                                                            |
| Small bounded integer key range                       | Counting sort               | `O(n+k)` where `k` is key range; often `O(n+k)` space for stable output         |
| Fixed-width nonnegative integer keys                  | Radix sort                  | `O(d(n+b))` for `d` digits/base `b`; needs stable per-digit pass                |
| Well-distributed values with known domain             | Bucket sort                 | Expected case depends on distribution and bucket sorter; worst can be quadratic |

**Memory anchor:** Insertion = playing cards; merge = split/combine; quick = pivot/partition; heap = repeatedly pick maximum. Bubble and selection mainly teach loop invariants; they are rarely production choices for large inputs. Shell, comb, cycle and pigeonhole are specialized; understand their constraints rather than memorizing code.

**Recall:** Can a sort be stable if ties are taken from the right half of a merge? Does `O(n log n)` average promise the worst case? Does radix sort accept arbitrary negative/fractional inputs without adaptation?
