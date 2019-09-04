/* 
1. How to implement array intersection in javascript
example:
let arr1 = [1,2,3];
let arr2 = [2,3,4,5];
output: [2,3];
*/
let arr1 = [1,2,3];
let arr2 = [2,3,4,5];

let intSecValue1 = arr1.filter(value => -1 !== arr2.indexOf(value));
console.log("intSecValue1",intSecValue1);

// OR 
let intSecValue2 = arr1.filter(value => arr2.includes(value));
console.log("intSecValue2",intSecValue2);

/* 
2. Unioin of two array
*/
var a = [34, 35, 45, 48, 49];
var b = [48, 55];
var union = [...new Set([...a, ...b])]; // very important
console.log('union',union);

/* 
3.How to merge two arrays in JavaScript and de-duplicate items
 */
var array1 = ["vikash","jay"];
var array2 = ["jay", "ram"];

// o/p should be var array3 = ["vikash","jay","jay","ram"];
//using destructuring
let meargeAr = [...array1,...array2];
console.log('meargeAr',meargeAr);

//using Array.concat
let meargeAr2 = array1.concat(array2)
console.log('meargeAr2',meargeAr2);
