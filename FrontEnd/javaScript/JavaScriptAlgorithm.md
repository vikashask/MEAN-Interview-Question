# JavaScript Algorithms

## Array Algorithms

### 1. Finding Maximum/Minimum
```javascript
// Finding max in array
const findMax = arr => Math.max(...arr);

// Finding min in array
const findMin = arr => Math.min(...arr);

// Custom implementation
function findMaxCustom(arr) {
    return arr.reduce((max, curr) => curr > max ? curr : max, arr[0]);
}
```

### 2. Array Search Algorithms

#### Linear Search
```javascript
function linearSearch(arr, target) {
    for (let i = 0; i < arr.length; i++) {
        if (arr[i] === target) return i;
    }
    return -1;
}
```

#### Binary Search (Sorted Arrays)
```javascript
function binarySearch(arr, target) {
    let left = 0;
    let right = arr.length - 1;
    
    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        
        if (arr[mid] === target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    
    return -1;
}
```

### 3. Sorting Algorithms

#### Bubble Sort
```javascript
function bubbleSort(arr) {
    const n = arr.length;
    
    for (let i = 0; i < n - 1; i++) {
        for (let j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
            }
        }
    }
    
    return arr;
}
```

#### Quick Sort
```javascript
function quickSort(arr) {
    if (arr.length <= 1) return arr;
    
    const pivot = arr[arr.length - 1];
    const left = [];
    const right = [];
    
    for (let i = 0; i < arr.length - 1; i++) {
        if (arr[i] < pivot) left.push(arr[i]);
        else right.push(arr[i]);
    }
    
    return [...quickSort(left), pivot, ...quickSort(right)];
}
```

#### Merge Sort
```javascript
function mergeSort(arr) {
    if (arr.length <= 1) return arr;
    
    const mid = Math.floor(arr.length / 2);
    const left = arr.slice(0, mid);
    const right = arr.slice(mid);
    
    return merge(mergeSort(left), mergeSort(right));
}

function merge(left, right) {
    const result = [];
    let leftIndex = 0;
    let rightIndex = 0;
    
    while (leftIndex < left.length && rightIndex < right.length) {
        if (left[leftIndex] < right[rightIndex]) {
            result.push(left[leftIndex]);
            leftIndex++;
        } else {
            result.push(right[rightIndex]);
            rightIndex++;
        }
    }
    
    return result
        .concat(left.slice(leftIndex))
        .concat(right.slice(rightIndex));
}
```

## String Algorithms

### 1. String Reversal
```javascript
// Using built-in methods
const reverse1 = str => str.split('').reverse().join('');

// Using loop
function reverse2(str) {
    let result = '';
    for (let char of str) {
        result = char + result;
    }
    return result;
}
```

### 2. Palindrome Check
```javascript
function isPalindrome(str) {
    str = str.toLowerCase().replace(/[^a-z0-9]/g, '');
    return str === str.split('').reverse().join('');
}
```

### 3. String Pattern Matching
```javascript
function findPattern(text, pattern) {
    const positions = [];
    let pos = text.indexOf(pattern);
    
    while (pos !== -1) {
        positions.push(pos);
        pos = text.indexOf(pattern, pos + 1);
    }
    
    return positions;
}
```

## Number Algorithms

### 1. Prime Numbers
```javascript
function isPrime(num) {
    if (num <= 1) return false;
    if (num <= 3) return true;
    
    if (num % 2 === 0 || num % 3 === 0) return false;
    
    for (let i = 5; i * i <= num; i += 6) {
        if (num % i === 0 || num % (i + 2) === 0) return false;
    }
    
    return true;
}

function generatePrimes(n) {
    const primes = [];
    let num = 2;
    
    while (primes.length < n) {
        if (isPrime(num)) primes.push(num);
        num++;
    }
    
    return primes;
}
```

### 2. Fibonacci Sequence
```javascript
// Iterative approach
function fibonacci(n) {
    if (n <= 1) return n;
    
    let prev = 0, curr = 1;
    
    for (let i = 2; i <= n; i++) {
        [prev, curr] = [curr, prev + curr];
    }
    
    return curr;
}

// Recursive approach (with memoization)
function fibonacciMemo(n, memo = {}) {
    if (n in memo) return memo[n];
    if (n <= 1) return n;
    
    memo[n] = fibonacciMemo(n - 1, memo) + fibonacciMemo(n - 2, memo);
    return memo[n];
}
```

## Algorithm Design Patterns

### 1. Two Pointer Technique
```javascript
function findPairWithSum(arr, target) {
    let left = 0;
    let right = arr.length - 1;
    
    while (left < right) {
        const sum = arr[left] + arr[right];
        
        if (sum === target) return [left, right];
        if (sum < target) left++;
        else right--;
    }
    
    return null;
}
```

### 2. Sliding Window
```javascript
function findMaxSubarraySum(arr, k) {
    let maxSum = 0;
    let windowSum = 0;
    
    for (let i = 0; i < k; i++) {
        windowSum += arr[i];
    }
    
    maxSum = windowSum;
    
    for (let i = k; i < arr.length; i++) {
        windowSum = windowSum - arr[i - k] + arr[i];
        maxSum = Math.max(maxSum, windowSum);
    }
    
    return maxSum;
}
```

### 3. Dynamic Programming
```javascript
// Memoization example: Climbing Stairs
function climbStairs(n, memo = {}) {
    if (n in memo) return memo[n];
    if (n <= 2) return n;
    
    memo[n] = climbStairs(n - 1, memo) + climbStairs(n - 2, memo);
    return memo[n];
}

// Tabulation example: Coin Change
function coinChange(coins, amount) {
    const dp = new Array(amount + 1).fill(Infinity);
    dp[0] = 0;
    
    for (let i = 1; i <= amount; i++) {
        for (const coin of coins) {
            if (coin <= i) {
                dp[i] = Math.min(dp[i], dp[i - coin] + 1);
            }
        }
    }
    
    return dp[amount] === Infinity ? -1 : dp[amount];
}
```

## Time Complexity Analysis

Common Time Complexities:
1. O(1) - Constant time
2. O(log n) - Logarithmic time (Binary Search)
3. O(n) - Linear time (Linear Search)
4. O(n log n) - Linearithmic time (Merge Sort, Quick Sort)
5. O(n²) - Quadratic time (Bubble Sort)
6. O(2ⁿ) - Exponential time (Recursive Fibonacci)

## Space Complexity Analysis

Common Space Complexities:
1. O(1) - Constant space (In-place algorithms)
2. O(n) - Linear space (Arrays, Objects)
3. O(log n) - Logarithmic space (Recursive Binary Search)
4. O(n²) - Quadratic space (2D arrays)

> Verify a prime number?
> Find all prime factors of a number?
> Get nth Fibonacci number?
> Find the greatest common divisor of two numbers?
> Remove duplicate members from an array?
> merge two sorted array?
> Swap two numbers without using a temp variable?
> Reverse a string in JavaScript?
> How would you reverse words in a sentence?
> Reverse words in place?
> Find the first non repeating char in a string?
> Remove duplicate characters from a sting?
> How will you verify a word as palindrome?
> Generate random between 5 to 7 by using defined function.
> Find missing number from unsorted array of integers.
> Get two numbers that equal to a given number?
> Find the largest sum of any two elements?
> Total number of zeros from 1 upto n?
> Check whether a given string is a substring of bigger string
> Get permutations of a string