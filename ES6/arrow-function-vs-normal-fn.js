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
