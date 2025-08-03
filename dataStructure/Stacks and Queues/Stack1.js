
class Stack {
    constructor() {
        this.items = [];
    }

    // Add element to the top of the stack
    push(element) {
        this.items.push(element);
    }

    // Remove element from the top of the stack
    pop() {
        if (this.items.length === 0) {
            return "Underflow";
        }
        return this.items.pop();
    }

    // View the top element of the stack
    peek() {
        return this.items[this.items.length - 1];
    }

    // Check if the stack is empty
    isEmpty() {
        return this.items.length === 0;
    }

    // Get the size of the stack
    size() {
        return this.items.length;
    }

    // Print the stack elements
    printStack() {
        let str = "";
        for (let i = 0; i < this.items.length; i++) {
            str += this.items[i] + " ";
        }
        return str;
    }
}

// Example usage:
const stack = new Stack();
console.log("Is the stack empty?", stack.isEmpty()); // true

stack.push(10);
stack.push(20);
stack.push(30);

console.log("Stack elements:", stack.printStack()); // 10 20 30
console.log("Top element:", stack.peek()); // 30
console.log("Stack size:", stack.size()); // 3

console.log("Popped element:", stack.pop()); // 30
console.log("Stack elements after pop:", stack.printStack()); // 10 20
