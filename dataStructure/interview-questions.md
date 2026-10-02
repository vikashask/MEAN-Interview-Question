# Data-structure interview questions — rapid recall

> Curated high-frequency questions, **not a guarantee of every possible interview question**. If time is limited, do Tier 1 first. Cover the right column, speak a 30-second answer, then check the “why” and an edge case. Each topic links to a deeper explanation in the [study map](./README.md).

## Tier 1 — must explain without notes

| # | Question | Short answer and condition |
| --- | --- | --- |
| 1 | Array versus linked list? | Array: `O(1)` index and locality; list: `O(n)` index, `O(1)` rewire **with predecessor/node already known**. |
| 2 | Why is array insertion at the front `O(n)`? | Elements shift one slot; append is `O(1)` amortized via capacity growth. |
| 3 | What does amortized `O(1)` mean? | An occasional resize takes `O(n)`, but `n` appends total `O(n)` under geometric growth. |
| 4 | When is binary search valid? | Sorted, indexable data with consistent comparison; halve interval: `O(log n)` time. |
| 5 | What does a JS string index represent? | A UTF-16 code unit; not always a Unicode code point or a user-visible character. |
| 6 | What does a hash table trade for fast lookup? | Expected `O(1)` exact-key lookup for memory; collisions/resize mean slower worst cases; no sorted-range lookup. |
| 7 | `Map` versus `Object` versus `Set`? | `Map`: arbitrary keys; `Object`: simple string/symbol-key record; `Set`: unique values. |
| 8 | Stack versus queue? | LIFO versus FIFO. Undo/DFS uses stack; arrival order/BFS uses queue. |
| 9 | Why not JS `shift()` for high-volume queue? | It can shift remaining elements (`O(n)`); use head index/deque/linked queue. |
| 10 | Why are linked-list edits not always `O(1)`? | Locating the target or predecessor is `O(n)`; rewiring after discovery is `O(1)`. |
| 11 | Reverse a linked list? | Save `next`, redirect `current.next` to `prev`, advance; `O(n)` time, `O(1)` extra. |
| 12 | Detect a cycle? | Slow pointer moves one, fast moves two; meet => cycle; `O(n)` time, `O(1)` space. |
| 13 | BST versus binary tree? | BST has left < root < right ordering; arbitrary binary tree does not. Both can be unbalanced. |
| 14 | BST lookup complexity? | `O(h)` where `h` = height; `O(log n)` balanced, `O(n)` worst for a chain. |
| 15 | Inorder traversal yields sorted values when? | Only if the binary tree satisfies BST ordering (including a defined duplicate policy). |
| 16 | Heap versus balanced BST? | Heap: best-at-root `O(1)`, extract/insert `O(log n)`; BST: ordered key lookup/ranges `O(log n)`. |
| 17 | What is a trie? | Shared-prefix tree; lookup `O(L)` for key length `L`, with node/memory overhead. |
| 18 | BFS versus DFS? | BFS queue explores by hop count; DFS stack/recursion follows a branch. Both `O(V+E)` on adjacency list. |
| 19 | Unweighted shortest path? | BFS; first visit finds fewest edges. Weighted nonnegative: Dijkstra, not plain BFS. |
| 20 | Adjacency list versus matrix? | List `O(V+E)` space; matrix `O(V²)`, but matrix edge lookup `O(1)`. |
| 21 | Stable sort? | Equal-key elements stay in original relative order; merge can be stable if ties choose left first. |
| 22 | Merge versus quick sort? | Merge `O(n log n)` worst, `O(n)` array scratch, stable when implemented carefully; quick average `O(n log n)`, worst `O(n²)`. |
| 23 | Counting sort faster than comparison lower bound? | Only by exploiting bounded integer keys; `O(n+k)` time, range-dependent space. |
| 24 | Two Sum? | Hash values already seen, check complement before insert; expected `O(n)` time / `O(n)` space. |
| 25 | How to find Top K of a stream? | Min-heap of size `k`; `O(n log k)` time and `O(k)` space. |
| 26 | What is the LRU cache combination? | Map → node + doubly linked recency list; average `O(1)` get/put/evict, aside from concurrency/persistence. |

### Check the *why* with one trace

- For #3, capacity `1 → 2 → 4 → 8`: how many old elements are copied total for eight appends?
- For #10, what changes when only a *value* is supplied rather than the node reference?
- For #18, why must a BFS mark nodes on **enqueue**, not only when dequeued?
- For #22, trace equal keys from left/right halves and watch stability.

## Tier 2 — distinguish stronger candidates

| # | Question | Interview-ready answer / trade-off |
| --- | --- | --- |
| 27 | What is a collision? | Two keys map to the same bucket; equality checking plus chaining/probing preserves correctness. |
| 28 | What happens during a hash resize? | Reallocate buckets and rehash entries, often `O(n)` for that operation. |
| 29 | Is `O(1)` lookup equal to fast end-to-end latency? | No: serialization, network, storage, contention and GC are outside an in-memory operation count. |
| 30 | How does a queue with two stacks work? | Transfer `in → out` only if `out` empty; each item moves at most twice, amortized `O(1)` dequeue. |
| 31 | What does a min-stack store? | A parallel running-min stack; `getMin()` `O(1)` with `O(n)` extra space. |
| 32 | Why keep tail pointer in a list? | Singly append becomes `O(1)`; singly remove-tail stays `O(n)` without predecessor. |
| 33 | Circular versus doubly list? | Circular tail links to head (round robin); doubly nodes link both directions (known-node deletion). |
| 34 | Balanced versus unbalanced BST? | Rotations bound height in AVL/red-black trees; plain BST can become a chain. |
| 35 | B+ tree versus trie? | B+ tree exploits page fanout and ordered leaf scans; trie exploits shared key prefixes. |
| 36 | Fenwick versus segment tree? | Both can do point updates/range sums `O(log n)`; segment tree supports more general aggregates/updates at higher code/space cost. |
| 37 | Heap build versus repeated insertion? | Bottom-up build is `O(n)`; `n` separate inserts `O(n log n)`. |
| 38 | Why isn't a heap sorted? | Only parent–child priority is guaranteed; arbitrary search costs `O(n)`. |
| 39 | When is Dijkstra invalid? | A reachable negative edge can break greedy finalization; use Bellman–Ford or another suited algorithm. |
| 40 | Cycle detection in directed versus undirected graph? | Directed DFS tracks recursion-path states; undirected DFS ignores the edge to parent (or use disjoint set for edge additions). |
| 41 | What is topological order? | Linear order where each DAG edge `u → v` puts `u` before `v`; cycles make it impossible. |
| 42 | Prefix sum versus Fenwick tree? | Static prefix queries `O(1)` after `O(n)` build; frequent updates justify `O(log n)` Fenwick operations. |
| 43 | Quickselect versus sort for kth? | Expected `O(n)` partition selection vs `O(n log n)` full sort; bad pivots may make quickselect `O(n²)`. |
| 44 | Why track minimum in maximum-product subarray? | A negative number turns a large negative product into the next maximum. |
| 45 | Why is radix not a universal `O(n)` sort? | Complexity includes digits/base and a stable digit pass; representation limits apply. |
| 46 | Does JS `.sort()` order numbers correctly by default? | No; default compares as strings. Pass `(a,b) => a-b`; `sort()` mutates. |

## Coding prompts — say invariant and edge cases first

| Prompt | Key invariant / failure case | Worked example |
| --- | --- | --- |
| Rotate array by `k` | Normalize `k % n`; handle empty; reversal trick `O(n)`/`O(1)` extra | [array examples](./array/1.arrayExample.md) |
| Remove duplicates from sorted array | `[0,write)` holds unique values; empty input | [array examples](./array/1.arrayExample.md) |
| Matrix rotate | Square & mutable? transpose then reverse rows; else new matrix | [core Q&A](./coreQuestion.md) |
| Pair sum, kth, median of sorted arrays | Define uniqueness, 1-based `k`, both-empty | [advanced patterns](./advance_ds_question.md) |
| Product except self / rain water | Prefix × suffix; lower boundary is settled | [advanced patterns](./advance_ds_question.md) |
| Longest consecutive / majority / rotated search | Start-only expansion; verify candidate; duplicates degrade search | [advanced patterns](./advance_ds_question.md) |
| Reverse/cycle/nth-from-end list | Save next; fast/slow; validate `n` | [linked-list notes](./linked%20list/00.Linked%20Lists.md) |
| Balanced brackets / BFS / min-stack | LIFO pairs; mark visited on enqueue; parallel minima | [stack/queue notes](./Stacks%20and%20Queues/index.md) |
| Tree height / validate BST / kth in BST | Define height; bounds not only parent; inorder property | [tree notes](./trees.md) |
| Top K / graph shortest path | Heap size `k`; ask if edges weighted or negative | [heap](./heaps.md) · [graph](./graphs.md) |

## Architecture questions — go beyond Big-O

1. **Design a local LRU cache.** Which unit is capacity (entries/bytes)? What happens on update, eviction, zero capacity and concurrent access? A map plus doubly list handles recency; TTL and durability are separate.
2. **Choose an index for autocomplete.** A trie gives prefix traversal, but a DB/search index may be simpler; discuss update frequency, ranking, Unicode normalization and memory.
3. **Build a job scheduler.** Heap for earliest deadline, map for task lookup, durable queue for crash recovery. What about retry, idempotency and worker races?
4. **Store social connections.** Adjacency list for sparse relationships. Use bounded-depth graph traversal and precomputed views when fan-out or latency demands it; distinguish in-memory graph model from distributed storage.
5. **Support many changing range sums.** Prefix sums if mostly reads/static input; Fenwick/segment tree if updates frequent. Clarify range semantics and whether writes need atomicity.
6. **Sort data larger than memory.** External merge sort processes sorted runs on disk; a DB index can serve ordered queries. Discuss I/O, pagination and whether a full sort is even needed.

### Last-minute checklist

- [ ] I can answer Tier 1 in my own words, not recite a table.
- [ ] For each Big-O I can name its assumption (balanced, expected, amortized, known node, representation).
- [ ] I can trace an empty input, a duplicate and a large input for my chosen algorithm.
- [ ] I can justify a real-system trade-off: memory, cache locality, GC, persistence, concurrency or network.

**Revision schedule:** one pass now, retest tomorrow, then retest one week later. If you miss a question, follow its link and draw the invariant; do not reread every page.
