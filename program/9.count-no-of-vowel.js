// Example 1: Count the Number of Vowels Using Regex
function countNoOfVowels(string) {
    return string.match(/[aeiou]/gi).length
}
console.log("countNoOfVowels --", countNoOfVowels("demo"))


//  Using for loop by using include function
const vowels = ["a", "e", "i", "o", "u"]

function countVowel(str) {
    let count = 0;
    // loop through string to test if each character is a vowel
    for (let letter of str.toLowerCase()) {
        if (vowels.includes(letter)) {
            count++;
        }
    }
    // return number of vowels
    return count
}