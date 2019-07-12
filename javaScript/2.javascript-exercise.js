console.log('1.', 1 == '1')
console.log("2.", 1 === '1')
console.log("3.", 1 === parseInt('1'))
// 1. TRUE because it's an auto-type conversion and it checks only value not type.
// 2. FALSE because it's not auto-type conversion and it check value and type both.
// 3. TRUE.

console.log("4", 0 == false);
console.log("5", 0 === false);
console.log("6", 1 == "1");
console.log("7", 1 === "1");
//4. true, because both are same type.
//5. false, because both are of a different type.
//6. true, automatic type conversion for value only.
//7. false, because both are of a different type.

console.log('8', null == undefined);
console.log('9', null === undefined);
console.log('10', '0' == false);
console.log('11', '0' === false);
console.log('12', 1 === parseInt("1"));

//8  true.
//9  false.
//10 true.
//11 false.
//12 true.

var bar = true;
console.log('13', bar + 0);
console.log('14', bar + "xyz");
console.log('15', bar + true);
console.log('16', bar + false);
// 13 1 
// 14 truexyz
// 15 2
// 16 1