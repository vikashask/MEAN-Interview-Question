# ES6 (ECMAScript 2015) Features and Concepts

## Core Features

### 1. let and const

```javascript
// Block scoping with let
{
  let x = 1;
  // x is only accessible here
}

// Constants
const PI = 3.14159;
const CONFIG = {
  api: "https://api.example.com",
};

// Object freezing for true immutability
Object.freeze(CONFIG);
```

### 2. Arrow Functions

```javascript
// Basic syntax
const add = (a, b) => a + b;

// With block body
const multiply = (a, b) => {
  const result = a * b;
  return result;
};

// Lexical this
class Timer {
  constructor() {
    this.seconds = 0;
    setInterval(() => this.seconds++, 1000);
  }
}
```

### 3. Template Literals

```javascript
const name = "John";
const greeting = `Hello ${name}!`;

// Multi-line strings
const html = `
    <div>
        <h1>${title}</h1>
        <p>${content}</p>
    </div>
`;

// Tagged templates
function highlight(strings, ...values) {
  return strings.reduce(
    (acc, str, i) => acc + str + (values[i] ? `<span>${values[i]}</span>` : ""),
    ""
  );
}
```

## Classes and Modules

### 1. Class Syntax

```javascript
class Person {
  constructor(name) {
    this.name = name;
  }

  sayHello() {
    return `Hello, I'm ${this.name}`;
  }

  static create(name) {
    return new Person(name);
  }
}

// Inheritance
class Employee extends Person {
  constructor(name, role) {
    super(name);
    this.role = role;
  }
}
```

### 2. Modules

```javascript
// Named exports
export const PI = 3.14159;
export function square(x) {
  return x * x;
}

// Default export
export default class Calculator {
  // ...
}

// Importing
import Calculator, { PI, square } from "./math";
import * as MathUtils from "./math";
```

## Enhanced Object Features

### 1. Object Property Shorthand

```javascript
const name = "John";
const age = 30;

const person = {
  name,
  age,
  sayHi() {
    return `Hi, I'm ${this.name}`;
  },
};
```

### 2. Computed Property Names

```javascript
const prefix = "user";
const userConfig = {
  [`${prefix}_name`]: "John",
  [`${prefix}_age`]: 30,
};
```

### 3. Object Destructuring

```javascript
const { name, age } = person;

// With default values
const { title = "Untitled", body = "" } = post;

// Nested destructuring
const {
  address: { city, country },
} = user;
```

## Arrays and Iterables

### 1. Array Destructuring

```javascript
const [first, second, ...rest] = numbers;

// Skipping elements
const [, , third] = numbers;

// Swap variables
let a = 1,
  b = 2;
[a, b] = [b, a];
```

### 2. Spread Operator

```javascript
// Array spread
const combined = [...arr1, ...arr2];
const copy = [...original];

// Object spread
const enhanced = {
  ...baseObject,
  newProp: "value",
};
```

### 3. Iterators and for...of

```javascript
// Custom iterator
const range = {
  from: 1,
  to: 5,
  [Symbol.iterator]() {
    return {
      current: this.from,
      last: this.to,
      next() {
        if (this.current <= this.last) {
          return { done: false, value: this.current++ };
        }
        return { done: true };
      },
    };
  },
};

for (const num of range) {
  console.log(num);
}
```

## Promises and Async

### 1. Promises

```javascript
function fetchUser(id) {
  return new Promise((resolve, reject) => {
    // Async operation
    if (user) {
      resolve(user);
    } else {
      reject(new Error("User not found"));
    }
  });
}

// Promise chaining
fetchUser(1)
  .then((user) => fetchOrders(user))
  .then((orders) => processOrders(orders))
  .catch((error) => console.error(error));
```

### 2. Async/Await

```javascript
async function getUserData() {
  try {
    const user = await fetchUser(1);
    const orders = await fetchOrders(user);
    return processOrders(orders);
  } catch (error) {
    console.error(error);
  }
}
```

## Other Features

### 1. Default Parameters

```javascript
function greet(name = "Guest", greeting = "Hello") {
  return `${greeting}, ${name}!`;
}
```

### 2. Rest Parameters

```javascript
function sum(...numbers) {
  return numbers.reduce((total, n) => total + n, 0);
}
```

### 3. Map and Set

```javascript
// Map
const userRoles = new Map();
userRoles.set(user1, "admin");
userRoles.set(user2, "user");

// Set
const uniqueNumbers = new Set([1, 2, 2, 3, 3]);
```

### 4. Symbols

```javascript
const MY_KEY = Symbol("my_key");
const obj = {
  [MY_KEY]: "value",
};

// Well-known symbols
class CustomIterator {
  [Symbol.iterator]() {
    // ...
  }
}
```

## Best Practices

1. Use const by default, let when needed
2. Prefer arrow functions for callbacks
3. Use template literals for string interpolation
4. Use destructuring for cleaner code
5. Use async/await for promise-based operations
6. Use modules for better code organization
7. Use class syntax for object-oriented code
8. Use Map/Set when appropriate
9. Use spread operator for immutable operations
10. Use default parameters for better function definitions
