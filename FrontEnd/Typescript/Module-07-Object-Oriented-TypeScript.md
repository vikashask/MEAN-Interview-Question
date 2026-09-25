# 📦 Module 7: Object-Oriented TypeScript

🟡 **Intermediate**

## 7.1 Basic Class

```typescript
class Person {
  name: string;
  age: number;

  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }

  greet(): string { return `Hi, I'm ${this.name}`; }
}
```

## 7.2 Access Modifiers

| Modifier | Accessible In |
| :--- | :--- |
| `public` (default) | Everywhere |
| `private` | This class only |
| `protected` | This class + subclasses |
| `readonly` | Set once |

```typescript
class BankAccount {
  public owner: string;
  private balance: number;
  readonly accountNumber: string;

  constructor(owner: string, balance: number, accNum: string) {
    this.owner = owner;
    this.balance = balance;
    this.accountNumber = accNum;
  }

  deposit(amount: number): void { this.balance += amount; }
  getBalance(): number { return this.balance; }
}
```

## 7.3 Parameter Properties Shorthand

```typescript
class Product {
  constructor(
    public name: string,
    private price: number,
    readonly sku: string
  ) {} // TS declares and assigns automatically
}
```

## 7.4 Inheritance

```typescript
class Animal {
  constructor(public name: string) {}
  speak(): string { return `${this.name} makes a sound.`; }
}

class Dog extends Animal {
  constructor(name: string, public breed: string) {
    super(name); // Must call super() first!
  }
  speak(): string { return `${this.name} barks!`; }
}
```

## 7.5 Abstract Classes

Cannot be instantiated — only extended.

```typescript
abstract class Shape {
  abstract getArea(): number; // subclass MUST implement this

  printArea(): void { console.log(`Area: ${this.getArea()}`); }
}

class Circle extends Shape {
  constructor(private radius: number) { super(); }
  getArea(): number { return Math.PI * this.radius ** 2; }
}

// new Shape(); // ❌ ERROR
new Circle(5).printArea(); // ✅
```

## 7.6 Implementing Interfaces

```typescript
interface Serializable { serialize(): string; }
interface Loggable { log(): void; }

class User implements Serializable, Loggable {
  constructor(public name: string) {}
  serialize(): string { return JSON.stringify({ name: this.name }); }
  log(): void { console.log(this.name); }
}
```

---

## ⚡ Key Takeaways — Module 7

- `private`, `protected`, `public` control access
- Parameter properties shorthand reduces boilerplate
- `abstract` classes define contracts that subclasses must implement
- `implements` enforces interface contracts on classes

---

## ✅ Checklist — Module 7

- [ ] I can write classes with properties, methods, and constructors
- [ ] I understand all 4 access modifiers
- [ ] I can use parameter property shorthand
- [ ] I can use inheritance with `extends` and `super`
- [ ] I understand abstract classes
- [ ] I can implement interfaces on classes

---
