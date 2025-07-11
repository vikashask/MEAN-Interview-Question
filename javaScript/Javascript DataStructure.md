# JavaScript Data Structures

## Arrays and Array Methods

### Array Manipulation
```javascript
// Creating arrays
const arr1 = [1, 2, 3];
const arr2 = new Array(4, 5, 6);
const arr3 = Array.from('hello'); // ['h', 'e', 'l', 'l', 'o']

// Adding/Removing elements
arr1.push(4);        // Add to end
arr1.pop();          // Remove from end
arr1.unshift(0);     // Add to start
arr1.shift();        // Remove from start
arr1.splice(1, 1);   // Remove at index
```

### Array Methods
```javascript
// Map, Filter, Reduce
const numbers = [1, 2, 3, 4, 5];

const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);
const sum = numbers.reduce((acc, n) => acc + n, 0);

// Sort and Reverse
numbers.sort((a, b) => a - b);  // Ascending
numbers.sort((a, b) => b - a);  // Descending
numbers.reverse();
```

## Linked Lists

### Singly Linked List
```javascript
class Node {
    constructor(data) {
        this.data = data;
        this.next = null;
    }
}

class LinkedList {
    constructor() {
        this.head = null;
    }
    
    append(data) {
        const newNode = new Node(data);
        
        if (!this.head) {
            this.head = newNode;
            return;
        }
        
        let current = this.head;
        while (current.next) {
            current = current.next;
        }
        current.next = newNode;
    }
    
    delete(data) {
        if (!this.head) return;
        
        if (this.head.data === data) {
            this.head = this.head.next;
            return;
        }
        
        let current = this.head;
        while (current.next) {
            if (current.next.data === data) {
                current.next = current.next.next;
                return;
            }
            current = current.next;
        }
    }
}
```

### Doubly Linked List
```javascript
class DoublyNode {
    constructor(data) {
        this.data = data;
        this.prev = null;
        this.next = null;
    }
}

class DoublyLinkedList {
    constructor() {
        this.head = null;
        this.tail = null;
    }
    
    append(data) {
        const newNode = new DoublyNode(data);
        
        if (!this.head) {
            this.head = newNode;
            this.tail = newNode;
            return;
        }
        
        newNode.prev = this.tail;
        this.tail.next = newNode;
        this.tail = newNode;
    }
}
```

## Stacks and Queues

### Stack Implementation
```javascript
class Stack {
    constructor() {
        this.items = [];
    }
    
    push(element) {
        this.items.push(element);
    }
    
    pop() {
        if (this.isEmpty()) return null;
        return this.items.pop();
    }
    
    peek() {
        if (this.isEmpty()) return null;
        return this.items[this.items.length - 1];
    }
    
    isEmpty() {
        return this.items.length === 0;
    }
    
    size() {
        return this.items.length;
    }
}
```

### Queue Implementation
```javascript
class Queue {
    constructor() {
        this.items = {};
        this.frontIndex = 0;
        this.backIndex = 0;
    }
    
    enqueue(element) {
        this.items[this.backIndex] = element;
        this.backIndex++;
    }
    
    dequeue() {
        if (this.isEmpty()) return null;
        
        const item = this.items[this.frontIndex];
        delete this.items[this.frontIndex];
        this.frontIndex++;
        return item;
    }
    
    isEmpty() {
        return this.frontIndex === this.backIndex;
    }
    
    size() {
        return this.backIndex - this.frontIndex;
    }
}
```

## Trees

### Binary Search Tree
```javascript
class TreeNode {
    constructor(data) {
        this.data = data;
        this.left = null;
        this.right = null;
    }
}

class BinarySearchTree {
    constructor() {
        this.root = null;
    }
    
    insert(data) {
        const newNode = new TreeNode(data);
        
        if (!this.root) {
            this.root = newNode;
            return;
        }
        
        this.insertNode(this.root, newNode);
    }
    
    insertNode(node, newNode) {
        if (newNode.data < node.data) {
            if (!node.left) {
                node.left = newNode;
            } else {
                this.insertNode(node.left, newNode);
            }
        } else {
            if (!node.right) {
                node.right = newNode;
            } else {
                this.insertNode(node.right, newNode);
            }
        }
    }
    
    inOrderTraversal(node = this.root) {
        if (node) {
            this.inOrderTraversal(node.left);
            console.log(node.data);
            this.inOrderTraversal(node.right);
        }
    }
}
```

## Hash Tables

### Basic Hash Table
```javascript
class HashTable {
    constructor(size = 53) {
        this.keyMap = new Array(size);
    }
    
    _hash(key) {
        let total = 0;
        const WEIRD_PRIME = 31;
        
        for (let i = 0; i < Math.min(key.length, 100); i++) {
            const char = key[i];
            const value = char.charCodeAt(0) - 96;
            total = (total * WEIRD_PRIME + value) % this.keyMap.length;
        }
        
        return total;
    }
    
    set(key, value) {
        const index = this._hash(key);
        
        if (!this.keyMap[index]) {
            this.keyMap[index] = [];
        }
        
        this.keyMap[index].push([key, value]);
    }
    
    get(key) {
        const index = this._hash(key);
        
        if (this.keyMap[index]) {
            for (let i = 0; i < this.keyMap[index].length; i++) {
                if (this.keyMap[index][i][0] === key) {
                    return this.keyMap[index][i][1];
                }
            }
        }
        
        return undefined;
    }
}
```

## Graphs

### Adjacency List Graph
```javascript
class Graph {
    constructor() {
        this.adjacencyList = {};
    }
    
    addVertex(vertex) {
        if (!this.adjacencyList[vertex]) {
            this.adjacencyList[vertex] = [];
        }
    }
    
    addEdge(vertex1, vertex2) {
        this.adjacencyList[vertex1].push(vertex2);
        this.adjacencyList[vertex2].push(vertex1);
    }
    
    removeEdge(vertex1, vertex2) {
        this.adjacencyList[vertex1] = this.adjacencyList[vertex1]
            .filter(v => v !== vertex2);
        this.adjacencyList[vertex2] = this.adjacencyList[vertex2]
            .filter(v => v !== vertex1);
    }
    
    removeVertex(vertex) {
        while (this.adjacencyList[vertex].length) {
            const adjacentVertex = this.adjacencyList[vertex].pop();
            this.removeEdge(vertex, adjacentVertex);
        }
        delete this.adjacencyList[vertex];
    }
}
```

## Best Practices

1. Choose the Right Data Structure
   - Arrays for ordered data
   - Hash Tables for key-value pairs
   - Trees for hierarchical data
   - Graphs for network-like data

2. Consider Time Complexity
   - Array operations: O(n) for insertions/deletions
   - Hash Table operations: O(1) average case
   - BST operations: O(log n) if balanced

3. Memory Usage
   - Arrays use contiguous memory
   - Linked Lists use scattered memory
   - Consider space-time tradeoffs

4. Implementation Tips
   - Use TypeScript for better type safety
   - Implement error handling
   - Add proper validation
   - Consider edge cases
