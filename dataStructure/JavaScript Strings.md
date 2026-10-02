# JavaScript strings — immutable sequence, tricky characters

**Mental model:** JS strings are immutable sequences of **UTF-16 code units**. `s[i]`/`charAt(i)` read a code unit; `.length` counts code units, not necessarily Unicode characters a user sees. Operations that “change” a string return a new one.

```js
const s = "cat";
s[0]; // 'c'
s.includes("at"); // true
s.indexOf("dog"); // -1
s.startsWith("ca"); // true
s.slice(1); // 'at'
s.replace("c", "b"); // 'bat'; s stays 'cat'
"red,blue".split(","); // ['red', 'blue']
```

| Need                      | Tool                                | Cost intuition                                                        |
| ------------------------- | ----------------------------------- | --------------------------------------------------------------------- |
| Read code unit at index   | `s[i]`, `charAt(i)`                 | `O(1)` indexing model                                                 |
| Scan for pattern          | `includes`, `indexOf`               | depends on input/pattern and algorithm; don't assert universal `O(n)` |
| Split / map / join        | `split`, `Array.from`, `join`       | allocates new storage                                                 |
| Build from many fragments | `parts.push(...)`; `parts.join('')` | avoids repeatedly constructing intermediate strings                   |
| Frequency count           | `Map`                               | `O(n)` expected over iterated units/code points                       |

**Unicode trap:** `'😀'.length === 2` but `[...'😀'].length === 1`. Even spreading into code points may split what people perceive as one grapheme (e.g., letter + combining accent). For user-visible characters use `Intl.Segmenter` with `granularity: 'grapheme'` when available. Clarify whether interview input is ASCII, code points or graphemes before reversing/palindrome logic.

**Comparison:** JS relational string comparison is lexicographic by UTF-16 code units, not human locale order. Use `localeCompare` or `Intl.Collator` when locale-sensitive sorting is actually required.

**Interview patterns:** two pointers for palindrome (state normalization rules), `Map` for anagram/frequency, sliding window for longest substring without repeats, trie for large prefix sets. If you only need to search a few strings, a trie adds unnecessary overhead.

**Boundary:** Base64 is an _encoding_, not encryption; passwords need an appropriate password-hashing scheme, not a string transformation. This topic is about data representation, not cryptography.

**Recall:** What does `.length` count? Is `replace` in-place? Why can `s.split('').reverse().join('')` mishandle emoji?
