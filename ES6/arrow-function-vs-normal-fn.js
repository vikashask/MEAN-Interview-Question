const Person = function (name, age) {
  this.age = age;
  this.name = name;
};

Person.prototype.introduction = function () {
  const getAge = () => {
    return this.age;
  };
  return `My name is ${this.name} and I am ${getAge()} years old!`;
};

Person.sayHi = function () {
  console.log(this);
};

Person.prototype.func2 = () => {
  console.log(this);
};

// class Person {
//   constructor(name, age) {
//     this.age = age;
//     this.name = name;
//   }

//   introduction() {
//     return `My name is ${this.name} and I am ${this.age} years old!`;
//   }

//   static sayHi() {
//     console.log("say hi");
//   }
// }

let john = new Person("John Smith", 18);
console.log(john);
john.func2();
Person.sayHi();

// const sayNameFunc = function() {
//     console.log(this.name);
//   }

//   const Library = {
//     introduction: function () {
//       console.log(`Hi I am john`);
//     },
//     createInstance: function (name) {
//       this._created = true;
//       this.name = name;
//       return this;
//     },
//     sayName: sayNameFunc
//   }
//   const john = Library.createInstance('John');

//   john.introduction();
//   john.sayName();

/*
  1. constructor function
  2. normal function
  */

//# Arrow Functions vs Regular Functions in JavaScript

// ## Syntax Differences

// ### Regular Function Declaration
// ```javascript
// function add(a, b) {
//     return a + b;
// }

// // Function expression
// const multiply = function(a, b) {
//     return a + b;
// };
// ```

// ### Arrow Function Declaration
// ```javascript
// const add = (a, b) => a + b;

// // With multiple lines
// const multiply = (a, b) => {
//     const result = a * b;
//     return result;
// };
// ```

// ## this Binding

// ### Regular Functions - Dynamic this
// ```javascript
// const obj = {
//     name: 'John',
//     greet: function() {
//         console.log('Hello, ' + this.name);
//     }
// };

// // Works as expected
// obj.greet(); // Output: "Hello, John"

// // this is lost in callback
// setTimeout(obj.greet, 1000); // Output: "Hello, undefined"
// ```

// ### Arrow Functions - Lexical this
// ```javascript
// const obj = {
//     name: 'John',
//     greet: () => {
//         console.log('Hello, ' + this.name);
//     },
//     // Common use in callbacks
//     delayedGreet: function() {
//         setTimeout(() => {
//             console.log('Hello, ' + this.name);
//         }, 1000);
//     }
// };
// ```

// ## Constructor Usage

// ### Regular Functions - Can be Constructors
// ```javascript
// function Person(name) {
//     this.name = name;
// }
// const john = new Person('John');
// ```

// ### Arrow Functions - Cannot be Constructors
// ```javascript
// const Person = (name) => {
//     this.name = name;
// };
// // Error: Person is not a constructor
// // const john = new Person('John'); // This will throw an error
// ```

// ## Arguments Object

// ### Regular Functions - Have arguments object
// ```javascript
// function sum() {
//     let total = 0;
//     for(let i = 0; i < arguments.length; i++) {
//         total += arguments[i];
//     }
//     return total;
// }
// console.log(sum(1, 2, 3)); // Output: 6
// ```

// ### Arrow Functions - No arguments object
// ```javascript
// const sum = () => {
//     // Error: arguments is not defined
//     // return Array.from(arguments).reduce((a, b) => a + b);
// };

// // Use rest parameters instead
// const sumWithRest = (...args) => {
//     return args.reduce((a, b) => a + b);
// };
// ```

// ## Method Definitions

// ### Regular Functions - Good for Methods
// ```javascript
// const calculator = {
//     value: 0,
//     add: function(n) {
//         this.value += n;
//         return this;
//     },
//     subtract: function(n) {
//         this.value -= n;
//         return this;
//     }
// };
// ```

// ### Arrow Functions - Better for Callbacks
// ```javascript
// const calculator = {
//     value: 0,
//     numbers: [1, 2, 3],
//     sum() {
//         // Arrow function preserves this
//         return this.numbers.reduce((acc, val) => acc + val, this.value);
//     }
// };
// ```

// ## Event Handlers

// ### Regular Functions - Rebinding Required
// ```javascript
// class Button {
//     constructor() {
//         this.clicked = false;
//         this.click = this.click.bind(this);
//     }
    
//     click() {
//         this.clicked = true;
//         console.log(this.clicked);
//     }
// }
// ```

// ### Arrow Functions - Automatic Binding
// ```javascript
// class Button {
//     clicked = false;
    
//     click = () => {
//         this.clicked = true;
//         console.log(this.clicked);
//     }
// }
// ```

// ## Best Practices

// 1. Use Arrow Functions For:
//    - Short callbacks
//    - Array methods (map, reduce, filter)
//    - Promise chains
//    - When you need lexical this

// 2. Use Regular Functions For:
//    - Object methods
//    - Constructor functions
//    - When you need the arguments object
//    - When you need function hoisting
//    - When this should be dynamic

// ## Common Patterns

// ### Event Handling
// ```javascript
// // Bad - this is lost
// class Component {
//     handleClick() {
//         this.setState({ clicked: true });
//     }
// }

// // Good - this is preserved
// class Component {
//     handleClick = () => {
//         this.setState({ clicked: true });
//     }
// }
// ```

// ### Array Methods
// ```javascript
// // Good use of arrow functions
// const numbers = [1, 2, 3, 4];
// const doubled = numbers.map(n => n * 2);
// const evens = numbers.filter(n => n % 2 === 0);
// const sum = numbers.reduce((acc, n) => acc + n, 0);
// ```

// ### Promise Chains
// ```javascript
// // Clean and concise with arrow functions
// fetchData()
//     .then(data => processData(data))
//     .then(result => console.log(result))
//     .catch(error => console.error(error));
// ```
