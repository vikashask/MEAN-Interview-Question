/**
 * LINKED LISTS IN JAVASCRIPT - SIMPLE & EASY GUIDE 🚀
 * ===================================================
 * Learn linked lists step by step with simple examples
 */

// ============================================
// 1. WHAT IS A LINKED LIST? 🤔
// ============================================

/*
A Linked List is like a chain of boxes:
📦 -> 📦 -> 📦 -> null

Each box (Node) contains:
- Data (the value you want to store)
- Next (pointer to the next box)

Unlike arrays, linked list elements are not stored in consecutive memory locations.
*/

// ============================================
// 2. NODE - The Building Block 🧱
// ============================================

class Node {
  constructor(data) {
    this.data = data; // The value we store
    this.next = null; // Points to next node (starts as null)
  }
}

// Creating nodes is simple:
const firstNode = new Node("Apple");
const secondNode = new Node("Banana");
const thirdNode = new Node("Cherry");

// Link them together:
firstNode.next = secondNode;
secondNode.next = thirdNode;
// Result: Apple -> Banana -> Cherry -> null

console.log("🍎 Simple Linked List:");
console.log(
  firstNode.data,
  "->",
  firstNode.next.data,
  "->",
  firstNode.next.next.data
);

// ============================================
// 3. SIMPLE LINKED LIST CLASS 📝
// ============================================

class SimpleLinkedList {
  constructor() {
    this.head = null; // Points to the first node
    this.size = 0; // Keep track of how many nodes we have
  }

  // ============================================
  // BASIC OPERATIONS (The Essential 4) ⭐
  // ============================================

  /**
   * 1. ADD TO FRONT 🔝 (Most common & efficient)
   */
  addToFront(data) {
    const newNode = new Node(data);
    newNode.next = this.head; // Point new node to current first node
    this.head = newNode; // Make new node the first one
    this.size++;

    console.log(`✅ Added "${data}" to front`);
  }

  /**
   * 2. ADD TO END 🔚 (Simple version)
   */
  addToEnd(data) {
    const newNode = new Node(data);

    // If list is empty, new node becomes the first node
    if (!this.head) {
      this.head = newNode;
    } else {
      // Find the last node and link to it
      let current = this.head;
      while (current.next) {
        current = current.next;
      }
      current.next = newNode;
    }
    this.size++;

    console.log(`✅ Added "${data}" to end`);
  }

  /**
   * 3. FIND A VALUE 🔍
   */
  find(data) {
    let current = this.head;
    let position = 0;

    while (current) {
      if (current.data === data) {
        console.log(`🎯 Found "${data}" at position ${position}`);
        return position;
      }
      current = current.next;
      position++;
    }

    console.log(`❌ "${data}" not found`);
    return -1;
  }

  /**
   * 4. REMOVE A VALUE ✂️
   */
  remove(data) {
    if (!this.head) {
      console.log("❌ List is empty");
      return false;
    }

    // If removing first node
    if (this.head.data === data) {
      this.head = this.head.next;
      this.size--;
      console.log(`✅ Removed "${data}" from front`);
      return true;
    }

    // Find and remove from middle/end
    let current = this.head;
    while (current.next && current.next.data !== data) {
      current = current.next;
    }

    if (current.next) {
      current.next = current.next.next; // Skip the node to delete
      this.size--;
      console.log(`✅ Removed "${data}"`);
      return true;
    }

    console.log(`❌ "${data}" not found`);
    return false;
  }

  // ============================================
  // HELPER METHODS 🛠️
  // ============================================

  /**
   * DISPLAY THE LIST 👀 (Very useful for learning!)
   */
  display() {
    if (!this.head) {
      console.log("📝 List is empty");
      return;
    }

    let result = "";
    let current = this.head;

    while (current) {
      result += current.data;
      if (current.next) {
        result += " -> ";
      }
      current = current.next;
    }
    result += " -> null";

    console.log(`📝 List: ${result}`);
  }

  /**
   * GET SIZE 📊
   */
  getSize() {
    console.log(`📊 Size: ${this.size}`);
    return this.size;
  }
}

// ============================================
// 4. LET'S TEST IT! 🧪
// ============================================

console.log("\n" + "=".repeat(50));
console.log("🚀 TESTING OUR SIMPLE LINKED LIST");
console.log("=".repeat(50));

// Create a new list
const myList = new SimpleLinkedList();

// Test adding elements
myList.addToFront("World");
myList.addToFront("Hello");
myList.display(); // Hello -> World -> null

myList.addToEnd("!");
myList.addToEnd("JavaScript");
myList.display(); // Hello -> World -> ! -> JavaScript -> null

// Test finding elements
myList.find("World"); // Found
myList.find("Python"); // Not found

// Test removing elements
myList.remove("!");
myList.display(); // Hello -> World -> JavaScript -> null

myList.getSize(); // Size: 3

// ============================================
// 5. WHY USE LINKED LISTS? 🤷‍♂️
// ============================================

console.log("\n" + "=".repeat(50));
console.log("🎯 LINKED LISTS vs ARRAYS");
console.log("=".repeat(50));

/*
LINKED LISTS ARE GOOD FOR:
✅ Adding/removing at the beginning (O(1))
✅ Dynamic size (grows/shrinks as needed)
✅ No memory waste (only allocate what you need)

ARRAYS ARE GOOD FOR:
✅ Accessing elements by index (O(1))
✅ Better memory locality
✅ Less memory per element (no next pointer)

CHOOSE LINKED LISTS WHEN:
- You frequently add/remove at the beginning
- You don't know the size in advance
- You rarely need to access elements by index
*/

console.log("🎉 That's it! You now understand linked lists!");
console.log(
  "💡 Practice by adding more methods or trying different data types!"
);

// ============================================
// 6. BONUS: STEP-BY-STEP EXAMPLE 📚
// ============================================

console.log("\n" + "=".repeat(50));
console.log("📚 STEP-BY-STEP EXAMPLE");
console.log("=".repeat(50));

// Let's create a shopping list!
const shoppingList = new SimpleLinkedList();

console.log("🛒 Creating a shopping list...");

// Add items to our shopping list
shoppingList.addToFront("Milk"); // Milk -> null
shoppingList.display();

shoppingList.addToEnd("Bread"); // Milk -> Bread -> null
shoppingList.display();

shoppingList.addToFront("Eggs"); // Eggs -> Milk -> Bread -> null
shoppingList.display();

shoppingList.addToEnd("Butter"); // Eggs -> Milk -> Bread -> Butter -> null
shoppingList.display();

// Look for items
shoppingList.find("Milk"); // Found at position 1
shoppingList.find("Cheese"); // Not found

// Remove an item
shoppingList.remove("Bread"); // Eggs -> Milk -> Butter -> null
shoppingList.display();

// Check final size
shoppingList.getSize(); // Size: 3

console.log("\n🎊 Congratulations! You've mastered basic linked lists!");
