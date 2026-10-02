# Data-structure roadmap: learn by access pattern

Start at [README](./README.md). You do not need to master everything in one pass. For each structure, be able to state: **invariant → fast operation → expensive operation → example**.

## Three passes

| Pass                     | Topics                                                                                                                                                   | Checkpoint                                          |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| 1: highest return        | [arrays](./array/array.md), [strings](./JavaScript%20Strings.md), [hash tables](./hash-tables.md), [stacks and queues](./Stacks%20and%20Queues/index.md) | Explain Two Sum, binary search and BFS queue choice |
| 2: pointers and ordering | [linked lists](./linked%20list/00.Linked%20Lists.md), [trees](./trees.md), [heaps](./heaps.md), [sorting](./shorting/index.md)                           | Trace pointer rewiring; pick heap vs balanced tree  |
| 3: connected data        | [graphs](./graphs.md), [advanced patterns](./advance_ds_question.md), [interview questions](./interview-questions.md)                                    | Explain BFS/DFS and shortest path assumptions       |

## Complexity without misleading shortcuts

`n` = number of elements, `V` = vertices, `E` = edges, `L` = key length; bounds below describe specific operations. Unless stated, lookup is by **value/key**, not by index.

| Structure            | Indexed access         | Find value / key                                     | Insert / remove                                                         | What changes the bound?                                   |
| -------------------- | ---------------------- | ---------------------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------- |
| Dynamic array        | `O(1)`                 | `O(n)` unsorted; `O(log n)` sorted via binary search | end append `O(1)` amortized; start/middle `O(n)`                        | resize costs `O(n)` occasionally                          |
| Singly linked list   | `O(n)`                 | `O(n)`                                               | head `O(1)`; at known predecessor `O(1)`                                | finding predecessor is `O(n)`; tail pointer speeds append |
| Stack                | not a useful operation | `O(n)` search                                        | top `O(1)` amortized with JS array                                      | only top is directly accessible                           |
| Queue                | not a useful operation | `O(n)` search                                        | ends `O(1)` amortized with deque/head-index; JS `shift()` can be `O(n)` | implementation matters                                    |
| Hash table           | not indexable in order | expected `O(1)` key lookup; worst `O(n)`             | expected `O(1)`; worst `O(n)`                                           | collisions/resize; no sorted-range guarantee              |
| Balanced BST         | no direct index        | `O(log n)`                                           | `O(log n)`                                                              | plain unbalanced BST may take `O(n)`                      |
| Binary heap          | root `O(1)`            | arbitrary key `O(n)`                                 | insert/remove root `O(log n)`                                           | heap orders parent-child only                             |
| Trie                 | not indexable          | `O(L)` for key                                       | `O(L)`                                                                  | memory depends on prefixes/alphabet                       |
| Graph adjacency list | varies                 | BFS/DFS across reachable graph `O(V+E)`              | edge addition often `O(1)` amortized                                    | graph density and visited representation                  |

**Space matters too:** arrays and heaps `O(n)`; linked lists `O(n)` with pointer overhead; adjacency list `O(V+E)` vs matrix `O(V²)`. `O(1)` in-process map lookup does not include a remote service's network latency.

## Repeat to remember

1. Choose a problem from [core Q&A](./coreQuestion.md) or [interview questions](./interview-questions.md).
2. Describe a brute-force solution, its time/space cost and a failing edge case.
3. State the invariant (e.g., “everything before the slow pointer is unique”).
4. Trace `[ ]`, a single value, duplicates and an already-sorted case.
5. Explain where this structure would live in a real service: memory, process, disk or distributed store.

**Memory anchor:** Array = index; Map = key; linked list = link; stack = last; queue = first; heap = best; BST = order; trie = prefix; graph = relationship.
