/**
 * ADVANCED LINKED LIST CONCEPTS IN JAVASCRIPT
 * ============================================
 */

// ============================================
// 1. DOUBLY LINKED LIST
// ============================================

class DoublyNode {
  constructor(data) {
    this.data = data;
    this.next = null;
    this.prev = null;
  }
}

class DoublyLinkedList {
  constructor() {
    this.head = null;
    this.tail = null;
    this.size = 0;
  }

  /**
   * Insert at beginning - O(1)
   */
  prepend(data) {
    const newNode = new DoublyNode(data);

    if (!this.head) {
      this.head = this.tail = newNode;
    } else {
      newNode.next = this.head;
      this.head.prev = newNode;
      this.head = newNode;
    }

    this.size++;
    return this;
  }

  /**
   * Insert at end - O(1)
   */
  append(data) {
    const newNode = new DoublyNode(data);

    if (!this.tail) {
      this.head = this.tail = newNode;
    } else {
      newNode.prev = this.tail;
      this.tail.next = newNode;
      this.tail = newNode;
    }

    this.size++;
    return this;
  }

  /**
   * Delete from beginning - O(1)
   */
  shift() {
    if (!this.head) return null;

    const removedData = this.head.data;

    if (this.head === this.tail) {
      this.head = this.tail = null;
    } else {
      this.head = this.head.next;
      this.head.prev = null;
    }

    this.size--;
    return removedData;
  }

  /**
   * Delete from end - O(1)
   */
  pop() {
    if (!this.tail) return null;

    const removedData = this.tail.data;

    if (this.head === this.tail) {
      this.head = this.tail = null;
    } else {
      this.tail = this.tail.prev;
      this.tail.next = null;
    }

    this.size--;
    return removedData;
  }

  /**
   * Traverse forward
   */
  toArrayForward() {
    const array = [];
    let current = this.head;

    while (current) {
      array.push(current.data);
      current = current.next;
    }

    return array;
  }

  /**
   * Traverse backward
   */
  toArrayBackward() {
    const array = [];
    let current = this.tail;

    while (current) {
      array.push(current.data);
      current = current.prev;
    }

    return array;
  }

  toString() {
    return "null <- " + this.toArrayForward().join(" <-> ") + " -> null";
  }

  print() {
    console.log(this.toString());
  }
}

// ============================================
// 2. CIRCULAR LINKED LIST
// ============================================

class CircularLinkedList {
  constructor() {
    this.head = null;
    this.size = 0;
  }

  /**
   * Insert at beginning - O(n)
   */
  prepend(data) {
    const newNode = new Node(data);

    if (!this.head) {
      this.head = newNode;
      newNode.next = newNode; // Point to itself
    } else {
      // Find last node
      let current = this.head;
      while (current.next !== this.head) {
        current = current.next;
      }

      newNode.next = this.head;
      current.next = newNode;
      this.head = newNode;
    }

    this.size++;
    return this;
  }

  /**
   * Insert at end - O(n)
   */
  append(data) {
    const newNode = new Node(data);

    if (!this.head) {
      this.head = newNode;
      newNode.next = newNode;
    } else {
      let current = this.head;
      while (current.next !== this.head) {
        current = current.next;
      }

      current.next = newNode;
      newNode.next = this.head;
    }

    this.size++;
    return this;
  }

  toArray() {
    if (!this.head) return [];

    const array = [];
    let current = this.head;

    do {
      array.push(current.data);
      current = current.next;
    } while (current !== this.head);

    return array;
  }

  toString() {
    return (
      this.toArray().join(" -> ") +
      ` -> ${this.head ? this.head.data : "null"} (circular)`
    );
  }

  print() {
    console.log(this.toString());
  }
}

// ============================================
// 3. COMMON INTERVIEW PROBLEMS
// ============================================

class Node {
  constructor(data) {
    this.data = data;
    this.next = null;
  }
}

/**
 * Problem 1: Reverse a Linked List
 * Time: O(n), Space: O(1)
 */
function reverseList(head) {
  let prev = null;
  let current = head;

  while (current) {
    const next = current.next;
    current.next = prev;
    prev = current;
    current = next;
  }

  return prev;
}

/**
 * Problem 2: Detect Cycle (Floyd's Algorithm)
 * Time: O(n), Space: O(1)
 */
function hasCycle(head) {
  if (!head || !head.next) return false;

  let slow = head;
  let fast = head;

  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;

    if (slow === fast) return true;
  }

  return false;
}

/**
 * Problem 3: Find Middle Element
 * Time: O(n), Space: O(1)
 */
function findMiddle(head) {
  if (!head) return null;

  let slow = head;
  let fast = head;

  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;
  }

  return slow;
}

/**
 * Problem 4: Merge Two Sorted Lists
 * Time: O(n + m), Space: O(1)
 */
function mergeTwoLists(l1, l2) {
  const dummy = new Node(0);
  let current = dummy;

  while (l1 && l2) {
    if (l1.data <= l2.data) {
      current.next = l1;
      l1 = l1.next;
    } else {
      current.next = l2;
      l2 = l2.next;
    }
    current = current.next;
  }

  current.next = l1 || l2;
  return dummy.next;
}

/**
 * Problem 5: Remove Nth Node From End
 * Time: O(n), Space: O(1)
 */
function removeNthFromEnd(head, n) {
  const dummy = new Node(0);
  dummy.next = head;

  let first = dummy;
  let second = dummy;

  // Move first n+1 steps ahead
  for (let i = 0; i <= n; i++) {
    first = first.next;
  }

  // Move both until first reaches end
  while (first) {
    first = first.next;
    second = second.next;
  }

  // Remove nth node
  second.next = second.next.next;
  return dummy.next;
}

/**
 * Problem 6: Check if Palindrome
 * Time: O(n), Space: O(1)
 */
function isPalindrome(head) {
  if (!head || !head.next) return true;

  // Find middle
  let slow = head;
  let fast = head;

  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;
  }

  // Reverse second half
  let prev = null;
  while (slow) {
    const next = slow.next;
    slow.next = prev;
    prev = slow;
    slow = next;
  }

  // Compare both halves
  let left = head;
  let right = prev;

  while (right) {
    if (left.data !== right.data) return false;
    left = left.next;
    right = right.next;
  }

  return true;
}

/**
 * Problem 7: Find Intersection of Two Lists
 * Time: O(n + m), Space: O(1)
 */
function getIntersectionNode(headA, headB) {
  if (!headA || !headB) return null;

  let a = headA;
  let b = headB;

  // When reaching end, switch to other list
  // They will meet at intersection or both become null
  while (a !== b) {
    a = a ? a.next : headB;
    b = b ? b.next : headA;
  }

  return a;
}

/**
 * Problem 8: Remove Duplicates from Sorted List
 * Time: O(n), Space: O(1)
 */
function deleteDuplicates(head) {
  let current = head;

  while (current && current.next) {
    if (current.data === current.next.data) {
      current.next = current.next.next;
    } else {
      current = current.next;
    }
  }

  return head;
}

/**
 * Problem 9: Rotate List by K positions
 * Time: O(n), Space: O(1)
 */
function rotateRight(head, k) {
  if (!head || !head.next || k === 0) return head;

  // Find length and make circular
  let length = 1;
  let tail = head;

  while (tail.next) {
    tail = tail.next;
    length++;
  }

  tail.next = head; // Make circular

  // Find new head
  k = k % length;
  let stepsToNewHead = length - k;

  let newTail = head;
  for (let i = 1; i < stepsToNewHead; i++) {
    newTail = newTail.next;
  }

  const newHead = newTail.next;
  newTail.next = null;

  return newHead;
}

/**
 * Problem 10: Add Two Numbers (represented as linked lists)
 * Time: O(max(n, m)), Space: O(max(n, m))
 */
function addTwoNumbers(l1, l2) {
  const dummy = new Node(0);
  let current = dummy;
  let carry = 0;

  while (l1 || l2 || carry) {
    const val1 = l1 ? l1.data : 0;
    const val2 = l2 ? l2.data : 0;
    const sum = val1 + val2 + carry;

    carry = Math.floor(sum / 10);
    current.next = new Node(sum % 10);
    current = current.next;

    if (l1) l1 = l1.next;
    if (l2) l2 = l2.next;
  }

  return dummy.next;
}

// ============================================
// 4. MEMORY MANAGEMENT & BEST PRACTICES
// ============================================

/**
 * Best Practices for JavaScript Linked Lists
 */

// 1. Always use dummy/sentinel nodes for easier deletion
function deleteNodeWithDummy(head, target) {
  const dummy = new Node(0);
  dummy.next = head;
  let current = dummy;

  while (current.next) {
    if (current.next.data === target) {
      current.next = current.next.next;
      break;
    }
    current = current.next;
  }

  return dummy.next;
}

// 2. Null checks are crucial
function safeTraversal(head) {
  if (!head) {
    console.log("Empty list");
    return;
  }

  let current = head;
  while (current) {
    console.log(current.data);
    current = current.next;
  }
}

// 3. Use two-pointer technique for efficient solutions
function findPairWithSum(head, target) {
  const seen = new Set();
  let current = head;

  while (current) {
    const complement = target - current.data;
    if (seen.has(complement)) {
      return [complement, current.data];
    }
    seen.add(current.data);
    current = current.next;
  }

  return null;
}

// 4. Method chaining for better API
class ChainableList {
  constructor() {
    this.head = null;
  }

  append(data) {
    // ... implementation
    return this; // Return this for chaining
  }

  prepend(data) {
    // ... implementation
    return this;
  }

  // Usage: list.append(1).append(2).prepend(0)
}

// 5. Iterator implementation for for...of loops
class IterableLinkedList {
  constructor() {
    this.head = null;
  }

  *[Symbol.iterator]() {
    let current = this.head;
    while (current) {
      yield current.data;
      current = current.next;
    }
  }

  // Usage: for (const value of list) { console.log(value); }
}

// ============================================
// 5. PERFORMANCE COMPARISONS
// ============================================

/**
 * Array vs Linked List Performance Test
 */
function performanceComparison() {
  const size = 10000;

  // Array operations
  console.log("Array Operations:");
  const arr = [];

  console.time("Array: Insert at beginning");
  for (let i = 0; i < size; i++) {
    arr.unshift(i); // O(n) each time
  }
  console.timeEnd("Array: Insert at beginning");

  console.time("Array: Insert at end");
  for (let i = 0; i < size; i++) {
    arr.push(i); // O(1) amortized
  }
  console.timeEnd("Array: Insert at end");

  console.time("Array: Access by index");
  let sum = 0;
  for (let i = 0; i < arr.length; i++) {
    sum += arr[i]; // O(1) each time
  }
  console.timeEnd("Array: Access by index");

  // Linked List operations
  console.log("\nLinked List Operations:");
  const list = new SinglyLinkedList();

  console.time("LL: Insert at beginning");
  for (let i = 0; i < size; i++) {
    list.prepend(i); // O(1) each time
  }
  console.timeEnd("LL: Insert at beginning");

  console.time("LL: Insert at end");
  for (let i = 0; i < size; i++) {
    list.append(i); // O(1) with tail pointer
  }
  console.timeEnd("LL: Insert at end");

  console.time("LL: Traverse");
  sum = 0;
  list.forEach((data) => (sum += data)); // O(n)
  console.timeEnd("LL: Traverse");
}

// ============================================
// 6. PRACTICAL USE CASES
// ============================================

/**
 * Use Case 1: Browser History Implementation
 */
class BrowserHistory {
  constructor(homepage) {
    this.current = new Node(homepage);
    this.current.prev = null;
    this.current.next = null;
  }

  visit(url) {
    const newNode = new Node(url);
    newNode.prev = this.current;
    this.current.next = newNode;
    this.current = newNode;
  }

  back(steps) {
    while (steps > 0 && this.current.prev) {
      this.current = this.current.prev;
      steps--;
    }
    return this.current.data;
  }

  forward(steps) {
    while (steps > 0 && this.current.next) {
      this.current = this.current.next;
      steps--;
    }
    return this.current.data;
  }
}

/**
 * Use Case 2: LRU Cache Implementation
 */
class LRUCache {
  constructor(capacity) {
    this.capacity = capacity;
    this.cache = new Map();
    this.head = new DoublyNode(0);
    this.tail = new DoublyNode(0);
    this.head.next = this.tail;
    this.tail.prev = this.head;
  }

  get(key) {
    if (!this.cache.has(key)) return -1;

    const node = this.cache.get(key);
    this.moveToHead(node);
    return node.data;
  }

  put(key, value) {
    if (this.cache.has(key)) {
      const node = this.cache.get(key);
      node.data = value;
      this.moveToHead(node);
    } else {
      const newNode = new DoublyNode(value);
      this.cache.set(key, newNode);
      this.addToHead(newNode);

      if (this.cache.size > this.capacity) {
        const removed = this.removeTail();
        this.cache.delete(removed.key);
      }
    }
  }

  moveToHead(node) {
    this.removeNode(node);
    this.addToHead(node);
  }

  removeNode(node) {
    node.prev.next = node.next;
    node.next.prev = node.prev;
  }

  addToHead(node) {
    node.next = this.head.next;
    node.prev = this.head;
    this.head.next.prev = node;
    this.head.next = node;
  }

  removeTail() {
    const removed = this.tail.prev;
    this.removeNode(removed);
    return removed;
  }
}

/**
 * Use Case 3: Music Playlist (Circular List)
 */
class MusicPlaylist {
  constructor() {
    this.head = null;
    this.current = null;
    this.size = 0;
  }

  addSong(name) {
    const newNode = new Node(name);

    if (!this.head) {
      this.head = newNode;
      this.current = newNode;
      newNode.next = newNode;
    } else {
      let temp = this.head;
      while (temp.next !== this.head) {
        temp = temp.next;
      }
      temp.next = newNode;
      newNode.next = this.head;
    }

    this.size++;
  }

  next() {
    if (!this.current) return null;
    this.current = this.current.next;
    return this.current.data;
  }

  previous() {
    if (!this.current) return null;
    let temp = this.current;
    while (temp.next !== this.current) {
      temp = temp.next;
    }
    this.current = temp;
    return this.current.data;
  }

  getCurrentSong() {
    return this.current ? this.current.data : null;
  }
}

// ============================================
// 7. COMMON PITFALLS & DEBUGGING TIPS
// ============================================

/**
 * Pitfall 1: Losing reference to head
 */
function wrongWay(head) {
  // WRONG: head is just a local variable
  head = head.next; // This doesn't affect the original list!
  return head;
}

function correctWay(head) {
  // CORRECT: Return new head or modify through dummy node
  const dummy = new Node(0);
  dummy.next = head;
  // ... operations
  return dummy.next;
}

/**
 * Pitfall 2: Not handling null/undefined
 */
function buggyCode(head) {
  // BUGGY: Will crash if head is null
  return head.next.data;
}

function safeCode(head) {
  // SAFE: Always check for null
  if (!head || !head.next) return null;
  return head.next.data;
}

/**
 * Pitfall 3: Infinite loops in circular lists
 */
function detectAndBreakCycle(head) {
  const visited = new Set();
  let current = head;

  while (current) {
    if (visited.has(current)) {
      console.log("Cycle detected!");
      break;
    }
    visited.add(current);
    current = current.next;
  }
}

// ============================================
// DEMONSTRATIONS
// ============================================

console.log("=".repeat(60));
console.log("DOUBLY LINKED LIST DEMO");
console.log("=".repeat(60));

const dList = new DoublyLinkedList();
dList.append(10).append(20).append(30);
console.log("Forward:", dList.toArrayForward());
console.log("Backward:", dList.toArrayBackward());
dList.print();

console.log("\n" + "=".repeat(60));
console.log("CIRCULAR LINKED LIST DEMO");
console.log("=".repeat(60));

const cList = new CircularLinkedList();
cList.append(1).append(2).append(3);
cList.print();

console.log("\n" + "=".repeat(60));
console.log("INTERVIEW PROBLEMS DEMO");
console.log("=".repeat(60));

// Create test list: 1 -> 2 -> 3 -> 4 -> 5
const testHead = new Node(1);
testHead.next = new Node(2);
testHead.next.next = new Node(3);
testHead.next.next.next = new Node(4);
testHead.next.next.next.next = new Node(5);

console.log("Original list: 1 -> 2 -> 3 -> 4 -> 5");
console.log("Middle element:", findMiddle(testHead).data);
console.log("Has cycle:", hasCycle(testHead));

// Palindrome test
const palindrome = new Node(1);
palindrome.next = new Node(2);
palindrome.next.next = new Node(2);
palindrome.next.next.next = new Node(1);
console.log("Is [1,2,2,1] palindrome:", isPalindrome(palindrome));

console.log("\n" + "=".repeat(60));
console.log("PRACTICAL USE CASES");
console.log("=".repeat(60));

// Browser History
const browser = new BrowserHistory("google.com");
browser.visit("youtube.com");
browser.visit("facebook.com");
console.log("Current:", "facebook.com");
console.log("Back 1:", browser.back(1)); // youtube.com
console.log("Forward 1:", browser.forward(1)); // facebook.com

// Music Playlist
const playlist = new MusicPlaylist();
playlist.addSong("Song 1");
playlist.addSong("Song 2");
playlist.addSong("Song 3");
console.log("\nPlaylist current:", playlist.getCurrentSong());
console.log("Next:", playlist.next());
console.log("Next:", playlist.next());
console.log("Next:", playlist.next()); // Back to Song 1

console.log("\n" + "=".repeat(60));
console.log("WHEN TO USE LINKED LISTS IN JAVASCRIPT");
console.log("=".repeat(60));

console.log(`
✅ USE Linked Lists when:
  - Frequent insertions/deletions at beginning
  - Implementing queues, stacks, LRU cache
  - Building complex data structures (graphs, trees)
  - Memory fragmentation is an issue
  - Don't need random access

❌ DON'T USE Linked Lists when:
  - Need fast random access (use Arrays)
  - Memory overhead is a concern
  - Simple sequential access (Arrays are faster in JS)
  - Cache locality matters (Arrays are cache-friendly)

💡 In JavaScript, Arrays are highly optimized and often
   better than Linked Lists for most use cases. Use Linked
   Lists when you have a specific algorithmic need.
`);

console.log("=".repeat(60));
console.log("TUTORIAL COMPLETE!");
console.log("=".repeat(60));
