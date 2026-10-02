# Heaps — repeatedly get the best candidate

**Mental picture:** A binary heap is a *complete* binary tree, usually kept in an array. A min-heap keeps each parent `<=` its children; that does **not** sort siblings or the entire array.

```text
          2 (minimum)        array: [2, 5, 3, 9, 8]
         / 
        5   3               child indices: 2i+1, 2i+2
       / \                  parent index: floor((i-1)/2)
      9   8
```

| Operation | Cost | Why |
| --- | --- | --- |
| Peek minimum / maximum | `O(1)` | Root at index 0 |
| Insert | `O(log n)` | Append then bubble up along height |
| Remove root | `O(log n)` | Replace with last, sift down |
| Build from `n` items | `O(n)` | Bottom-up heapify, not repeated inserts |
| Search for arbitrary value | `O(n)` | Heap only orders parent vs children |
| Space | `O(n)` | Array of elements |

**Top K:** Maintain a min-heap of at most `k` largest values; if a new value exceeds the root, replace the root. `O(n log k)` time and `O(k)` space; sorting everything costs `O(n log n)` and stores the input/result according to implementation.

**Scheduling:** A priority queue keyed by due time extracts earliest work. An indexed heap can pair a map (`id -> position`) with the heap for updates/cancellation; without it, finding a task is `O(n)`. In distributed systems, the heap is only a local scheduling primitive; persistence, competing workers and delivery guarantees require separate design.

**Heap versus BST:** heap wins on repeated min/max; balanced BST supports arbitrary-key lookup and ordered range queries. Neither structure is a replacement for a hash map's expected `O(1)` exact lookup.

**Recall:** Why is the root the only guaranteed minimum? What happens to `O(log n)` if you scan for an arbitrary value? Why is bottom-up build `O(n)`?
