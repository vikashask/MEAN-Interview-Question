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

