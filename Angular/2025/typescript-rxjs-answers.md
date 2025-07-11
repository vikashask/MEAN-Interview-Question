# TypeScript and RxJS Interview Questions and Answers

## TypeScript Section

### 1. What are the pros and cons of TypeScript?

**Pros:**
1. **Static Typing**
   - Catch errors at compile time
   - Better IDE support and IntelliSense
   - Improved code maintainability

2. **Object-Oriented Features**
   - Classes and Interfaces
   - Generics
   - Decorators
   - Access modifiers

3. **Enhanced Code Quality**
   - Better documentation
   - Easier refactoring
   - Type inference
   - Module support

4. **ECMAScript Compatibility**
   - Support for latest JavaScript features
   - Backward compatibility
   - Future-proof code

**Cons:**
1. **Additional Learning Curve**
   - New syntax to learn
   - Type system complexity
   - Configuration overhead

2. **Build Step Required**
   - Need to compile to JavaScript
   - Additional setup time
   - Build process complexity

3. **Overhead**
   - More initial code to write
   - Type definition maintenance
   - Larger project setup time

### 2. How to create TypeScript interface?

Interfaces define contracts in your code and provide explicit names for type checking:

```typescript
// Basic interface
interface User {
    id: number;
    name: string;
    email?: string; // Optional property
    readonly createdAt: Date; // Read-only property
}

// Interface with methods
interface Vehicle {
    start(): void;
    stop(): void;
    speed: number;
}

// Interface extending another interface
interface Employee extends User {
    salary: number;
    department: string;
}

// Implementing interface in class
class Car implements Vehicle {
    speed: number = 0;
    
    start() {
        console.log('Starting car');
    }
    
    stop() {
        this.speed = 0;
    }
}
```

### 3. How to define TypeScript array?

There are several ways to define arrays in TypeScript:

```typescript
// Using square brackets
let numbers: number[] = [1, 2, 3, 4, 5];
let names: string[] = ['John', 'Jane', 'Bob'];

// Using Array generic type
let numbers2: Array<number> = [1, 2, 3, 4, 5];
let names2: Array<string> = ['John', 'Jane', 'Bob'];

// Mixed type array using union
let mixed: (string | number)[] = [1, 'two', 3, 'four'];

// Array of objects
interface Person {
    name: string;
    age: number;
}
let people: Person[] = [
    { name: 'John', age: 30 },
    { name: 'Jane', age: 25 }
];

// Readonly arrays
const readOnlyNumbers: ReadonlyArray<number> = [1, 2, 3];
// readOnlyNumbers[0] = 4; // Error
```

### 4. What is type assertion in TypeScript?

Type assertion is a way to tell the TypeScript compiler "trust me, I know what I'm doing" when you have more specific information about a value's type than TypeScript does:

```typescript
// Using angle-bracket syntax
let someValue: any = "this is a string";
let strLength: number = (<string>someValue).length;

// Using 'as' syntax (preferred, especially in JSX)
let someValue2: any = "this is a string";
let strLength2: number = (someValue2 as string).length;

// Asserting to multiple types
let input = document.getElementById('input') as HTMLInputElement;

// Assertions with custom types
interface User {
    name: string;
    id: number;
}

let userObj: any = { name: 'John', id: 1 };
let user = userObj as User;
```

### 5. What is void and unknown in TypeScript?

**void:**
- Represents the absence of any type
- Commonly used as function return type
- Can only be assigned undefined or null (in non-strict mode)

```typescript
// Function returning void
function logMessage(message: string): void {
    console.log(message);
    // No return statement needed
}

// Variable of type void
let unusable: void = undefined;
// unusable = 1; // Error
```

**unknown:**
- Type-safe counterpart of any
- Nothing can be done with an unknown value without type checking
- Must narrow type before using

```typescript
let value: unknown = "Hello World";

// Must check type before using
if (typeof value === "string") {
    console.log(value.toUpperCase());
}

// Function accepting unknown
function processValue(val: unknown): string {
    if (Array.isArray(val)) {
        return val.join(',');
    }
    if (typeof val === 'string') {
        return val.toUpperCase();
    }
    return String(val);
}
```

### 6. Create function annotation in TypeScript

Function annotations specify the types of parameters and return values:

```typescript
// Basic function type
function add(x: number, y: number): number {
    return x + y;
}

// Arrow function type
const multiply: (x: number, y: number) => number = 
    (x, y) => x * y;

// Function type with optional parameter
function greet(name: string, greeting?: string): string {
    return greeting ? `${greeting}, ${name}!` : `Hello, ${name}!`;
}

// Function type with default parameter
function countdown(start: number = 10): void {
    console.log(start);
}

// Function type with rest parameters
function sum(...numbers: number[]): number {
    return numbers.reduce((total, n) => total + n, 0);
}

// Generic function type
function identity<T>(arg: T): T {
    return arg;
}

// Interface for function type
interface MathFunc {
    (x: number, y: number): number;
}
let add2: MathFunc = (x, y) => x + y;
```

### 7. What is the purpose of tsconfig.json?

The tsconfig.json file specifies the root files and compiler options for a TypeScript project:

```json
{
    "compilerOptions": {
        "target": "ES2020",        // ECMAScript target version
        "module": "commonjs",      // Module system
        "strict": true,            // Enable all strict type checking
        "esModuleInterop": true,   // Enable ES Module interop
        "skipLibCheck": true,      // Skip type checking of declaration files
        "forceConsistentCasingInFileNames": true,
        "outDir": "./dist",        // Output directory
        "rootDir": "./src",        // Source directory
        "declaration": true,       // Generate .d.ts files
        "sourceMap": true         // Generate source maps
    },
    "include": [
        "src/**/*"               // Files to include
    ],
    "exclude": [
        "node_modules",          // Files to exclude
        "**/*.spec.ts"
    ]
}
```

Key purposes:
1. Specifies compiler options
2. Defines root files
3. Sets up project structure
4. Configures type checking
5. Manages file inclusion/exclusion

### 8. What is elvis operator in TypeScript?

The elvis operator (?.) is also known as the optional chaining operator. It allows safe access to nested properties and methods:

```typescript
// Without elvis operator
const value = user && user.address && user.address.street;

// With elvis operator
const value = user?.address?.street;

// With methods
const result = obj?.method?.();

// Combined with nullish coalescing
const name = user?.name ?? 'Anonymous';

// Array access
const item = arr?.[0];

// Real-world example
interface User {
    name: string;
    address?: {
        street?: string;
        city?: string;
    };
}

function getUserCity(user?: User): string {
    return user?.address?.city ?? 'Unknown City';
}
```

### 9. Why any is bad in TypeScript?

Using `any` defeats the purpose of TypeScript's type system:

**Problems with any:**
1. **Loss of Type Safety**
   ```typescript
   let value: any = "hello";
   value = 42;        // No error
   value.nonexistent(); // No error at compile time, fails at runtime
   ```

2. **No IntelliSense Support**
   ```typescript
   let obj: any = { name: "John" };
   // No autocomplete for obj.
   ```

3. **Type Inference Breaking**
   ```typescript
   function processValue(val: any) {
       // TypeScript can't help here
       val.toString(); // Might fail at runtime
   }
   ```

**Better Alternatives:**
```typescript
// Use unknown instead
function processValue(val: unknown) {
    if (typeof val === "string") {
        console.log(val.toUpperCase()); // Safe
    }
}

// Use specific types
interface User {
    name: string;
    age: number;
}
function processUser(user: User) {
    console.log(user.name); // Safe
}

// Use generics
function identity<T>(arg: T): T {
    return arg;
}
```

### 10. What are enums in TypeScript?

Enums allow defining a set of named constants:

```typescript
// Numeric enum
enum Direction {
    Up = 1,
    Down,      // 2
    Left,      // 3
    Right      // 4
}

// String enum
enum Color {
    Red = "RED",
    Green = "GREEN",
    Blue = "BLUE"
}

// Heterogeneous enum
enum BooleanLikeHeterogeneousEnum {
    No = 0,
    Yes = "YES",
}

// Computed enum
enum FileAccess {
    None,
    Read = 1 << 1,
    Write = 1 << 2,
    ReadWrite = Read | Write
}

// Const enum (more efficient)
const enum HttpStatus {
    OK = 200,
    NotFound = 404,
    Error = 500
}

// Usage example
function move(direction: Direction) {
    switch (direction) {
        case Direction.Up:
            return { x: 0, y: 1 };
        case Direction.Down:
            return { x: 0, y: -1 };
        // ...
    }
}
```

### 11. How to create custom types in TypeScript?

Custom types can be created using various TypeScript features:

```typescript
// Type alias
type Point = {
    x: number;
    y: number;
};

// Union type
type Result = string | number;

// Intersection type
type Employee = Person & { salary: number };

// Literal type
type Direction = 'up' | 'down' | 'left' | 'right';

// Mapped type
type Optional<T> = {
    [P in keyof T]?: T[P];
};

// Conditional type
type NonNullable<T> = T extends null | undefined ? never : T;

// Template literal type
type EmailLocaleIDs = `email_${string}`;

// Utility type combinations
type ReadOnlyPoint = Readonly<Point>;
type PartialPoint = Partial<Point>;

// Example usage
const point: Point = { x: 10, y: 20 };
const direction: Direction = 'up';
const optionalPoint: Optional<Point> = { x: 10 };
```

### 12. What are generics in TypeScript?

Generics allow creating reusable components that work with multiple types:

```typescript
// Generic function
function identity<T>(arg: T): T {
    return arg;
}

// Generic interface
interface Container<T> {
    value: T;
    getValue(): T;
}

// Generic class
class Queue<T> {
    private data: T[] = [];
    
    push(item: T) {
        this.data.push(item);
    }
    
    pop(): T | undefined {
        return this.data.shift();
    }
}

// Multiple type parameters
function pair<T, U>(first: T, second: U): [T, U] {
    return [first, second];
}

// Generic constraints
interface Lengthwise {
    length: number;
}

function loggingIdentity<T extends Lengthwise>(arg: T): T {
    console.log(arg.length);
    return arg;
}

// Generic type aliases
type ResponseWrapper<T> = {
    data: T;
    status: number;
    message: string;
};

// Usage examples
const numberQueue = new Queue<number>();
const response: ResponseWrapper<string[]> = {
    data: ['item1', 'item2'],
    status: 200,
    message: 'Success'
};
```

## RxJS Section

### 1. What are pros and cons of RxJS?

**Pros:**
1. **Powerful Data Handling**
   - Stream-based programming
   - Rich operator ecosystem
   - Handles async operations elegantly

2. **Composition**
   - Combine multiple data streams
   - Transform data easily
   - Chain operations

3. **Error Handling**
   - Built-in error handling
   - Retry mechanisms
   - Error recovery strategies

4. **State Management**
   - Predictable state flows
   - Reactive programming model
   - Easy to test

**Cons:**
1. **Learning Curve**
   - Complex concepts
   - Many operators to learn
   - Different programming paradigm

2. **Debugging Complexity**
   - Stack traces can be confusing
   - Memory leaks if not managed properly
   - Complex error scenarios

3. **Bundle Size**
   - Adds to application size
   - Need to be careful with imports

### 2. How to transform data in RxJS?

RxJS provides various operators for data transformation:

```typescript
import { map, pluck, mergeMap, switchMap, concatMap } from 'rxjs/operators';
import { of, from } from 'rxjs';

// Basic transformation using map
of(1, 2, 3).pipe(
    map(x => x * 2)
); // Output: 2, 4, 6

// Transform object properties
const users = of({ name: 'John', age: 30 });
users.pipe(
    map(user => ({
        ...user,
        age: user.age + 1
    }))
);

// Extract property using pluck
const people = of(
    { name: 'John', address: { city: 'NY' } },
    { name: 'Jane', address: { city: 'LA' } }
);
people.pipe(
    pluck('address', 'city')
); // Output: 'NY', 'LA'

// Transform with async operations
const getUserDetails = (id: number) => 
    of({ id, name: `User ${id}` });

from([1, 2, 3]).pipe(
    mergeMap(id => getUserDetails(id))
);
```

### 3. How filter works in RxJS?

RxJS provides several filtering operators:

```typescript
import { filter, take, skip, distinct, debounceTime } from 'rxjs/operators';
import { from, fromEvent } from 'rxjs';

// Basic filtering
from([1, 2, 3, 4, 5]).pipe(
    filter(x => x % 2 === 0)
); // Output: 2, 4

// Take specific number of values
from([1, 2, 3, 4, 5]).pipe(
    take(3)
); // Output: 1, 2, 3

// Skip values
from([1, 2, 3, 4, 5]).pipe(
    skip(2)
); // Output: 3, 4, 5

// Remove duplicates
from([1, 1, 2, 2, 3, 3]).pipe(
    distinct()
); // Output: 1, 2, 3

// Debounce user input
fromEvent(inputElement, 'input').pipe(
    debounceTime(300),
    map(event => (event.target as HTMLInputElement).value)
);
```

### 4. How to implement error handling in RxJS?

RxJS provides multiple ways to handle errors:

```typescript
import { catchError, retry, retryWhen, delay } from 'rxjs/operators';
import { throwError, of } from 'rxjs';

// Basic error handling
observable.pipe(
    catchError(error => {
        console.error('Error:', error);
        return of([]); // Return fallback value
    })
);

// Retry on error
observable.pipe(
    retry(3), // Retry 3 times
    catchError(error => of([]))
);

// Advanced retry with delay
observable.pipe(
    retryWhen(errors => 
        errors.pipe(
            delay(1000), // Wait 1 second before retrying
            take(3)      // Maximum 3 retries
        )
    )
);

// Error handling with async operations
const fetchData = () => {
    return httpClient.get('/api/data').pipe(
        catchError(error => {
            if (error.status === 404) {
                return of([]); // Return empty array for 404
            }
            return throwError(() => error); // Re-throw other errors
        })
    );
};
```

### 5. What does combineLatest operator do in RxJS?

`combineLatest` combines multiple observables and emits when any source observable emits:

```typescript
import { combineLatest, timer, of } from 'rxjs';

// Basic combineLatest
const numbers$ = of(1, 2, 3);
const letters$ = of('a', 'b', 'c');

combineLatest([numbers$, letters$]).subscribe(
    ([num, letter]) => console.log(`${num}${letter}`)
);

// Real-world example: Form validation
const username$ = usernameInput.valueChanges;
const email$ = emailInput.valueChanges;
const password$ = passwordInput.valueChanges;

combineLatest([username$, email$, password$]).pipe(
    map(([username, email, password]) => {
        return {
            isValid: username.length > 0 && 
                    email.includes('@') && 
                    password.length >= 8,
            values: { username, email, password }
        };
    })
);
```

### 6. How Subject and BehaviorSubject work in RxJS?

Subjects are both observers and observables:

```typescript
import { Subject, BehaviorSubject } from 'rxjs';

// Subject
const subject = new Subject<number>();

subject.subscribe(x => console.log('A:', x));
subject.next(1); // A: 1

subject.subscribe(x => console.log('B:', x));
subject.next(2); // A: 2, B: 2

// BehaviorSubject (requires initial value)
const behaviorSubject = new BehaviorSubject<number>(0);

behaviorSubject.subscribe(x => console.log('A:', x)); // A: 0
behaviorSubject.next(1); // A: 1

behaviorSubject.subscribe(x => console.log('B:', x)); // B: 1
behaviorSubject.next(2); // A: 2, B: 2

// Real-world example: State management
class StateService {
    private state = new BehaviorSubject<any>({
        user: null,
        isLoading: false
    });
    
    getState() {
        return this.state.asObservable();
    }
    
    updateState(newState: any) {
        this.state.next({
            ...this.state.value,
            ...newState
        });
    }
}
```

### 7. Observables vs Promises - what is the difference?

Key differences between Observables and Promises:

```typescript
// Promise (single value)
const promise = new Promise(resolve => {
    resolve(1);
    resolve(2); // Ignored
});

// Observable (multiple values)
const observable = new Observable(subscriber => {
    subscriber.next(1);
    subscriber.next(2); // Emitted
    subscriber.complete();
});

// Promise example
async function fetchData() {
    try {
        const data = await fetch('/api/data');
        return data.json();
    } catch (error) {
        console.error(error);
    }
}

// Observable example
function fetchDataStream() {
    return new Observable(subscriber => {
        fetch('/api/data')
            .then(response => response.json())
            .then(data => {
                subscriber.next(data);
                subscriber.complete();
            })
            .catch(error => subscriber.error(error));
    });
}

// Differences:
// 1. Cancellation
const subscription = observable.subscribe(/*...*/);
subscription.unsubscribe(); // Can be cancelled

// 2. Transformation
observable.pipe(
    map(x => x * 2),
    filter(x => x > 0)
);

// 3. Retry
observable.pipe(
    retry(3)
);
```

### 8. Cold vs Hot Observables - what is the difference?

```typescript
// Cold Observable (unicast)
const cold$ = new Observable(subscriber => {
    const random = Math.random();
    subscriber.next(random);
});

cold$.subscribe(x => console.log('Sub 1:', x));
cold$.subscribe(x => console.log('Sub 2:', x));
// Different values for each subscriber

// Hot Observable (multicast)
const subject = new Subject();
const hot$ = subject.asObservable();

hot$.subscribe(x => console.log('Sub 1:', x));
hot$.subscribe(x => console.log('Sub 2:', x));
subject.next(Math.random());
// Same value for all subscribers

// Making cold observable hot
const source$ = interval(1000).pipe(
    share() // Now it's hot
);
```

### 9. ConcatMap vs SwitchMap vs MergeMap vs Map vs ExhaustMap in RxJS

These operators handle inner observables differently:

```typescript
import { concatMap, switchMap, mergeMap, map, exhaustMap } from 'rxjs/operators';

// map - Simple value transformation
observable.pipe(
    map(x => x * 2)
);

// concatMap - Sequential execution
// Waits for each inner observable to complete
clicks$.pipe(
    concatMap(event => http.get('/api/data'))
);

// switchMap - Switches to new observable, cancels previous
// Used for search typeahead
searchInput$.pipe(
    switchMap(term => http.get(`/api/search?q=${term}`))
);

// mergeMap - Parallel execution
// Handles multiple inner observables simultaneously
userIds$.pipe(
    mergeMap(id => http.get(`/api/user/${id}`))
);

// exhaustMap - Ignores new values while inner observable is active
// Used for login to prevent double submission
loginButton$.pipe(
    exhaustMap(event => http.post('/api/login', credentials))
);

// Real-world example: File upload with progress
const upload$ = file$.pipe(
    switchMap(file => {
        const formData = new FormData();
        formData.append('file', file);
        
        return http.post('/api/upload', formData).pipe(
            map(event => {
                if (event.type === HttpEventType.UploadProgress) {
                    return {
                        progress: Math.round(100 * event.loaded / event.total)
                    };
                }
                return { progress: 100 };
            })
        );
    })
);
```