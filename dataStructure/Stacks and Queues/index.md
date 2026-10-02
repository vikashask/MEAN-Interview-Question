# Stacks and queues — order is the contract

| Structure | Invariant | Core operations | Typical use |
| --- | --- | --- | --- |
| Stack | Last in, first out (LIFO) | push/pop/peek `O(1)` amortized with JS array | Undo, call stack, balanced brackets, DFS |
| Queue | First in, first out (FIFO) | enqueue/dequeue `O(1)` amortized with head index | BFS, work scheduling, message processing |
| Deque | Both ends | `O(1)` end operations with appropriate implementation | Sliding-window maximum |

```text
stack: push A, push B, pop -> B   (plates)
queue: add A, add B, take -> A   (line)
```

## In JavaScript

[The runnable stack example](./Stack1.js) uses array `push`/`pop`. **Avoid `array.shift()` in a hot FIFO loop:** removal at index 0 may shift `n-1` elements, costing `O(n)` per dequeue. A head-index queue retains consumed slots until compacted; the following example uses `O(n)` storage for the lifetime of the batch and constant-time dequeue, with periodic compaction needed for a long-lived service:

```js
const items = [];
let head = 0;
items.push('A', 'B');
const first = head < items.length ? items[head++] : undefined; // 'A'
if (head === items.length) { items.length = 0; head = 0; }
```

For long-lived queues compact occasionally when consumed prefix exceeds a threshold, or use a linked-node/deque implementation. `Array.prototype.push` can occasionally resize the backing store; **amortized** is the accurate bound.

## Problem triggers

- **Balanced brackets:** push opening symbol; on a closing one, pop and check its pair. Empty stack at the end means balanced. Time `O(n)`, space `O(n)` worst.
- **BFS shortest path in an unweighted graph:** enqueue start, mark visited *on enqueue*, process neighbors. Each vertex/edge visited at most once: `O(V+E)`.
- **Queue with two stacks:** push into `in`; if `out` is empty, transfer everything from `in` to `out`; pop from `out`. Each item moves at most twice: **amortized** `O(1)` dequeue, worst single dequeue `O(n)`.
- **Min stack:** keep a parallel stack of current minima; push/pop both, `getMin()` `O(1)` at `O(n)` extra space.

**Architecture lens:** A process-local queue is not a durable message broker. If workers crash, need retries, deduplication, backpressure or ordering across hosts, design a persistent queue and define delivery semantics separately.

**Recall:** Why does JS `shift()` differ from dequeue on a linked queue? Why mark visited at enqueue rather than dequeue? What does amortized mean?
