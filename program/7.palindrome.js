// check palidrome for string
var isPalindrome = function (string) {
    if (string == string.split('').reverse().join('')) {
        console.log(string + ' is palindrome.');
    }
    else {
        console.log(string + ' is not palindrome.');
    }
}
console.log(isPalindrome('121'));

// check palidrome for number
var isNumberPalindrome = function (number) {
    if (number == number.toString().split('').reverse().join('')) {
        console.log(number + ' is palindrome.');
    }
    else {
        console.log(number + ' is not palindrome.');
    }
}
console.log(isNumberPalindrome(1213));
