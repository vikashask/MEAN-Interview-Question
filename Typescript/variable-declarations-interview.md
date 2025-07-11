# TypeScript Variable Declarations Interview Questions

## 1. What are the differences between let, const, and var declarations in TypeScript?
**Answer:**
- `var`: Function-scoped or globally-scoped, can be redeclared and updated
- `let`: Block-scoped, can be updated but not redeclared in the same scope
- `const`: Block-scoped, cannot be updated or redeclared after initialization

Example:
```typescript
var x = 1; // Can be redeclared
var x = 2; // Valid

let y = 1;
let y = 2; // Error: Cannot redeclare block-scoped variable

const z = 1;
z = 2; // Error: Cannot assign to 'z' because it is a constant
```

## 2. What is Block-Scoping in TypeScript?
**Answer:**
Block-scoping means that variables declared with `let` and `const` are only accessible within the block they are declared in (including if statements, loops, etc.).

```typescript
function blockScopeExample() {
    if (true) {
        let x = 1;
        const y = 2;
        var z = 3;
    }
    console.log(z); // Works: z is function-scoped
    console.log(x); // Error: x is not defined
    console.log(y); // Error: y is not defined
}
```

## 3. What is Destructuring in TypeScript and how does it work?
**Answer:**
Destructuring allows you to extract values from arrays or properties from objects into distinct variables.

Array Destructuring:
```typescript
let input = [1, 2];
let [first, second] = input;
console.log(first);  // outputs 1
console.log(second); // outputs 2
```

Object Destructuring:
```typescript
let person = {
    name: "John",
    age: 30
};
let { name, age } = person;
console.log(name); // "John"
console.log(age);  // 30
```

## 4. What is the Rest operator in TypeScript and how is it used?
**Answer:**
The Rest operator (`...`) allows you to collect multiple elements into an array. It's commonly used in destructuring and function parameters.

```typescript
// In Object Destructuring
let object = {
    a: "foo",
    b: 12,
    c: "bar"
};
let { a, ...passthrough } = object;
console.log(passthrough); // { b: 12, c: "bar" }

// In Function Parameters
function sum(...numbers: number[]): number {
    return numbers.reduce((total, num) => total + num, 0);
}
console.log(sum(1, 2, 3, 4)); // 10
```

## 5. What is the Spread operator in TypeScript and how does it differ from the Rest operator?
**Answer:**
The Spread operator (`...`) is the opposite of the Rest operator. It spreads elements of an array or object into another array or object.

```typescript
// Array spreading
let first = [1, 2];
let second = [3, 4];
let combined = [0, ...first, ...second, 5];
console.log(combined); // [0, 1, 2, 3, 4, 5]

// Object spreading
let defaults = { width: 100, color: "white" };
let options = { ...defaults, height: 200 };
console.log(options); // { width: 100, color: "white", height: 200 }
```

## 6. How does shadowing work with variable declarations in TypeScript?
**Answer:**
Shadowing occurs when a variable declared in a certain scope has the same name as a variable in an outer scope. The inner variable "shadows" the outer one.

```typescript
function shadowingExample() {
    let x = 10;
    if (true) {
        let x = 20; // This x shadows the outer x
        console.log(x); // 20
    }
    console.log(x); // 10
}
```

## 7. What are the best practices for using variable declarations in TypeScript?
**Answer:**
1. Use `const` by default for variables that won't be reassigned
2. Use `let` when you need to reassign variables
3. Avoid using `var` due to its function-scoping and hoisting behavior
4. Use destructuring to make code more readable when working with objects and arrays
5. Use meaningful variable names that indicate their purpose
6. Declare variables in the smallest scope possible