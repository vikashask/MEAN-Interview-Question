# JavaScript Interview Questions and Answers

## Difference Between Null & Undefined

- **Undefined** means a variable has been declared but has not yet been assigned a value.
- **Null** is an assignment value that represents a deliberate non-value or absence of any object value.

Key differences:

1. `undefined` is a type itself while `null` is an object
2. `undefined` is automatically assigned while `null` is manually assigned
3. `typeof undefined` returns "undefined" while `typeof null` returns "object"

Example:

```javascript
let variable; // undefined
console.log(variable); // undefined

let nullVar = null; // explicitly set to null
console.log(nullVar); // null
```

## Function Scope Vs. Block Scope

### Function Scope

- Created by variables declared with `var`
- Accessible anywhere within the function
- Hoisted to the top of their function scope

```javascript
function example() {
  var x = 1;
  if (true) {
    var x = 2; // same variable!
    console.log(x); // 2
  }
  console.log(x); // 2
}
```

### Block Scope

- Created by variables declared with `let` and `const`
- Only accessible within the block they are defined (between {})
- Not hoisted

```javascript
function example() {
  let x = 1;
  if (true) {
    let x = 2; // different variable
    console.log(x); // 2
  }
  console.log(x); // 1
}
```

## What is Automatic Semicolon Insertion (ASI)?

ASI is a JavaScript feature that automatically inserts semicolons after statements when they are missing. However, relying on ASI can lead to unexpected results.

Rules when ASI occurs:

1. When a line ends with an invalid statement
2. When there's a line break before `]`, `)`, or `}`
3. When the end of the program is reached
4. Before a `break`, `continue`, `return`, or `throw` statement

Example of potential ASI issues:

```javascript
// What you write:
return;
{
  key: "value";
}

// What JavaScript sees:
return;
{
  key: "value";
}
```

Best practice: Always explicitly add semicolons to avoid ASI-related bugs.

## Difference between Rest and Spread Operator

Both use the same `...` syntax but serve different purposes:

### Rest Operator

- Collects multiple elements into an array
- Used in function parameters or destructuring
- Always comes last in a declaration

```javascript
// In function parameters
function sum(...numbers) {
  return numbers.reduce((total, num) => total + num, 0);
}
console.log(sum(1, 2, 3, 4)); // 10

// In destructuring
const [first, second, ...rest] = [1, 2, 3, 4, 5];
console.log(rest); // [3, 4, 5]
```

### Spread Operator

- Expands elements from an array or object
- Used in function calls, array literals, or object literals
- Can be used anywhere in a declaration

```javascript
// In function calls
const numbers = [1, 2, 3];
console.log(Math.max(...numbers)); // 3

// In arrays
const arr1 = [1, 2];
const arr2 = [...arr1, 3, 4];
console.log(arr2); // [1, 2, 3, 4]

// In objects
const obj1 = { foo: "bar" };
const obj2 = { ...obj1, baz: "qux" };
console.log(obj2); // { foo: 'bar', baz: 'qux' }
```

## When do you get Infinity or -Infinity as output?

`Infinity` or `-Infinity` occurs in JavaScript in several scenarios:

1. Division by zero:

```javascript
console.log(1 / 0); // Infinity
console.log(-1 / 0); // -Infinity
```

2. Number exceeding maximum value:

```javascript
console.log(Number.MAX_VALUE * 2); // Infinity
```

3. Math operations:

```javascript
console.log(Math.pow(10, 1000)); // Infinity
console.log(-Math.pow(10, 1000)); // -Infinity
```

4. Logarithm of zero:

```javascript
console.log(Math.log(0)); // -Infinity
```

## When do you get NaN as output?

NaN (Not a Number) occurs in these common scenarios:

1. Invalid mathematical operations:

```javascript
console.log(0 / 0); // NaN
console.log(Math.sqrt(-1)); // NaN
```

2. Parsing invalid numbers:

```javascript
console.log(parseInt("hello")); // NaN
console.log(Number("123abc")); // NaN
```

3. Operations with NaN:

```javascript
console.log(NaN + 5); // NaN
console.log(NaN * 10); // NaN
```

Key points about NaN:

- `typeof NaN` returns "number"
- `NaN` is never equal to itself: `NaN === NaN` is `false`
- Use `isNaN()` or `Number.isNaN()` to check for NaN

## Explain must know points of arrow function

Arrow functions are a concise way to write function expressions in ES6+. Here are the key points:

1. Syntax:

```javascript
// Basic syntax
const simple = () => 42;
const withParam = (x) => x * 2;
const multiParams = (x, y) => x + y;
const multiLine = () => {
  const x = 1;
  return x + 2;
};
```

2. Lexical `this` binding:

```javascript
const obj = {
  name: "object",
  regularMethod: function () {
    setTimeout(function () {
      console.log(this.name); // undefined
    }, 100);
  },
  arrowMethod: function () {
    setTimeout(() => {
      console.log(this.name); // "object"
    }, 100);
  },
};
```

3. Limitations:

- Cannot be used as constructors
- Don't have their own `arguments` object
- Can't use `yield` within an arrow function
- Can't change `this` with call(), apply(), or bind()

4. Best use cases:

```javascript
// Array methods
const numbers = [1, 2, 3];
const doubled = numbers.map((x) => x * 2);

// Short callbacks
button.addEventListener("click", () => console.log("clicked"));

// Object methods with fixed this
const counter = {
  count: 0,
  increment: () => this.count++, // Note: this won't work as expected!
};
```

5. When to avoid:

```javascript
// Methods in objects (this will not be bound correctly)
const obj = {
    value: 42,
    getValue: () => this.value // 'this' refers to outer scope
};

// Prototype methods
class Person {
    constructor(name) {
        this.name = name;
    }
    // Don't use arrow functions for methods
    greet: () => console.log(`Hello, ${this.name}`) // wrong!
}
```

## How does a "closure" work in JavaScript?

A closure is a function that has access to variables in its outer (enclosing) lexical scope, even after the outer function has returned. It preserves the data from the outer scope.

Key aspects:

1. Data Privacy
2. State Preservation
3. Access to Outer Scope

```javascript
function createCounter() {
  let count = 0; // Private variable

  return {
    increment() {
      return ++count;
    },
    decrement() {
      return --count;
    },
    getCount() {
      return count;
    },
  };
}

const counter = createCounter();
console.log(counter.increment()); // 1
console.log(counter.increment()); // 2
console.log(counter.getCount()); // 2
console.log(counter.decrement()); // 1
```

Common use cases:

1. Module Pattern

```javascript
const module = (function () {
  let private = "private data";

  return {
    publicMethod() {
      return private;
    },
  };
})();
```

2. Partial Application

```javascript
function multiply(a) {
  return function (b) {
    return a * b;
  };
}
const multiplyByTwo = multiply(2);
console.log(multiplyByTwo(4)); // 8
```

## How can sum(5)(6) return 11?

This is an example of function currying using closures. Here's how to implement it:

```javascript
function sum(a) {
  return function (b) {
    return a + b;
  };
}

console.log(sum(5)(6)); // 11

// Advanced version with multiple calls
function advancedSum(a) {
  let currentSum = a;

  function f(b) {
    currentSum += b;
    return f;
  }

  f.toString = function () {
    return currentSum;
  };

  return f;
}

console.log(advancedSum(1)(2)(3)); // 6
```

## Iterables and Iterators

Iterables are objects that implement the iterable protocol, allowing them to be iterated over using for...of loops.

1. Built-in Iterables:

```javascript
// Arrays
const arr = [1, 2, 3];
for (const item of arr) {
  console.log(item);
}

// Strings
const str = "hello";
for (const char of str) {
  console.log(char);
}

// Maps
const map = new Map([
  ["a", 1],
  ["b", 2],
]);
for (const [key, value] of map) {
  console.log(key, value);
}
```

2. Creating Custom Iterables:

```javascript
const customIterable = {
  *[Symbol.iterator]() {
    yield 1;
    yield 2;
    yield 3;
  },
};

for (const value of customIterable) {
  console.log(value);
}

// Manual iterator usage
const iterator = customIterable[Symbol.iterator]();
console.log(iterator.next()); // { value: 1, done: false }
console.log(iterator.next()); // { value: 2, done: false }
console.log(iterator.next()); // { value: 3, done: false }
console.log(iterator.next()); // { value: undefined, done: true }
```

3. Fibonacci Sequence Iterator Example:

```javascript
const fibonacci = {
  *[Symbol.iterator]() {
    let prev = 0,
      curr = 1;

    while (true) {
      yield curr;
      [prev, curr] = [curr, prev + curr];
    }
  },
};

// Get first 6 Fibonacci numbers
let count = 0;
for (const num of fibonacci) {
  if (count++ === 6) break;
  console.log(num);
}
// Output: 1, 1, 2, 3, 5, 8
```

## Generators

Generators are special functions that can be paused and resumed, yielding multiple values over time.

```javascript
function* numberGenerator() {
  yield 1;
  yield 2;
  yield 3;
}

// Using the generator
const gen = numberGenerator();
console.log(gen.next().value); // 1
console.log(gen.next().value); // 2
console.log(gen.next().value); // 3
console.log(gen.next().done); // true

// Infinite sequence generator
function* infiniteSequence() {
  let i = 0;
  while (true) {
    yield i++;
  }
}

// Generator with input
function* twoWayGenerator() {
  const what = yield "Hello";
  yield "World " + what;
}

const twoWay = twoWayGenerator();
console.log(twoWay.next().value); // Hello
console.log(twoWay.next("Javascript!").value); // World Javascript!
```

Common Use Cases:

1. Implementing Iterables
2. Data Streaming
3. Async Flow Control
4. State Machines

## Memory Management & Garbage Collection

JavaScript automatically manages memory through garbage collection. Here are the key concepts:

1. Memory Lifecycle:

```javascript
// 1. Allocation
let obj = { name: "example" }; // Memory is allocated

// 2. Usage
console.log(obj.name); // Memory is used

// 3. Release
obj = null; // Memory can be garbage collected
```

2. Common Memory Leaks:

```javascript
// 1. Global Variables
function leak() {
  oops = { data: "I'm global!" }; // Missing 'let/const/var'
}

// 2. Forgotten Timers
function setTimer() {
  const heavyObject = {
    /* lots of data */
  };
  setInterval(() => {
    // heavyObject is retained even if not needed
    console.log(new Date());
  }, 1000);
}

// 3. Closures holding references
function closure() {
  const heavyData = {
    /* lots of data */
  };
  return function () {
    console.log(heavyData); // Keeps heavyData in memory
  };
}
```

3. Best Practices:

```javascript
// Clear event listeners
element.addEventListener("click", handler);
// Later:
element.removeEventListener("click", handler);

// Clear intervals
const intervalId = setInterval(fn, 1000);
// Later:
clearInterval(intervalId);

// Clear object references
let obj = { data: "large data" };
// When done:
obj = null;
```

## How do you handle errors in JavaScript code?

1. Try-Catch Blocks:

```javascript
try {
  // Code that might throw an error
  throw new Error("Something went wrong");
} catch (error) {
  console.error("Error:", error.message);
} finally {
  // Always executes
  console.log("Cleanup code");
}
```

2. Custom Error Types:

```javascript
class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = "ValidationError";
  }
}

try {
  throw new ValidationError("Invalid input");
} catch (e) {
  if (e instanceof ValidationError) {
    console.log("Handling validation error");
  } else {
    throw e; // Re-throw unknown errors
  }
}
```

3. Async Error Handling:

```javascript
// Using async/await
async function fetchData() {
  try {
    const response = await fetch("https://api.example.com/data");
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Fetch error:", error);
    throw error; // Re-throw or handle appropriately
  }
}

// Using promises
fetch("https://api.example.com/data")
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error("Error:", error))
  .finally(() => console.log("Done"));
```

4. Error Types:

```javascript
// Common built-in error types
try {
  // ReferenceError
  console.log(undefinedVariable);
} catch (e) {
  console.log(e instanceof ReferenceError); // true
}

try {
  // TypeError
  null.toString();
} catch (e) {
  console.log(e instanceof TypeError); // true
}

try {
  // SyntaxError (cannot be caught, occurs during parsing)
  eval('{"bad": json}');
} catch (e) {
  console.log(e instanceof SyntaxError); // true
}
```

## Explain array & traversal in array

Arrays in JavaScript are ordered collections that can hold mixed types of data. Here are the key concepts:

1. Array Traversal Methods:

```javascript
const arr = [1, 2, 3, 4, 5];

// 1. for...of loop (ES6+)
for (const item of arr) {
  console.log(item);
}

// 2. forEach method
arr.forEach((item, index) => {
  console.log(`Item ${item} at index ${index}`);
});

// 3. Traditional for loop
for (let i = 0; i < arr.length; i++) {
  console.log(arr[i]);
}

// 4. for...in loop (not recommended for arrays)
for (const index in arr) {
  console.log(arr[index]);
}
```

2. Array Iteration Methods:

```javascript
const numbers = [1, 2, 3, 4, 5];

// map: Transform elements
const doubled = numbers.map((x) => x * 2);

// filter: Select elements
const evenNumbers = numbers.filter((x) => x % 2 === 0);

// reduce: Accumulate values
const sum = numbers.reduce((acc, curr) => acc + curr, 0);

// some: Check if any element matches
const hasEven = numbers.some((x) => x % 2 === 0);

// every: Check if all elements match
const allPositive = numbers.every((x) => x > 0);
```

## Add, Remove, Insert, Replace Elements in Array

1. Adding Elements:

```javascript
const arr = [1, 2, 3];

// Add to end
arr.push(4); // [1, 2, 3, 4]

// Add to beginning
arr.unshift(0); // [0, 1, 2, 3, 4]

// Add using spread
const newArr = [...arr, 5]; // [0, 1, 2, 3, 4, 5]
```

2. Removing Elements:

```javascript
// Remove from end
arr.pop(); // Returns last element

// Remove from beginning
arr.shift(); // Returns first element

// Remove specific elements
arr.splice(2, 1); // Removes 1 element at index 2
```

3. Inserting Elements:

```javascript
const arr = [1, 2, 4, 5];

// Insert at specific position
arr.splice(2, 0, 3); // [1, 2, 3, 4, 5]

// Replace elements
arr.splice(1, 2, "a", "b"); // [1, 'a', 'b', 4, 5]
```

## How do you perform search in an array?

1. Basic Search Methods:

```javascript
const arr = [1, 2, 3, 4, 5, 2];

// indexOf: Find first occurrence
console.log(arr.indexOf(2)); // 1

// lastIndexOf: Find last occurrence
console.log(arr.lastIndexOf(2)); // 5

// includes: Check existence
console.log(arr.includes(3)); // true
```

2. Advanced Search Methods:

```javascript
const users = [
  { id: 1, name: "John" },
  { id: 2, name: "Jane" },
  { id: 3, name: "Bob" },
];

// find: Return first matching element
const user = users.find((u) => u.id === 2);
console.log(user); // { id: 2, name: 'Jane' }

// findIndex: Return index of first match
const index = users.findIndex((u) => u.name === "Bob");
console.log(index); // 2

// filter: Return all matches
const results = users.filter((u) => u.name.startsWith("J"));
console.log(results); // [{ id: 1, name: 'John' }, { id: 2, name: 'Jane' }]
```

## What is the use of map() method?

The map() method creates a new array with the results of calling a function for every array element.

1. Basic Usage:

```javascript
const numbers = [1, 2, 3, 4];
const squared = numbers.map((x) => x * x);
console.log(squared); // [1, 4, 9, 16]
```

2. Working with Objects:

```javascript
const users = [
  { name: "John", age: 30 },
  { name: "Jane", age: 25 },
];

const names = users.map((user) => user.name);
console.log(names); // ['John', 'Jane']

const formatted = users.map((user) => ({
  displayName: user.name.toUpperCase(),
  isAdult: user.age >= 18,
}));
```

3. Map with Index:

```javascript
const letters = ["a", "b", "c"];
const indexed = letters.map((letter, index) => ({
  letter,
  position: index + 1,
}));
// [{letter: 'a', position: 1}, ...]
```

## How to flatten 2D array?

There are several ways to flatten arrays in JavaScript:

1. Using flat() method (ES2019+):

```javascript
const array2D = [
  [1, 2],
  [3, 4],
  [5, 6],
];
const flattened = array2D.flat();
console.log(flattened); // [1, 2, 3, 4, 5, 6]

// Works with deeper nesting too
const deepArray = [
  [1, [2, 3]],
  [4, [5, 6]],
];
const flattenedDeep = deepArray.flat(2);
console.log(flattenedDeep); // [1, 2, 3, 4, 5, 6]
```

2. Using reduce():

```javascript
const array2D = [
  [1, 2],
  [3, 4],
  [5, 6],
];
const flattened = array2D.reduce((acc, curr) => acc.concat(curr), []);
console.log(flattened); // [1, 2, 3, 4, 5, 6]
```

3. Using spread operator:

```javascript
const array2D = [
  [1, 2],
  [3, 4],
  [5, 6],
];
const flattened = [].concat(...array2D);
console.log(flattened); // [1, 2, 3, 4, 5, 6]
```

## How can you sort an array?

Arrays in JavaScript can be sorted using various methods:

1. Basic Sorting:

```javascript
// Default sort (converts to strings)
const fruits = ["banana", "apple", "orange"];
fruits.sort();
console.log(fruits); // ['apple', 'banana', 'orange']

// Numeric sort
const numbers = [10, 2, 5, 1, 9];
numbers.sort((a, b) => a - b); // ascending
console.log(numbers); // [1, 2, 5, 9, 10]

numbers.sort((a, b) => b - a); // descending
console.log(numbers); // [10, 9, 5, 2, 1]
```

2. Complex Object Sorting:

```javascript
const users = [
  { name: "John", age: 30 },
  { name: "Alice", age: 25 },
  { name: "Bob", age: 35 },
];

// Sort by age
users.sort((a, b) => a.age - b.age);

// Sort by name
users.sort((a, b) => a.name.localeCompare(b.name));

// Sort by multiple criteria
users.sort((a, b) => {
  if (a.age === b.age) {
    return a.name.localeCompare(b.name);
  }
  return a.age - b.age;
});
```

## Explain Array Destructuring

Array destructuring allows you to unpack values from arrays into distinct variables:

1. Basic Destructuring:

```javascript
const numbers = [1, 2, 3];
const [a, b, c] = numbers;
console.log(a, b, c); // 1 2 3

// Skip elements
const [first, , third] = numbers;
console.log(first, third); // 1 3
```

2. Default Values:

```javascript
const [x = 1, y = 2, z = 3] = [10, 20];
console.log(x, y, z); // 10 20 3
```

3. Rest Pattern:

```javascript
const [head, ...tail] = [1, 2, 3, 4];
console.log(head); // 1
console.log(tail); // [2, 3, 4]
```

4. Swapping Variables:

```javascript
let a = 1,
  b = 2;
[a, b] = [b, a];
console.log(a, b); // 2 1
```

## String Basics - [UTF-16] - \u - Unicode

Strings in JavaScript are UTF-16 encoded:

1. Unicode Characters:

```javascript
// Unicode escape sequences
console.log("\u00A9"); // ©
console.log("\u{1F600}"); // 😀 (ES6 extended unicode)

// String length with unicode
const emoji = "😀";
console.log(emoji.length); // 2 (because it's UTF-16)
```

2. String Literal Types:

```javascript
// Regular string literal
const simple = "Hello";

// Template literal
const template = `Hello ${name}`;

// Tagged template literal
function tag(strings, ...values) {
  return strings[0] + values[0].toUpperCase();
}
const tagged = tag`Hello ${name}`;
```

## ES6 Template Literal (String)

Template literals provide enhanced string functionality:

1. Basic Usage:

```javascript
const name = "World";
const greeting = `Hello ${name}!`;
console.log(greeting); // Hello World!

// Multi-line strings
const multiLine = `
    Line 1
    Line 2
    Line 3
`;
```

2. Expression Interpolation:

```javascript
const a = 10,
  b = 20;
console.log(`Sum: ${a + b}`); // Sum: 30

const obj = { name: "John" };
console.log(`Name: ${obj.name}`); // Name: John
```

3. Tagged Templates:

```javascript
function highlight(strings, ...values) {
  let result = "";
  strings.forEach((str, i) => {
    result += str;
    if (i < values.length) {
      result += `<em>${values[i]}</em>`;
    }
  });
  return result;
}

const name = "World";
const highlighted = highlight`Hello ${name}!`;
// Result: "Hello <em>World</em>!"
```

## ".length" Property and Search Methods

1. String Length:

```javascript
const str = "Hello World";
console.log(str.length); // 11

// Note with Unicode:
const emoji = "👋";
console.log(emoji.length); // 2 (UTF-16 surrogate pair)
```

2. Search Methods:

```javascript
const text = "Hello World";

// indexOf
console.log(text.indexOf("o")); // 4
console.log(text.lastIndexOf("o")); // 7

// includes
console.log(text.includes("World")); // true

// startsWith/endsWith
console.log(text.startsWith("Hello")); // true
console.log(text.endsWith("World")); // true

// search with regex
console.log(text.search(/World/)); // 6
```

## Extraction Methods

```javascript
const str = "Hello World";

// slice(start, end)
console.log(str.slice(0, 5)); // "Hello"
console.log(str.slice(-5)); // "World"

// substring(start, end)
console.log(str.substring(6)); // "World"

// substr(start, length)
console.log(str.substr(0, 5)); // "Hello"

// Split string into array
console.log(str.split(" ")); // ["Hello", "World"]
console.log(str.split("")); // ["H", "e", "l", "l", "o", " ", "W", "o", "r", "l", "d"]

// charAt
console.log(str.charAt(0)); // "H"
```

## Case Conversion & replace() Method

1. Case Conversion:

```javascript
const str = "Hello World";

console.log(str.toLowerCase()); // "hello world"
console.log(str.toUpperCase()); // "HELLO WORLD"

// Locale-specific conversions
console.log(str.toLocaleLowerCase()); // "hello world"
console.log(str.toLocaleUpperCase()); // "HELLO WORLD"
```

2. Replace Methods:

```javascript
const str = "Hello World, Hello JavaScript";

// replace (first occurrence)
console.log(str.replace("Hello", "Hi"));
// "Hi World, Hello JavaScript"

// replaceAll (all occurrences - ES2021)
console.log(str.replaceAll("Hello", "Hi"));
// "Hi World, Hi JavaScript"

// Using regex
console.log(str.replace(/Hello/g, "Hi"));
// "Hi World, Hi JavaScript"

// Replace with function
console.log(str.replace(/Hello/g, (match) => match.toUpperCase()));
// "HELLO World, HELLO JavaScript"
```

## Date & Time Basics

1. Creating Dates:

```javascript
// Current date and time
const now = new Date();

// Specific date and time
const date1 = new Date("2025-07-11");
const date2 = new Date(2025, 6, 11); // Month is 0-based
const date3 = new Date(1689062400000); // Unix timestamp
```

2. Date Components:

```javascript
const date = new Date();

console.log(date.getFullYear()); // e.g., 2025
console.log(date.getMonth()); // 0-11
console.log(date.getDate()); // 1-31
console.log(date.getDay()); // 0-6 (Sunday-Saturday)
console.log(date.getHours()); // 0-23
console.log(date.getMinutes()); // 0-59
console.log(date.getSeconds()); // 0-59
console.log(date.getMilliseconds()); // 0-999
```

## Date Methods

1. Date Formatting:

```javascript
const date = new Date("2025-07-11");

// Built-in formats
console.log(date.toDateString()); // "Fri Jul 11 2025"
console.log(date.toISOString()); // "2025-07-11T00:00:00.000Z"
console.log(date.toLocaleDateString()); // Locale-specific format
console.log(date.toUTCString()); // "Fri, 11 Jul 2025 00:00:00 GMT"
```

2. Date Operations:

```javascript
const date = new Date("2025-07-11");

// Add/subtract days
date.setDate(date.getDate() + 5); // Add 5 days
date.setDate(date.getDate() - 2); // Subtract 2 days

// Add/subtract months
date.setMonth(date.getMonth() + 1); // Add 1 month

// Add/subtract years
date.setFullYear(date.getFullYear() + 1); // Add 1 year
```

## Time Methods

1. Time Components:

```javascript
const now = new Date();

// Get time components
console.log(now.getHours()); // 0-23
console.log(now.getMinutes()); // 0-59
console.log(now.getSeconds()); // 0-59
console.log(now.getMilliseconds()); // 0-999

// Get timestamp (milliseconds since Unix epoch)
console.log(now.getTime());
console.log(Date.now()); // Static method
```

2. Time Operations:

```javascript
const date = new Date();

// Add hours
date.setHours(date.getHours() + 2);

// Add minutes
date.setMinutes(date.getMinutes() + 30);

// Time differences
const date1 = new Date("2025-07-11");
const date2 = new Date("2025-07-12");
const diffInMs = date2 - date1;
const diffInDays = diffInMs / (1000 * 60 * 60 * 24);
console.log(diffInDays); // 1
```

3. Performance Timing:

```javascript
// High-resolution timing
const start = performance.now();
// ... some operations ...
const end = performance.now();
console.log(`Operation took ${end - start} milliseconds`);
```

## What is object literal?

An object literal is a way to create objects in JavaScript using curly braces notation.

1. Basic Object Literal:

```javascript
const person = {
  name: "John",
  age: 30,
  greet() {
    return `Hello, I'm ${this.name}`;
  },
};
```

2. Enhanced Object Literals (ES6+):

```javascript
// Property shorthand
const name = "John";
const age = 30;
const person = { name, age };

// Computed property names
const propName = "age";
const person2 = {
  name: "John",
  [propName]: 30,
};

// Method shorthand
const calculator = {
  add(a, b) {
    return a + b;
  },
  subtract(a, b) {
    return a - b;
  },
};
```

## What is "this" object?

"this" is a special keyword that references the current execution context.

1. Global Context:

```javascript
console.log(this === window); // true (in browser)
```

2. Function Context:

```javascript
function regularFunction() {
  console.log(this); // window (in non-strict mode)
}

function strictFunction() {
  "use strict";
  console.log(this); // undefined
}
```

3. Method Context:

```javascript
const obj = {
  name: "Object",
  method() {
    console.log(this.name); // 'Object'
  },
};
```

4. Constructor Context:

```javascript
function Person(name) {
  this.name = name;
  // 'this' refers to the new instance
}
const person = new Person("John");
```

## What is the purpose of call(), apply() and bind()?

These methods allow you to explicitly set the `this` context of a function.

1. call():

```javascript
function greet() {
  return `Hello, I'm ${this.name}`;
}

const person = { name: "John" };
console.log(greet.call(person)); // "Hello, I'm John"

// With parameters
function introduce(age, profession) {
  return `I'm ${this.name}, ${age} years old, ${profession}`;
}
console.log(introduce.call(person, 30, "developer"));
```

2. apply():

```javascript
// Same as call() but takes array of arguments
console.log(introduce.apply(person, [30, "developer"]));

// Useful for math operations
const numbers = [5, 6, 2, 3, 7];
console.log(Math.max.apply(null, numbers));
```

3. bind():

```javascript
// Creates a new function with fixed 'this'
const boundGreet = greet.bind(person);
console.log(boundGreet()); // "Hello, I'm John"

// Partial application
const greet30YearOld = introduce.bind(person, 30);
console.log(greet30YearOld("developer"));
```

## Class, Class expression & Static members

1. Class Declaration:

```javascript
class Person {
  constructor(name) {
    this.name = name;
  }

  greet() {
    return `Hello, I'm ${this.name}`;
  }

  static create(name) {
    return new Person(name);
  }
}
```

2. Class Expression:

```javascript
// Anonymous
const Person = class {
  constructor(name) {
    this.name = name;
  }
};

// Named
const Person = class PersonClass {
  constructor(name) {
    this.name = name;
  }
};
```

3. Static Members:

```javascript
class MathOperations {
  static PI = 3.14159;

  static sum(x, y) {
    return x + y;
  }

  static {
    // Static initialization block (ES2022)
    this.SQRT2 = Math.sqrt(2);
  }
}
```

## Inheritance, Subclassing and Extending built-in class

1. Basic Inheritance:

```javascript
class Animal {
  constructor(name) {
    this.name = name;
  }

  speak() {
    return `${this.name} makes a sound`;
  }
}

class Dog extends Animal {
  speak() {
    return `${this.name} barks`;
  }
}
```

2. Extending Built-in Classes:

```javascript
class MyArray extends Array {
  first() {
    return this[0];
  }

  last() {
    return this[this.length - 1];
  }
}

const arr = new MyArray(1, 2, 3);
console.log(arr.first()); // 1
```

## Class Accessors - getter & setter methods

```javascript
class Person {
  #age = 0; // Private field

  get age() {
    return this.#age;
  }

  set age(value) {
    if (value < 0) {
      throw new Error("Age cannot be negative");
    }
    this.#age = value;
  }
}

const person = new Person();
person.age = 25; // Uses setter
console.log(person.age); // Uses getter
```

## Map

Map is a collection of key-value pairs where both keys and values can be of any type.

1. Basic Usage:

```javascript
const map = new Map();

// Setting values
map.set("name", "John");
map.set(42, "answer");
map.set(person, "object key");

// Getting values
console.log(map.get("name")); // "John"

// Checking existence
console.log(map.has(42)); // true

// Size
console.log(map.size); // 3

// Deletion
map.delete(42);
```

2. Iteration:

```javascript
const map = new Map([
  ["name", "John"],
  ["age", 30],
]);

// Keys
for (const key of map.keys()) {
  console.log(key);
}

// Values
for (const value of map.values()) {
  console.log(value);
}

// Entries
for (const [key, value] of map.entries()) {
  console.log(`${key}: ${value}`);
}
```

## Set

Set is a collection of unique values of any type.

1. Basic Usage:

```javascript
const set = new Set();

// Adding values
set.add(1);
set.add("text");
set.add({ x: 10 });

// Size
console.log(set.size); // 3

// Checking existence
console.log(set.has(1)); // true

// Deletion
set.delete(1);
```

2. Common Use Cases:

```javascript
// Remove duplicates from array
const array = [1, 2, 2, 3, 3, 4];
const unique = [...new Set(array)];

// Set operations
const set1 = new Set([1, 2, 3]);
const set2 = new Set([2, 3, 4]);

// Union
const union = new Set([...set1, ...set2]);

// Intersection
const intersection = new Set([...set1].filter((x) => set2.has(x)));

// Difference
const difference = new Set([...set1].filter((x) => !set2.has(x)));
```

## WeakMap() and WeakSet()

1. WeakMap:

```javascript
const weakMap = new WeakMap();
let obj = { data: 42 };

// Only objects as keys
weakMap.set(obj, "associated data");

// Garbage collection friendly
obj = null; // object will be garbage collected
```

2. WeakSet:

```javascript
const weakSet = new WeakSet();
let obj = { data: 42 };

// Only objects as values
weakSet.add(obj);

// Garbage collection friendly
obj = null; // object will be garbage collected
```

Key differences from Map/Set:

- Only objects as keys (WeakMap) or values (WeakSet)
- No size property
- No iteration methods
- Garbage collection friendly
