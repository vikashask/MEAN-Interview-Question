
//1.? What is the difference between undefined and not defined in 
var x; // declaring x
console.log('17', x);
// console.log('18',y);  

// 2.? what would be output
var y1 = 1;
if (function f() {}) {
  y1 += typeof f;
}
console.log(y1);

//3. what will be output
var k = 1;
if (1) {
  function foo() {};
  k += typeof foo;
}
console.log(k);

/* 
4.? Write a function curring function
console.log(mul(2)(3)(4)); // output : 24 
*/

function multiply(x) {
  return function (y) { // anonymous function 
    return function (z) { // anonymous function 
      return x * y * z;
    };
  };
}

/* 5.? How to empty an array */
var arrayList = ['a', 'b', 'c', 'd', 'e', 'f'];

/* 6.? How do you check if an object is an array or not? */
var arrayList1 = [1, 2, 3];

// 7.what will be output
var output = (function (x) {
  console.log('x=', x, 'type of', typeof x);
  delete x;
  return x;
})(2);
console.log(output);

/* 8.? What will be the output of the code below? */
var x1 = {
  foo: 1
};
var output2 = (function () {
  delete x1.foo;
  return x1.foo;
})();
console.log(output2);

/* 9.? What will be the output of the code below? */
var Employee = {
  company: 'xyz'
}
var emp1 = Object.create(Employee);
delete emp1.company
console.log(emp1.company);
console.log(emp1.hasOwnProperty('company')); //output : false

/* 10.? what would be output */
var trees = ["redwood", "bay", "cedar", "oak", "maple"];
delete trees[3];
console.log(trees);
trees.push();
console.log(trees.length); // 5

/* 11.? What would be output */
var z = 1,
  y = z = typeof y;

/* 12.? What would be output */
var foo = function bar() {
  return 12;
};
typeof bar(); 

// 13. ? what will be output
var bar = function () {
  return 12;  
};
typeof bar();
console.log("typeof bar()", bar());


//14. difference between the function declarations below?
var foo1 = function () {
  // Some code
};

function bar1() {
  // Some code
};
// The main difference is the function foo is defined at run-time whereas function bar is defined at parse time.