console.log(1 == '1')
// Its returns true because it's an auto-type conversion and it checks only value not type.
console.log(1 === '1')
// Its returns false because it's not auto-type conversion and it check value and type both.
console.log(1=== parseInt('1'))
//  its returns true.
 console.log(0 == false); // return true, because both are same type.
 console.log(0 === false); // return false, because both are of a different type.
 console.log(1 == "1"); // return true, automatic type conversion for value only.
 console.log(1 === "1"); // return false, because both are of a different type.
 console.log(null == undefined); // return true.
 console.log(null === undefined); // return false.
 console.log('0' == false); // return true.
 console.log('0' === false); // return false.
 console.log(1=== parseInt("1")); // return true.

//1.  What is the difference between undefined and not defined in 
var x; // declaring x
console.log(x); //output: undefined
// console.log(y);  // Output: ReferenceError: y is not defined

// 2.what would be output
var y1 = 1;
  if (function f(){}) {
    y1 += typeof f;
  }
  console.log(y1); 
/*
// 1undefined
eval(function f(){}) returns function f(){} (which is true)   
if statement, executing typeof f returns undefined because the if statement code executes at run time, 
and the statement inside the if condition is evaluated during run time.
*/
var k = 1;
  if (1) {
    function foo(){};
    k += typeof foo;
  }
  console.log(k); // output 1function

  /* 
  Write a function
  console.log(mul(2)(3)(4)); // output : 24 
  console.log(mul(4)(3)(4)); // output : 48
  */

 function multiply (x) {
  return function (y) { // anonymous function 
      return function (z) { // anonymous function 
          return x * y * z; 
      };
  };
}

/* How to empty an array */
var arrayList =  ['a','b','c','d','e','f'];
// Method 1
/* 
> arrayList = []; // Empty the array 
> arrayList.length = 0;
> arrayList.splice(0, arrayList.length);

while(arrayList.length){
  arrayList.pop();
} 
*/

/* How do you check if an object is an array or not? */
var arrayList1 = [1,2,3];
Array.isArray(arrayList1);

var output = (function(x){
  console.log('x=',x,'type of',typeof x);
  
  delete x;
  return x;
})(2);
console.log(output);
// 2
// The delete operator is used to delete properties from an object.

