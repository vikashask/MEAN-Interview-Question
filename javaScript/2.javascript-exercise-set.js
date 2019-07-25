console.log('1.', 1 == '1')
console.log("2.", 1 === '1')
console.log("3.", 1 === parseInt('1'))

console.log("4", 0 == false);
console.log("5", 0 === false);
console.log("6", 1 == "1");
console.log("7", 1 === "1");

console.log('8', null == undefined);
console.log('9', null === undefined);
console.log('10', '0' == false);
console.log('11', '0' === false);
console.log('12', 1 === parseInt("1"));

var bar = true;
console.log('13', bar + 0);
console.log('14', bar + "xyz");
console.log('15', bar + true);
console.log('16', bar + false);
