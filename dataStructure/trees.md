# Trees — height is the hidden variable

A tree represents a hierarchy. In a binary tree each node has at most two children; **binary** alone says nothing about ordering or balance. For `n` nodes, many costs depend on height `h`: balanced `h = O(log n)`, a chain `h = O(n)`.

```text
        8              BST invariant: every left descendant < node < every right descendant
       / \             search 6: 8 -> 3 -> 6
      3  10
     / \   \
    1   6   14
```

| Type                   | Invariant / purpose                                           | Key cost                                        | When to choose                                 |
| ---------------------- | ------------------------------------------------------------- | ----------------------------------------------- | ---------------------------------------------- |
| Binary tree            | At most two children; no order promised                       | search `O(n)`                                   | parsers, arbitrary hierarchy                   |
| BST                    | left keys smaller, right keys larger (state duplicate policy) | `O(h)` lookup/insert/delete; can be `O(n)`      | ordered lookup when height controlled          |
| AVL / red-black tree   | Self-balancing BST                                            | `O(log n)` worst-case lookup/insert/delete      | in-memory ordered maps/sets                    |
| B-tree / B+ tree       | High branching factor, few page reads                         | `O(log n)` node visits (base depends on fanout) | disk/page-oriented indexes, range queries      |
| Trie                   | shared key prefixes                                           | `O(L)` lookup/insert (`L` = key length)         | many prefix queries                            |
| Heap                   | parent dominates child                                        | `O(1)` best-at-root, `O(log n)` update          | scheduling / Top K; [details](./heaps.md)      |
| Fenwick / segment tree | aggregate over indexed intervals                              | `O(log n)` point update and range query         | changing sums/minima; storage typically `O(n)` |

**Do not say every DB uses a B+ tree.** Index implementations vary by engine and index type. B+ trees store searchable records at leaves (often linked for range iteration); disk-oriented fanout reduces page reads. A trie path is a prefix but usually needs an end-of-word marker (`car` and `cart` can coexist). Alphabet size and node representation affect trie memory.

## Traversal: draw it once

```text
        1
       / \
      2   3
     / \
    4   5
preorder  root,left,right: 1 2 4 5 3  (serialize)
inorder   left,root,right: 4 2 5 1 3  (sorted only for a BST)
postorder left,right,root: 4 5 2 3 1  (children before parent)
level-order, queue:      1 2 3 4 5  (BFS)
```

All traversals visit `n` nodes: `O(n)` time. DFS recursion needs `O(h)` stack; BFS queue can need `O(w)` where `w` is maximum width. Empty tree: height convention differs (edges = -1, nodes = 0); state your convention.

**Why balancing matters:** Inserting `1,2,3,4` into an ordinary BST creates a chain, so lookup is `O(n)`. Rotations restore a height bound in a self-balancing BST. A balanced tree's memory access pattern can still be slower than an array scan for small inputs; measure.

**Architecture lens:** File hierarchies and DOM trees favor traversal; ordered in-memory maps favor balanced trees; autocomplete may use tries; persistent range indexes may use B+ trees; mutable interval sums call for Fenwick/segment trees. Pick based on queries and updates, not names.

**Recall:** Is every binary tree searchable in `O(log n)`? Why is inorder sorted only for BST? What does `L` mean for trie complexity?
