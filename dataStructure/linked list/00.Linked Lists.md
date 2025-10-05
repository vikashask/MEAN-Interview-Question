# Linked List Data Structures

This document explains the different types of linked lists and their fundamental operations.

---

### The Core Idea of a Linked List

A linked list is a linear data structure, but unlike an array, its elements are not stored at contiguous memory locations. The elements in a linked list are linked using pointers. Each element is a separate object called a **node**.

Each node contains two key pieces of information:
1.  The **data** it holds.
2.  A **pointer** (or "link") to the next node in the sequence.

The entry point to the list is a pointer to the first node, called the `head`. The end of the list is indicated by a node whose pointer is `null`.

---

### 1. Singly Linked List

This is the most basic form of a linked list.

*   **Structure:** Each node contains a single pointer that points to the **next** node in the chain. Traversal is only possible in one direction (forward).

*   **Diagram:**
    ```
    head
      |
      v
    [Data|Next] -> [Data|Next] -> [Data|Next] -> null
    ```

---

### 2. Doubly Linked List

This version provides more flexibility by allowing traversal in both directions.

*   **Structure:** Each node contains **two pointers**:
    1.  A `next` pointer, which points to the next node.
    2.  A `prev` (previous) pointer, which points to the node before it.

*   **Advantage:** This bidirectional linking makes some operations, like deleting a specific node or inserting a node before another, more efficient as you don't need to traverse the list from the beginning to find the previous node.

*   **Diagram:**
    ```
      +----------+      +----------+      +----------+
      |          v      |          v      |          v
    null <-[Prev|Data|Next]<->[Prev|Data|Next]<->[Prev|Data|Next]-> null
             ^          |      ^          |      ^          |
             +----------+      +----------+      +----------+
    ```

---

### 3. Circular Linked List

A circular linked list is a variation where the list forms a circle.

*   **Structure:** The `next` pointer of the last node points back to the `head` node instead of pointing to `null`. This can be implemented for both singly and doubly linked lists.

*   **Use Case:** Ideal for applications that require a continuous cycle, such as managing turns in a game, creating a music playlist loop, or round-robin scheduling algorithms.

*   **Diagram (Singly Circular):**
    ```
      +-----------------------------------------+
      |                                         |
      v                                         |
    [Data|Next] -> [Data|Next] -> [Data|Next] ---+
    ```

---

### Common Operations

Here’s how the main operations are conceptually performed on a standard singly linked list:

*   **Traversal:**
    1.  Create a temporary pointer, `current`, and initialize it with the `head`.
    2.  While `current` is not `null`:
        *   Process the data of the `current` node.
        *   Move to the next node by updating `current = current.next`.

*   **Insertion:**
    *   **At the beginning (prepending):**
        1.  Create a `newNode`.
        2.  Set `newNode.next` to the current `head`.
        3.  Update the `head` to be the `newNode`.
    *   **At the end (appending):**
        1.  Create a `newNode`.
        2.  Traverse the list to find the last node (where `next` is `null`).
        3.  Set the `next` pointer of that last node to the `newNode`.

*   **Deletion:**
    *   To delete a node, you must find the node **before** it (let's call it `previousNode`).
    *   You then update the pointers to "bypass" the node you want to remove.
    *   Set `previousNode.next` to `previousNode.next.next`. This unlinks the target node from the chain.
