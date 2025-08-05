## Find all pairs in an array whose sum is equal to a specific target.

This is a classic problem that can be solved efficiently using a hash set (or a hash map).

**Algorithm:**

1.  Create an empty hash set to store the numbers we have seen so far.
2.  Iterate through the array.
3.  For each number, calculate the `complement` (i.e., `target - current_number`).
4.  Check if the `complement` exists in the hash set. If it does, we have found a pair.
5.  Add the current number to the hash set.

**Time Complexity:** O(n) because we iterate through the array once.
**Space Complexity:** O(n) to store the numbers in the hash set.

```javascript
function findPairs(arr, target) {
  const seen = new Set();
  const pairs = [];
  for (const num of arr) {
    const complement = target - num;
    if (seen.has(complement)) {
      pairs.push([complement, num]);
    }
    seen.add(num);
  }
  return pairs;
}
```

---

## Find the smallest/largest kth element in an array (QuickSelect).

QuickSelect is an algorithm to find the kth smallest (or largest) element in an unsorted array. It is related to the QuickSort algorithm.

**Algorithm:**

1.  Choose a pivot element from the array.
2.  Partition the array around the pivot, so that elements smaller than the pivot are on its left and elements larger are on its right.
3.  The pivot is now in its final sorted position. Let's say its index is `p`.
4.  If `p` is equal to `k-1`, then the pivot is the kth smallest element.
5.  If `p` is greater than `k-1`, then the kth smallest element must be in the left subarray. Recursively apply the algorithm to the left subarray.
6.  If `p` is less than `k-1`, then the kth smallest element must be in the right subarray. Recursively apply the algorithm to the right subarray.

**Time Complexity:**
*   **Average Case:** O(n)
*   **Worst Case:** O(n^2) (if the pivot selection is consistently bad)

```javascript
// (Implementation of QuickSelect would be here)
```

---

## Product of array except self, without using division.

**Algorithm:**

1.  Create a `result` array of the same size as the input array, initialized with 1s.
2.  Create a `prefix` variable, initialized to 1.
3.  Iterate through the input array from left to right. For each element, set `result[i] = prefix`, and then update `prefix` by multiplying it with the current element.
4.  Create a `postfix` variable, initialized to 1.
5.  Iterate through the input array from right to left. For each element, multiply `result[i]` by `postfix`, and then update `postfix` by multiplying it with the current element.

**Time Complexity:** O(n)
**Space Complexity:** O(n) (for the result array)

```javascript
function productExceptSelf(nums) {
  const n = nums.length;
  const result = new Array(n).fill(1);
  let prefix = 1;
  for (let i = 0; i < n; i++) {
    result[i] = prefix;
    prefix *= nums[i];
  }
  let postfix = 1;
  for (let i = n - 1; i >= 0; i--) {
    result[i] *= postfix;
    postfix *= nums[i];
  }
  return result;
}
```

---

## Find the longest consecutive sequence in an unsorted array.

**Algorithm:**

1.  Create a hash set of all the numbers in the array for O(1) lookups.
2.  Initialize a `maxLength` variable to 0.
3.  Iterate through the array. For each number:
    *   Check if it's the start of a sequence (i.e., `number - 1` is not in the hash set).
    *   If it is the start of a sequence, start counting the length of the sequence by checking for `number + 1`, `number + 2`, and so on in the hash set.
    *   Update `maxLength` if the current sequence is longer.

**Time Complexity:** O(n)
**Space Complexity:** O(n)

```javascript
function longestConsecutive(nums) {
  const numSet = new Set(nums);
  let maxLength = 0;
  for (const num of numSet) {
    if (!numSet.has(num - 1)) {
      let currentNum = num;
      let currentLength = 1;
      while (numSet.has(currentNum + 1)) {
        currentNum++;
        currentLength++;
      }
      maxLength = Math.max(maxLength, currentLength);
    }
  }
  return maxLength;
}
```

---

## Find the majority element in an array (Boyer-Moore Voting Algorithm).

The Boyer-Moore Voting Algorithm is an efficient way to find the majority element (the element that appears more than n/2 times).

**Algorithm:**

1.  Initialize a `candidate` and a `count` to 0.
2.  Iterate through the array.
    *   If `count` is 0, set the `candidate` to the current element.
    *   If the current element is the same as the `candidate`, increment `count`. Otherwise, decrement `count`.
3.  The `candidate` will be the majority element.

**Time Complexity:** O(n)
**Space Complexity:** O(1)

```javascript
function majorityElement(nums) {
  let candidate = null;
  let count = 0;
  for (const num of nums) {
    if (count === 0) {
      candidate = num;
    }
    count += (num === candidate) ? 1 : -1;
  }
  return candidate;
}
```

---

## Search in a rotated sorted array.

This can be solved with a modified binary search.

**Algorithm:**

1.  Perform a binary search.
2.  In each step, determine which half of the array is sorted.
3.  Check if the target is within the sorted half. If it is, search in that half. Otherwise, search in the other half.

**Time Complexity:** O(log n)
**Space Complexity:** O(1)

```javascript
// (Implementation of search in rotated sorted array would be here)
```

---

## Implement an algorithm to solve the Trapping Rain Water problem.

This problem can be solved using a two-pointer approach.

**Algorithm:**

1.  Initialize `left` and `right` pointers at the beginning and end of the array, respectively.
2.  Initialize `leftMax` and `rightMax` to 0.
3.  Initialize `water` to 0.
4.  While `left` is less than `right`:
    *   If `height[left]` is less than `height[right]`:
        *   If `height[left]` is greater than or equal to `leftMax`, update `leftMax`.
        *   Otherwise, add `leftMax - height[left]` to `water`.
        *   Increment `left`.
    *   Else:
        *   If `height[right]` is greater than or equal to `rightMax`, update `rightMax`.
        *   Otherwise, add `rightMax - height[right]` to `water`.
        *   Decrement `right`.

**Time Complexity:** O(n)
**Space Complexity:** O(1)

```javascript
// (Implementation of trapping rain water would be here)
```

---

## Find the median of two sorted arrays.

This is a challenging problem that can be solved with a binary search approach on the smaller of the two arrays.

**Algorithm:**

The goal is to partition both arrays into two halves such that:

1.  The number of elements in the left halves is equal to the number of elements in the right halves.
2.  The maximum element in the left halves is less than or equal to the minimum element in the right halves.

Once we find such a partition, the median can be calculated from the maximum of the left halves and the minimum of the right halves.

**Time Complexity:** O(log(min(m, n))) where m and n are the lengths of the arrays.
**Space Complexity:** O(1)

```javascript
// (Implementation of median of two sorted arrays would be here)
```

---

## Maximum product subarray.

This can be solved by keeping track of the maximum and minimum product seen so far.

**Algorithm:**

1.  Initialize `maxProduct`, `minProduct`, and `result` to the first element of the array.
2.  Iterate through the array from the second element.
3.  For each element, calculate the new `maxProduct` and `minProduct`. The new `maxProduct` is the maximum of the current element, `maxProduct * current_element`, and `minProduct * current_element`. The new `minProduct` is the minimum of the same three values.
4.  Update the overall `result` with the `maxProduct`.

**Time Complexity:** O(n)
**Space Complexity:** O(1)

```javascript
// (Implementation of maximum product subarray would be here)
```