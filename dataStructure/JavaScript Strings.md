# JavaScript Strings

## JavaScript String Primitive

### String Access

For accessing characters, you use `.charAt()`.

```javascript
"dog".charAt(1);
// returns "o"
```

### String Comparison

```javascript
console.log("a" < "b");
// prints 'true'
console.log("add" < "ab");
// prints 'false'
```

### String Search

```javascript
"Red Dragon".indexOf("Red");
// returns 0

"Red Dragon".indexOf("RedScale");
// returns -1

"Red Dragon".startsWith("Red");
// returns true

"Red Dragon".endsWith("Dragon");
// returns true
```

### String Decomposition

```javascript
var test1 = "chicken,noodle,soup,broth";
test1.split(",");
// ["chicken", "noodle", "soup", "broth"]
```

### String Replace

- Regular Expressions
- Basic Regex
- Commonly Used Regexes
- Encoding
- Base64 Encoding
- String Shortening
- Encryption
- RSA Encryption
