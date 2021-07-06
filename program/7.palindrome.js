// check palidrome for string
// MADAM is palindrome
var isPalindrome = function (string) {
    if (string == string.split('').reverse().join('')) {
        console.log(string + ' is palindrome.');
    }
    else {
        console.log(string + ' is not palindrome.');
    }
}
console.log(isPalindrome('121'));
console.log(isPalindrome('madam'));

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

//  - -  -- - - - FOR LOOP - - - - - - 
function checkPalindrome(string) {
    // find the length of a string
    const len = string.length;
    // loop through half of the string
    for (let i = 0; i < len / 2; i++) {
        // check if first and last string are same
        if (string[i] !== string[len - 1 - i]) {
            console.log(string," is not a palindrome");
        }
    }
    console.log(string,' is a palindrome');
}
const checkPalin = checkPalindrome("madam");
console.log("checkPalin--".checkPalin);