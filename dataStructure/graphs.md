# Graphs — relationships with explicit costs

A graph has vertices `V` and edges `E`; it may be directed/undirected, weighted/unweighted, cyclic/acyclic. Ask these questions *before* choosing an algorithm. A tree is a special connected, acyclic graph.

## Representation

```text
A -- B -- D       adjacency list: A: [B,C], B: [A,D], C: [A], D: [B]
|                undirected edges appear at both endpoints
C
```

| Structure | Space | Edge test | Iterate neighbors | Choose when |
| --- | --- | --- | --- | --- |
| Adjacency list | `O(V+E)` | `O(degree(v))` with arrays; average `O(1)` with neighbor sets | `O(degree(v))` | Sparse graphs, traversals |
| Adjacency matrix | `O(V²)` | `O(1)` | `O(V)` | Dense graphs, frequent edge tests |

## Traversals: same cost, different order

**BFS** uses a queue and visits by hop count: shortest *number of edges* in an **unweighted** graph. **DFS** uses recursion or a stack: explores a branch, backtracks; handy for components, cycle detection and topological ordering. Both cost `O(V+E)` with an adjacency list and visited set, assuming the reachable graph is traversed (or run from all vertices).

```js
function bfs(graph, start) {
  const seen = new Set([start]);
  const queue = [start];
  for (let head = 0; head < queue.length; head++) {
    for (const next of graph.get(queue[head]) ?? []) {
      if (!seen.has(next)) { seen.add(next); queue.push(next); }
    }
  }
  return [...seen];
}
```

For path reconstruction, record `parent[next] = current` when first discovered. `seen` on enqueue prevents repeated entries; recursion-based DFS may use `O(V)` call-stack space and can overflow on deep graphs.

## Shortest path decision

| Edges | Algorithm | Cost (adjacency list) | Caveat |
| --- | --- | --- | --- |
| Unweighted/equal cost | BFS | `O(V+E)` | Minimizes hops |
| Nonnegative weights | Dijkstra + binary heap | `O((V+E) log V)` | Negative weights invalidate greedy choice |
| Negative weights, no negative cycle on target path | Bellman–Ford | `O(VE)` | Can detect reachable negative cycles |
| Directed acyclic graph | Topological order + relax edges | `O(V+E)` | Requires DAG |

**Architecture lens:** Social follows and dependencies may be graphs, but traversing an entire production graph per HTTP request is rarely acceptable. Specify hop limits, pagination and precomputation/caching; decide what happens if data changes mid-traversal. Route planning needs edge weights, not just BFS.

**Recall:** BFS versus DFS for unweighted shortest path? Why does a matrix waste space on sparse graphs? When is Dijkstra invalid?
