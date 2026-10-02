# Core array questions — answer from first principles

For the mental model, read [arrays](./array/array.md); for runnable examples, read [array exercises](./array/1.arrayExample.md). Practice by stating assumptions, deriving the cost, then tracing an empty and a duplicate-filled input.

## 1. Array vs linked list?

|                      | Packed/dynamic array model                                     | Linked list                                                     |
| -------------------- | -------------------------------------------------------------- | --------------------------------------------------------------- |
| Index read           | `O(1)`                                                         | `O(n)`                                                          |
| Middle insert/remove | `O(n)` due to shifting                                         | `O(1)` **once predecessor/node is known**; finding it is `O(n)` |
| Memory               | contiguous slots, locality; dynamic capacity may reserve extra | separate nodes, link overhead, poorer locality                  |

JavaScript arrays are an abstraction: do not claim every JS array has fixed-size contiguous physical elements. [Linked-list details](./linked%20list/00.Linked%20Lists.md).

## 2. Why choose an array? When not?

Choose for indexed reads, scans, good locality and built-in ergonomics. Avoid repeated large front shifts or key lookups without an index; consider head-index queue, `Map`, heap or linked list as the operation requires. Measure in real JS before replacing an array.

## 3. Can arrays resize?

A fixed-size array cannot resize its original allocation; a **dynamic array** creates a larger backing store and copies elements when full. Python lists and JS arrays grow dynamically; C++ `std::vector` and Java `ArrayList` do as well. Single growth `O(n)`, amortized append `O(1)`.

## 4. Why is indexed access constant-time?

In the packed fixed-width model, `address = base + index × element_size` (subject to bounds). Not a claim about JS engine physical layout. A linked list must follow pointers instead.

## 5. What does amortized cost mean?

With capacity doubling, capacities `1,2,4,8,...` cause at most `1+2+4+... < 2n` element copies over `n` appends. Total `O(n)` work → average **per operation over the sequence** `O(1)`, even though one append can be `O(n)`.

## 6. Operation costs?

| Indexed access | Unsorted search | Sorted binary search | End append       | Front/middle edit |
| -------------- | --------------- | -------------------- | ---------------- | ----------------- |
| `O(1)`         | `O(n)`          | `O(log n)` if sorted | `O(1)` amortized | `O(n)` shift      |

## 7. How do you make a matrix in JS?

```js
const rows = 2,
  cols = 3;
const matrix = Array.from({ length: rows }, () => Array(cols).fill(0));
matrix[1][2] = 7; // distinct row arrays
```

Do **not** use `Array(rows).fill(Array(cols).fill(0))`: all rows then reference the _same_ inner array. For a square in-place rotation, transpose, then reverse each row; `O(n²)` time and `O(1)` extra space.

## 8. Intersection and union of arrays?

Decide whether output is unique, sorted, or should preserve duplicates. For **unique** values:

```js
const a = [1, 2, 2],
  b = [2, 2, 3];
const bSet = new Set(b);
const intersection = [...new Set(a)].filter((x) => bSet.has(x)); // [2]
const union = [...new Set([...a, ...b])]; // [1, 2, 3]
```

Expected `O(n+m)` time/space with hash-based sets; for sorted arrays a two-pointer scan can avoid a hash index (output aside).

## 9. Rotate a square matrix 90° clockwise?

Transpose `(i,j) ↔ (j,i)` for `j > i`, then reverse each row. Preconditions: square `n × n` array, mutation allowed. Example: `[[1,2],[3,4]] → [[3,1],[4,2]]`. If input is rectangular or must be immutable, allocate a new matrix and map `result[j][rows - 1 - i] = input[i][j]`.

**Recall:** When is a linked-list insertion actually `O(1)`? What does `Array.fill(innerArray)` alias? Does the meaning of “intersection” include multiplicity?
