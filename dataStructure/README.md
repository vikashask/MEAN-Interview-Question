# Data Structures — fast path, deep understanding

> Read in a dark-themed Markdown preview if you prefer; this guide uses text diagrams and contrast-independent labels rather than color. You do **not** have to memorize every implementation. Remember the invariant, operation cost, and trade-off.

## If time is short

| Time | Do this | Outcome |
| --- | --- | --- |
| 15 minutes | Read the decision table below and [interview questions](./interview-questions.md) (Tier 1) | Recognize the right structure and avoid common traps |
| 45 minutes | Add [arrays](./array/array.md), [hashes](./hash-tables.md), [stacks/queues](./Stacks%20and%20Queues/index.md), [trees](./trees.md) | Explain the highest-frequency choices |
| 90 minutes | Add [linked lists](./linked%20list/00.Linked%20Lists.md), [heaps](./heaps.md), [graphs](./graphs.md), [sorting](./shorting/index.md) | Handle common coding and architecture follow-ups |
| Later | Work examples and [advanced array problems](./advance_ds_question.md); run the JS/Python files | Build recall through traces and implementation |

**Learning loop (5 minutes per topic):** 1. Say the invariant aloud. 2. Trace one example by hand. 3. Name the operation and its *conditions* for the stated Big-O. 4. Explain a real product use. 5. Answer two questions without looking. Return tomorrow and a week later.

## Choose by operation, not by fashion

| Need | Start with | Why / caution |
| --- | --- | --- |
| Index-based reads, compact iteration | Array | `O(1)` access; front/middle insertion shifts elements |
| Membership or lookup by key | `Map` / `Set` | Average `O(1)`; memory overhead and no sorted order |
| Frequent edits *at a known node* | Linked list | `O(1)` pointer change; finding the node is still `O(n)` |
| Undo / nested evaluation | Stack | LIFO; JS array `push`/`pop` |
| Work in arrival order / BFS | Queue | FIFO; use head index or deque, not repeated JS `shift()` |
| Repeated best-priority extraction | Heap / priority queue | `O(1)` peek, `O(log n)` insert/remove; not fully sorted |
| Ordered lookups and ranges | Balanced search tree / B+ tree | `O(log n)` height; plain BST can degrade to `O(n)` |
| Prefix lookups | Trie | `O(L)` for key length `L`, at a memory cost |
| Relationships / routes | Graph adjacency list | Traversals `O(V+E)`; shortest path depends on edge weights |
| Fast sum over changing intervals | Fenwick / segment tree | Usually `O(log n)` point update and range query |

**Big-O is conditional.** Specify average vs worst, whether you have a pointer, whether the tree is balanced, and whether memory is auxiliary or includes output. Big-O does not capture constant factors, CPU cache behavior, GC overhead, or network/storage latency.

## The mental map

```text
Data structures (how to store)
├─ Linear: array, linked list, stack, queue
├─ Keyed: hash table (Map/Set)
├─ Hierarchical: BST, balanced tree, heap, trie, range tree
└─ Relational: graph
Algorithms (what to do): search, sort, traverse, select
Patterns (how to think): two pointers, sliding window, prefix sums,
                        fast/slow pointers, BFS/DFS, binary search
```

| Topic | Learn this invariant | Practice |
| --- | --- | --- |
| [Complexity + roadmap](./dataStructure%20roadmap.md) | Workload and access pattern determine the cost | Compare two options aloud |
| [Arrays](./array/array.md) · [examples](./array/1.arrayExample.md) · [Python notebook](./array/array.ipynb) | Index access versus element shifting | Rotate, deduplicate, binary search |
| [Strings](./JavaScript%20Strings.md) | JS strings are immutable; indices are UTF-16 units | Frequency, palindrome, Unicode |
| [Hash tables](./hash-tables.md) | Hash to bucket, resolve collision | Two Sum, frequency count |
| [Linked lists](./linked%20list/00.Linked%20Lists.md) · [JS basics](./linked%20list/01.beginner.js) · [JS advanced](./linked%20list/03.expert%20javascript.js) · [Python](./linked%20list/04.expert%20javascript.py) | Preserve the next link while rewiring | Reverse, cycle, LRU |
| [Stacks and queues](./Stacks%20and%20Queues/index.md) · [stack JS](./Stacks%20and%20Queues/Stack1.js) | LIFO vs FIFO | Brackets, BFS, minimum stack |
| [Trees](./trees.md) | BST ordering; balanced height bounds work | Traversal, range, trie |
| [Heaps](./heaps.md) | Parent dominates children, not siblings | Top K, scheduling |
| [Graphs](./graphs.md) | Vertices + edges; visited controls traversal | BFS/DFS, shortest path |
| [Sorting](./shorting/index.md) · [alternative overview](./typeOfShorting.md) | Stability, mutation, constraints, worst case | Merge vs quick vs heap |
| [Core array Q&A](./coreQuestion.md) · [advanced patterns](./advance_ds_question.md) | State assumptions before choosing algorithm | Re-derive, do not memorize |
| [Interview questions](./interview-questions.md) | Explain *why*, then code | Tier 1 before Tier 2 |

### Architecture lens

In production, pick based on the *dominant* operation: an LRU cache combines a hash map with a doubly linked list; a scheduler uses a heap plus a map of task metadata; a search index uses an inverted index; a DB index may use a B+ tree for locality and ranges. These are conceptual designs, not a promise about a particular runtime's internal representation. Ask about size, update/read ratio, ordering, consistency, memory limit and failure behavior before choosing.

**A 30-second explanation template:** “We need [operation]. I choose [structure] because its invariant makes that [cost, with condition]. We pay [memory/other operation]. At scale I'd watch [cache behavior, contention, persistence or failure].”
