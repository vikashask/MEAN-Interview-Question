# ES6 (ECMAScript 2015) Interview Questions

## Basic ES6 Questions

1. **What is ES6 and when was it released?**
   - ES6 (ECMAScript 2015) is the sixth major release of the ECMAScript language specification. It was released in June 2015 and introduced significant enhancements to JavaScript.

2. **What are the major features introduced in ES6?**
   - Major features include: let/const declarations, arrow functions, template literals, destructuring, classes, modules, promises, generators, iterators, Map/Set collections, and default parameters.

3. **What's the difference between let, const, and var?**
   - `var`: Function-scoped, hoisted, can be redeclared and updated
   - `let`: Block-scoped, not hoisted, can be updated but not redeclared in same scope
   - `const`: Block-scoped, not hoisted, cannot be updated or redeclared, but object properties can be modified

4. **How do arrow functions differ from regular functions?**
   - Arrow functions have a more concise syntax
   - They don't have their own `this` binding (lexical `this`)
   - They don't have `arguments` object
   - Cannot be used as constructors (no `new` keyword)
   - Cannot use `yield` within them

5. **What are template literals and how do they improve string handling?**
   - Template literals use backticks (\`) instead of quotes
   - Allow multi-line strings without escape characters
   - Enable string interpolation with `${expression}` syntax
   - Support tagged templates for custom string processing

## Intermediate ES6 Questions

6. **Explain destructuring in ES6 and provide examples for both objects and arrays.**
   - Destructuring is a syntax that allows unpacking values from arrays or properties from objects into distinct variables.
   - Array example: `const [first, second] = [1, 2];`
   - Object example: `const { name, age } = person;`

7. **What is the spread operator and how is it used?**
   - The spread operator (`...`) allows an iterable to be expanded in places where zero or more arguments/elements are expected.
   - Used for array concatenation, copying arrays/objects, converting strings to arrays, and passing multiple arguments to functions.

8. **How do ES6 modules help with code organization?**
   - Modules provide a way to organize code into separate files
   - They use `import` and `export` statements to share functionality
   - They have their own scope (variables are not global)
   - They are singletons (imported only once)
   - They support both named and default exports

9. **What are Promises and how do they improve asynchronous programming?**
   - Promises represent a value that might be available now, later, or never
   - They help avoid callback hell with chainable `.then()` and `.catch()` methods
   - They have three states: pending, fulfilled, and rejected
   - They provide better error handling for asynchronous operations

10. **What is the purpose of the Symbol type in ES6?**
    - Symbols are unique and immutable primitive values
    - They can be used as object property keys to avoid name collisions
    - They enable private-like properties in objects
    - Well-known symbols allow customizing language behaviors (like iteration)

## Advanced ES6 Questions

11. **Explain how ES6 classes work under the hood. Are they true classes?**
    - ES6 classes are primarily syntactic sugar over JavaScript's prototype-based inheritance
    - They don't introduce a new object-oriented inheritance model
    - Under the hood, they still use prototype chains
    - The `class` syntax makes the code more readable and familiar to developers from class-based languages

12. **What are generators and how do they work with iterators?**
    - Generators are functions that can be paused and resumed, defined with `function*`
    - They use `yield` to pause and return values
    - They implement the iterator protocol automatically
    - They're useful for creating sequences, handling asynchronous operations, and managing control flow

13. **How can you handle multiple promises concurrently in ES6?**
    - `Promise.all()`: Waits for all promises to resolve or any to reject
    - `Promise.race()`: Settles as soon as any promise settles
    - `Promise.allSettled()`: Waits for all promises to settle regardless of state
    - `Promise.any()`: Resolves when any promise resolves, rejects only if all reject

14. **What are WeakMap and WeakSet, and when would you use them?**
    - They hold weak references to objects, allowing garbage collection when objects are no longer referenced elsewhere
    - `WeakMap`: Collection of key/value pairs where keys must be objects
    - `WeakSet`: Collection of objects
    - Used for storing metadata about objects without preventing garbage collection

15. **How do you implement the module pattern using ES6 features?**
    - Use ES6 modules with named and default exports
    - Leverage private variables through module scope
    - Create factory functions or classes for instance creation
    - Use Symbol properties for truly private members

## Performance and Optimization Questions

16. **How does ES6 affect performance compared to ES5?**
    - Modern browsers optimize ES6 features well, often matching or exceeding ES5 performance
    - Transpiled ES6 code may have slight overhead but is generally negligible
    - Some features like `for...of` loops can be slower than traditional `for` loops
    - Arrow functions can be optimized better by engines in certain cases
    - Destructuring can have minor performance costs but improves code readability

17. **What are the performance implications of using the spread operator vs. traditional methods?**
    - Spread operator is generally slower for large arrays compared to methods like `Array.prototype.concat()`
    - For small arrays or objects, the performance difference is negligible
    - Spread creates a shallow copy, which may be more memory efficient than deep copying
    - Modern JavaScript engines continue to optimize spread operations

18. **How can you optimize the use of Promises in high-performance applications?**
    - Avoid creating unnecessary Promises for synchronous operations
    - Use `Promise.all()` for concurrent operations instead of sequential chaining
    - Consider using async/await for better readability and debugging
    - Be cautious with Promise chains that process large data sets
    - Implement proper error handling to prevent memory leaks

## Practical Application Questions

19. **How would you refactor this ES5 code to use ES6 features?**
    ```javascript
    // ES5
    var user = {
      name: 'John',
      getFullName: function() {
        var self = this;
        return function() {
          return 'Mr. ' + self.name;
        };
      }
    };
    ```
    Answer:
    ```javascript
    // ES6
    const user = {
      name: 'John',
      getFullName() {
        return () => `Mr. ${this.name}`;
      }
    };
    ```

20. **How would you implement a throttle function using ES6 features?**
    ```javascript
    const throttle = (fn, delay) => {
      let lastCall = 0;
      return (...args) => {
        const now = new Date().getTime();
        if (now - lastCall < delay) {
          return;
        }
        lastCall = now;
        return fn(...args);
      };
    };
    ```

21. **How can you use ES6 features to implement the observer pattern?**
    ```javascript
    class Observable {
      constructor() {
        this.observers = new Set();
      }
      
      subscribe(observer) {
        this.observers.add(observer);
        return () => this.observers.delete(observer); // Unsubscribe function
      }
      
      notify(data) {
        this.observers.forEach(observer => observer(data));
      }
    }
    ```

## Compatibility and Tooling Questions

22. **How do you ensure ES6 code works in older browsers?**
    - Use transpilers like Babel to convert ES6 to ES5-compatible code
    - Include polyfills for missing features (e.g., Promise, Map, Set)
    - Use bundlers like webpack or Rollup with appropriate presets
    - Consider using feature detection for conditional feature usage
    - Test across multiple browsers and versions

23. **What tools in the JavaScript ecosystem help with writing modern ES6 code?**
    - Babel: For transpiling ES6+ to backward-compatible versions
    - ESLint: For linting and enforcing code style with ES6 rules
    - Prettier: For consistent code formatting
    - TypeScript: For static typing with ES6 features
    - webpack/Rollup: For bundling modules and applying transformations

24. **What are the trade-offs of using ES6 modules vs. CommonJS?**
    - ES6 modules are statically analyzed, allowing tree-shaking
    - CommonJS modules are dynamically evaluated at runtime
    - ES6 modules are asynchronous by design, CommonJS is synchronous
    - ES6 modules have better circular dependency handling
    - CommonJS has better compatibility with older Node.js versions

## Conceptual Understanding Questions

25. **How has ES6 influenced the evolution of JavaScript frameworks and libraries?**
    - Modern frameworks (React, Vue, Angular) heavily leverage ES6 features
    - Component-based architecture aligns well with ES6 classes and modules
    - Reactive programming patterns benefit from Promises and async/await
    - Functional programming approaches utilize arrow functions and destructuring
    - Build tools and transpilers have become essential parts of development workflows

## Coding Challenges and Real-World Scenarios

26. **Write a function that converts an array of objects to a Map using ES6 features.**
    ```javascript
    // Example: Convert [{id: 1, name: 'John'}, {id: 2, name: 'Jane'}] to Map where id is the key
    function arrayToMap(array, keyProp) {
      return new Map(array.map(item => [item[keyProp], item]));
    }
    
    // Usage
    const users = [{id: 1, name: 'John'}, {id: 2, name: 'Jane'}];
    const userMap = arrayToMap(users, 'id');
    // Map(2) {1 => {id: 1, name: 'John'}, 2 => {id: 2, name: 'Jane'}}
    ```

27. **Implement a debounce function using ES6 features.**
    ```javascript
    const debounce = (fn, delay) => {
      let timeoutId;
      return (...args) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn(...args), delay);
      };
    };
    
    // Usage
    const handleSearch = debounce((query) => {
      console.log(`Searching for: ${query}`);
      // API call here
    }, 300);
    ```

28. **Create a utility that deep freezes an object using ES6 features.**
    ```javascript
    function deepFreeze(obj) {
      // Get all properties, including non-enumerable ones
      const propNames = Object.getOwnPropertyNames(obj);
      
      // Freeze properties before freezing the object itself
      propNames.forEach(name => {
        const prop = obj[name];
        
        // Recursively freeze prop if it's an object and not already frozen
        if (prop !== null && (typeof prop === 'object' || typeof prop === 'function') 
            && !Object.isFrozen(prop)) {
          deepFreeze(prop);
        }
      });
      
      return Object.freeze(obj);
    }
    ```

29. **Implement a simple Promise-based cache mechanism.**
    ```javascript
    class Cache {
      constructor(ttl = 60000) { // Default TTL: 1 minute
        this.cache = new Map();
        this.ttl = ttl;
      }
      
      async get(key, fetchFn) {
        const now = Date.now();
        const cachedItem = this.cache.get(key);
        
        // Return cached value if it exists and hasn't expired
        if (cachedItem && now < cachedItem.expiry) {
          return cachedItem.value;
        }
        
        // Fetch new value
        try {
          const value = await fetchFn();
          this.cache.set(key, {
            value,
            expiry: now + this.ttl
          });
          return value;
        } catch (error) {
          // If fetch fails but we have a stale value, return it
          if (cachedItem) {
            return cachedItem.value;
          }
          throw error;
        }
      }
      
      invalidate(key) {
        this.cache.delete(key);
      }
    }
    ```

30. **Create a function that flattens a nested array using ES6 features.**
    ```javascript
    function flattenArray(arr) {
      return arr.reduce((flat, item) => {
        return flat.concat(Array.isArray(item) ? flattenArray(item) : item);
      }, []);
    }
    
    // Using built-in ES6+ method
    function modernFlatten(arr) {
      return arr.flat(Infinity);
    }
    ```