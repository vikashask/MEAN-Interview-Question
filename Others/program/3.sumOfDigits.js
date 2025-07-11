function sumOfDigits(value){
    var sum = 0;
    while (value) {
        sum += value % 10;
        value = Math.floor(value / 10);
    }
    return sum;
}
let result = sumOfDigits(12);
console.log('result',result);

/*
converting number to string and spliting and getting array with all digit and perform redude to get sum
*/
function sumOfDigitsString(value) {
    var sum = value
        .toString()
        .split('')
        .map(Number)
        .reduce(function (a, b) {
            return a + b;
        }, 0);
return `sum of ${value} is ${sum}`;
}

let sum = sumOfDigitsString(234);
console.log(sum);

// var sumGlobal = 0;
function add_digits(no) {
    var sum = 0;
    if (no == 0) {
      return 0;
    }
    sum = no%10 + add_digits(no/10);
    return Math.floor(sum);
    return `sum of ${no} is ${Math.floor(sum)}`;
  }

let resultRecursive = add_digits(123);
console.log('recursive',resultRecursive);
