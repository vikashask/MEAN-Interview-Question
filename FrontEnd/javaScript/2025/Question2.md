# JavaScript String Methods and Regular Expressions

## search() Method
The `search()` method searches a string for a specified value or regular expression and returns the position of the match.

```javascript
const str = "Hello World!";
console.log(str.search("World"));     // Returns 6
console.log(str.search(/World/));     // Returns 6
console.log(str.search(/javascript/)); // Returns -1 if not found
```

## split() Method
The `split()` method splits a string into an array of substrings based on a specified delimiter.

```javascript
const str = "Hello,World,JavaScript";

// Split by comma
console.log(str.split(",")); // ["Hello", "World", "JavaScript"]

// Split by space
const sentence = "The quick brown fox";
console.log(sentence.split(" ")); // ["The", "quick", "brown", "fox"]

// Split into characters
console.log("hello".split("")); // ["h", "e", "l", "l", "o"]

// Limit the number of splits
console.log(str.split(",", 2)); // ["Hello", "World"]
```

## replace() Method
The `replace()` method returns a new string with some or all matches of a pattern replaced by a replacement.

```javascript
const str = "Hello World";

// Replace first occurrence
console.log(str.replace("o", "0")); // "Hell0 World"

// Replace all occurrences using regex
console.log(str.replace(/o/g, "0")); // "Hell0 W0rld"

// Using function as replacer
const text = "cat, bat, rat";
console.log(text.replace(/[cbr]at/g, match => match.toUpperCase()));
// "CAT, BAT, RAT"
```

## test() Method
The `test()` method tests for a match in a string and returns true or false.

```javascript
const pattern = /hello/i;
console.log(pattern.test("Hello World")); // true
console.log(pattern.test("Good morning")); // false

// Testing for numbers
const hasNumber = /\d/.test("abc123"); // true

// Testing for email format
const isEmail = /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test("test@email.com"); // true
```

## Group Capturing
Group capturing allows you to extract specific parts of a match using parentheses in regular expressions.

```javascript
// Basic group capturing
const regex = /(\w+)\s(\w+)/;
const str = "John Doe";
const match = str.match(regex);
console.log(match[1]); // "John"
console.log(match[2]); // "Doe"

// Named groups (ES2018+)
const nameRegex = /(?<first>\w+)\s(?<last>\w+)/;
const result = "John Doe".match(nameRegex).groups;
console.log(result.first); // "John"
console.log(result.last);  // "Doe"

// Multiple captures
const dates = "2025-07-11 and 2025-12-25";
const dateRegex = /(\d{4})-(\d{2})-(\d{2})/g;
const matches = [...dates.matchAll(dateRegex)];
matches.forEach(match => {
    console.log(`Year: ${match[1]}, Month: ${match[2]}, Day: ${match[3]}`);
});
```

## Back Reference
Back references in regex allow you to match the same text that was matched by a capturing group earlier in the regex.

```javascript
// Finding repeated words
const repeatedWord = /(\b\w+\b)\s+\1/g;
console.log("the the quick quick".match(repeatedWord)); 
// ["the the", "quick quick"]

// HTML tag matching
const htmlTag = /<(\w+)>.*?<\/\1>/;
console.log(htmlTag.test("<div>Hello</div>")); // true
console.log(htmlTag.test("<div>Hello</span>")); // false

// Back reference in replace
const fixRepeats = "hello hello world world";
console.log(fixRepeats.replace(/(\b\w+\b)\s+\1/g, "$1"));
// "hello world"
```

## Regex Validation Examples

### 1. Validate First Letter Uppercase
```javascript
const isFirstLetterUpper = (str) => {
    return /^[A-Z]/.test(str);
};

console.log(isFirstLetterUpper("Hello")); // true
console.log(isFirstLetterUpper("hello")); // false
```

### 2. Validate String Beginning with Digit
```javascript
const startsWithDigit = (str) => {
    return /^\d/.test(str);
};

console.log(startsWithDigit("1hello")); // true
console.log(startsWithDigit("hello1")); // false
```

### 3. Validate Word Containing Only Digits
```javascript
const hasOnlyDigits = (str) => {
    return /^\d+$/.test(str);
};

console.log(hasOnlyDigits("12345")); // true
console.log(hasOnlyDigits("123a45")); // false
```

### 4. Validate Word Containing Only Letters
```javascript
const hasOnlyLetters = (str) => {
    return /^[A-Za-z]+$/.test(str);
};

console.log(hasOnlyLetters("Hello")); // true
console.log(hasOnlyLetters("Hello123")); // false
```

### 5. Validate All Uppercase Characters
```javascript
const isAllUppercase = (str) => {
    return /^[A-Z]+$/.test(str);
};

console.log(isAllUppercase("HELLO")); // true
console.log(isAllUppercase("HeLLo")); // false
```

### 6. Count Vowels and Consonants
```javascript
const countVowelsAndConsonants = (str) => {
    const vowels = (str.match(/[aeiou]/gi) || []).length;
    const consonants = (str.match(/[bcdfghjklmnpqrstvwxyz]/gi) || []).length;
    return { vowels, consonants };
};

const result = countVowelsAndConsonants("Hello World");
console.log(result); // { vowels: 3, consonants: 7 }
```

### 7. Find Double Words
```javascript
const findDoubleWords = (str) => {
    return str.match(/\b(\w+)\s+\1\b/g) || [];
};

console.log(findDoubleWords("nice nice day day")); 
// ["nice nice", "day day"]
```

### 8. Find Words with Specific Length
```javascript
const findWordsWithLength = (str, length) => {
    const regex = new RegExp(`\\b\\w{${length}}\\b`, 'g');
    return str.match(regex) || [];
};

console.log(findWordsWithLength("The quick brown fox jumps", 5));
// ["quick", "brown", "jumps"]
```

### 9. Validate Date Format (mm/dd/yyyy)
```javascript
const isValidDateFormat = (dateStr) => {
    return /^(0[1-9]|1[0-2])\/(0[1-9]|[12]\d|3[01])\/\d{4}$/.test(dateStr);
};

console.log(isValidDateFormat("07/11/2025")); // true
console.log(isValidDateFormat("13/45/2025")); // false
```