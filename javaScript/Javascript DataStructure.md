# JavaScript Data Structures

## Arrays
Arrays are used to store multiple values in a single variable.

```javascript
let fruits = ['Apple', 'Banana', 'Orange'];
```

### Common Array Methods
* `push()` - Add elements to the end
* `pop()` - Remove element from the end
* `shift()` - Remove element from the beginning
* `unshift()` - Add elements to the beginning
* `splice()` - Add/Remove elements from any position

## Objects
Objects store data in key-value pairs.

```javascript
let person = {
    name: 'John',
    age: 30,
    city: 'New York'
};
```

## Sets
Sets are collections of unique values.

```javascript
let mySet = new Set();
mySet.add(1);
mySet.add(2);
mySet.add(2); // Won't add duplicate
```

## Maps
Maps hold key-value pairs where both keys and values can be of any type.

```javascript
let myMap = new Map();
myMap.set('name', 'John');
myMap.set(1, 'number one');
```

## Stack
Last In First Out (LIFO) data structure.

```javascript
class Stack {
    constructor() {
        this.items = [];
    }
    
    push(element) {
        this.items.push(element);
    }
    
    pop() {
        return this.items.pop();
    }
}
```

## Queue
First In First Out (FIFO) data structure.

```javascript
class Queue {
    constructor() {
        this.items = [];
    }
    
    enqueue(element) {
        this.items.push(element);
    }
    
    dequeue() {
        return this.items.shift();
    }
}
```

## Linked List
A sequence of elements where each element points to the next element.

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
}
```

## Tree
Hierarchical data structure with a root value and subtrees of children.

```javascript
class TreeNode {
    constructor(value) {
        this.value = value;
        this.left = null;
        this.right = null;
    }
}
```
