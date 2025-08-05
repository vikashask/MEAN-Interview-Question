## What is an array and how is it different from a linked list?

An array is a data structure that stores a collection of elements of the same data type in contiguous memory locations. This means that the elements are stored one after another in a single block of memory. Because of this, you can access any element in an array directly using its index.

A linked list is a data structure that stores a collection of elements, called nodes, where each node contains a value and a pointer to the next node in the sequence. Unlike arrays, the nodes in a linked list are not stored in contiguous memory locations.

**Key Differences:**

| Feature | Array | Linked List |
| :--- | :--- | :--- |
| **Memory Allocation** | Contiguous | Non-contiguous |
| **Element Access** | O(1) (Direct access) | O(n) (Sequential access) |
| **Insertion/Deletion** | O(n) (at the beginning or middle) | O(1) (if you have a pointer to the node) |
| **Size** | Fixed (in many languages) | Dynamic |

---

## What are the advantages and disadvantages of arrays?

**Advantages:**

*   **Fast Access:** Accessing an element by its index is very fast (O(1) time complexity).
*   **Memory Efficiency:** Arrays are memory-efficient as they don't store any extra pointers, unlike linked lists.
*   **Easy to Implement:** Arrays are simple to create and use.

**Disadvantages:**

*   **Fixed Size:** In many programming languages, the size of an array is fixed when it's created. Resizing an array can be an expensive operation.
*   **Inefficient Insertions/Deletions:** Inserting or deleting elements in the middle of an array requires shifting subsequent elements, which is slow (O(n) time complexity).

---

## Can arrays be resized at runtime? If not, why?

In some languages (like C++ or Java), traditional arrays have a fixed size and cannot be resized at runtime. This is because the memory for the array is allocated as a single, contiguous block. To "resize" it, you would need to create a new, larger array and copy all the elements from the old array to the new one.

However, many modern languages provide "dynamic arrays" (like `std::vector` in C++, `ArrayList` in Java, or lists in Python) that can be resized.

---

## Explain how arrays are stored in memory and how memory allocation is handled.

Arrays are stored in a contiguous block of memory. When you declare an array, the compiler or runtime allocates a single chunk of memory large enough to hold all the elements. The address of the first element is the base address of the array.

To access an element at a given index, the memory address is calculated using the formula:

```
address_of_element = base_address + (index * size_of_one_element)
```

This is why array access is so fast.

---

## How do dynamic arrays work behind the scenes?

Dynamic arrays (like Python lists or C++ vectors) are built on top of static arrays. They work by:

1.  **Allocating an initial array:** When you create a dynamic array, it allocates an underlying static array with a certain initial capacity.
2.  **Adding elements:** As you add elements, they are placed in the underlying array.
3.  **Resizing:** When the underlying array becomes full, the dynamic array automatically:
    *   Allocates a new, larger static array (often double the size of the old one).
    *   Copies all the elements from the old array to the new one.
    *   Deallocates the old array.

This resizing process is what allows dynamic arrays to grow as needed.

---

## What’s the time complexity of various operations (insert, delete, access) on an array?

| Operation | Time Complexity | Explanation |
| :--- | :--- | :--- |
| **Access (by index)** | O(1) | You can directly calculate the memory address. |
| **Search (unsorted)** | O(n) | You may have to look at every element. |
| **Search (sorted)** | O(log n) | You can use binary search. |
| **Insertion (at the end)** | O(1) (amortized for dynamic arrays) | If there's space, it's fast. If not, resizing takes O(n). |
| **Insertion (at the beginning/middle)** | O(n) | You have to shift all subsequent elements. |
| **Deletion (at the end)** | O(1) | Just remove the last element. |
| **Deletion (at the beginning/middle)** | O(n) | You have to shift all subsequent elements. |

---

## How do you declare and initialize a multi-dimensional array in your favorite language?

In JavaScript:

```javascript
// 2D array (matrix)
let matrix = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
];

// Accessing an element
console.log(matrix[1][2]); // Output: 6
```

---

## How would you find the intersection or union of two arrays?

**Intersection** (elements present in both arrays):

```javascript
function intersection(arr1, arr2) {
  const set1 = new Set(arr1);
  const result = [];
  for (const element of arr2) {
    if (set1.has(element)) {
      result.push(element);
    }
  }
  return result;
}
```

**Union** (all unique elements from both arrays):

```javascript
function union(arr1, arr2) {
  const set = new Set([...arr1, ...arr2]);
  return Array.from(set);
}
```

---

## How would you rotate a 2D matrix by 90 degrees?

To rotate a 2D matrix by 90 degrees clockwise, you can follow these two steps:

1.  **Transpose the matrix:** Swap the rows and columns. The element at `(i, j)` becomes the element at `(j, i)`.
2.  **Reverse each row:** Reverse the order of elements in each row.

```javascript
function rotateMatrix(matrix) {
  const n = matrix.length;

  // Transpose the matrix
  for (let i = 0; i < n; i++) {
    for (let j = i; j < n; j++) {
      [matrix[i][j], matrix[j][i]] = [matrix[j][i], matrix[i][j]];
    }
  }

  // Reverse each row
  for (let i = 0; i < n; i++) {
    matrix[i].reverse();
  }

  return matrix;
}
```