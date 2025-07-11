# ES6 (ECMAScript 2015) Features

## Let and Const
- Block-scoped declarations
- `let` for variables that can be reassigned
- `const` for constants (cannot be reassigned)

```javascript
let x = 10;
const PI = 3.14;
```

## Arrow Functions
Shorter syntax for function expressions
```javascript
// Traditional function
function add(a, b) {
    return a + b;
}

// Arrow function
const add = (a, b) => a + b;
```

## Template Literals
String interpolation and multiline strings
```javascript
const name = 'John';
const greeting = `Hello ${name}!
This is a multiline
string.`;
```

## Destructuring
### Array Destructuring
```javascript
const numbers = [1, 2, 3];
const [first, second] = numbers;
```

### Object Destructuring
```javascript
const person = { name: 'John', age: 30 };
const { name, age } = person;
```

## Default Parameters
```javascript
function greet(name = 'Guest') {
    return `Hello ${name}!`;
}
```

## Rest and Spread Operators
### Rest Parameters
```javascript
function sum(...numbers) {
    return numbers.reduce((total, num) => total + num, 0);
}
```

### Spread Operator
```javascript
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5];
```

## Classes
```javascript
class Person {
    constructor(name) {
        this.name = name;
    }
    
    greet() {
        return `Hello, I'm ${this.name}`;
    }
}
```

## Modules
```javascript
// export
export const PI = 3.14;
export class Calculator { }

// import
import { PI, Calculator } from './math';
```

## Promises
```javascript
const promise = new Promise((resolve, reject) => {
    // async operation
    if (success) {
        resolve(result);
    } else {
        reject(error);
    }
});
```

## Map and Set
### Map
```javascript
const map = new Map();
map.set('key', 'value');
```

### Set
```javascript
const set = new Set([1, 2, 3]);
set.add(4);
```

## Enhanced Object Literals
```javascript
const name = 'John';
const person = {
    name,
    greet() {
        return `Hello ${this.name}`;
    }
};
```

## Array Methods
- `Array.from()`
- `Array.of()`
- `Array.prototype.find()`
- `Array.prototype.findIndex()`
- `Array.prototype.includes()`

## Symbol
```javascript
const sym = Symbol('description');
const obj = {
    [sym]: 'value'
};
```

## Iterators and Generators
```javascript
function* numberGenerator() {
    yield 1;
    yield 2;
    yield 3;
}
```

## Proxy and Reflect
```javascript
const handler = {
    get: (target, prop) => `Property ${prop}`
};
const proxy = new Proxy({}, handler);
```
