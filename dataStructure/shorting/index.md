1. Comparison-Based Sorting Algorithms
   These algorithms sort elements by comparing them directly.

- **Bubble Sort:** A simple sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order. The pass through the list is repeated until the list is sorted.

  - **Time Complexity:** O(n<sup>2</sup>) in the average and worst cases, and O(n) in the best case.
  - **Space Complexity:** O(1)

- **Selection Sort:** An in-place comparison sorting algorithm. It has an O(n<sup>2</sup>) time complexity, which makes it inefficient on large lists, and generally performs worse than the similar insertion sort.

  - **Time Complexity:** O(n<sup>2</sup>) in all cases.
  - **Space Complexity:** O(1)

- **Insertion Sort:** A simple sorting algorithm that builds the final sorted array (or list) one item at a time. It is much less efficient on large lists than more advanced algorithms such as quicksort, heapsort, or merge sort.

  - **Time Complexity:** O(n<sup>2</sup>) in the average and worst cases, and O(n) in the best case.
  - **Space Complexity:** O(1)

- **Merge Sort:** An efficient, comparison-based, divide-and-conquer sorting algorithm. Most implementations produce a stable sort, which means that the order of equal elements is the same in the input and output.

  - **Time Complexity:** O(n log n) in all cases.
  - **Space Complexity:** O(n)

- **Quick Sort:** An efficient sorting algorithm. When implemented well, it can be about two or three times faster than its main competitors, merge sort and heapsort.

  - **Time Complexity:** O(n log n) on average, O(n<sup>2</sup>) in the worst case.
  - **Space Complexity:** O(log n) on average for the recursion stack.

- **Heap Sort:** A comparison-based sorting technique based on a Binary Heap data structure. It is similar to selection sort where we first find the maximum element and place the maximum element at the end.

  - **Time Complexity:** O(n log n) in all cases.
  - **Space Complexity:** O(1)

- **Shell Sort:** A generalization of insertion sort that allows exchange of far-off elements.

  - **Time Complexity:** Varies, but typically O(n log<sup>2</sup> n) or O(n<sup>3/2</sup>) in worst case, depending on gap sequence.
  - **Space Complexity:** O(1)

- **Comb Sort:** Improves on bubble sort by comparing elements farther apart before reducing the gap.

  - **Time Complexity:** O(n log n) on average, O(n<sup>2</sup>) in worst case.
  - **Space Complexity:** O(1)

- **Cycle Sort:** Arranges the elements into cycles and rotates them to their correct positions.

  - **Time Complexity:** O(n<sup>2</sup>) in all cases.
  - **Space Complexity:** O(1)

2. Non-Comparison (Linear Time) Sorting Algorithms
   These algorithms do not compare elements directly; instead, they exploit properties of the input.

- **Counting Sort:** Counts the number of elements less than each element to find its correct position (best for small integer ranges).

  - **Time Complexity:** O(n + k) where n is the number of elements and k is the range of input.
  - **Space Complexity:** O(k)

- **Radix Sort:** Sorts numbers digit by digit, from least significant to most significant digit (or vice versa).

  - **Time Complexity:** O(nk) where n is the number of elements and k is the number of digits in the largest number.
  - **Space Complexity:** O(n+k)

- **Bucket Sort:** Distributes elements into buckets, then sorts each bucket (can use another sort inside).

  - **Time Complexity:** O(n+k) on average, where k is the number of buckets. The worst-case time complexity is O(n<sup>2</sup>).
  - **Space Complexity:** O(n+k)

- **Pigeonhole Sort:** Similar to counting sort but used when the number of keys is nearly equal to the number of elements.

  - **Time Complexity:** O(n + range) where range is the difference between maximum and minimum values.
  - **Space Complexity:** O(range)

### Common Sorting Algorithms (JavaScript Implementations)

Below are JavaScript implementations for some of the common sorting algorithms, along with their time and space complexities.

- **Bubble Sort**

  ```javascript
  function bubbleSort(arr) {
    let n = arr.length;
    for (let i = 0; i < n - 1; i++) {
      for (let j = 0; j < n - i - 1; j++) {
        if (arr[j] > arr[j + 1]) {
          // swap arr[j+1] and arr[j]
          let temp = arr[j];
          arr[j] = arr[j + 1];
          arr[j + 1] = temp;
        }
      }
    }
    return arr;
  }
  ```

- **Selection Sort**

  ```javascript
  function selectionSort(arr) {
    let n = arr.length;
    for (let i = 0; i < n - 1; i++) {
      let min_idx = i;
      for (let j = i + 1; j < n; j++) {
        if (arr[j] < arr[min_idx]) {
          min_idx = j;
        }
      }
      // Swap the found minimum element with the first element
      let temp = arr[min_idx];
      arr[min_idx] = arr[i];
      arr[i] = temp;
    }
    return arr;
  }
  ```

- **Insertion Sort**

  ```javascript
  function insertionSort(arr) {
    let n = arr.length;
    for (let i = 1; i < n; i++) {
      let key = arr[i];
      let j = i - 1;
      while (j >= 0 && arr[j] > key) {
        arr[j + 1] = arr[j];
        j = j - 1;
      }
      arr[j + 1] = key;
    }
    return arr;
  }
  ```

- **Merge Sort**

  ```javascript
  function mergeSort(arr) {
    if (arr.length <= 1) {
      return arr;
    }

    const mid = Math.floor(arr.length / 2);
    const left = arr.slice(0, mid);
    const right = arr.slice(mid);

    return merge(mergeSort(left), mergeSort(right));
  }

  function merge(left, right) {
    let resultArray = [],
      leftIndex = 0,
      rightIndex = 0;

    while (leftIndex < left.length && rightIndex < right.length) {
      if (left[leftIndex] < right[rightIndex]) {
        resultArray.push(left[leftIndex]);
        leftIndex++;
      } else {
        resultArray.push(right[rightIndex]);
        rightIndex++;
      }
    }

    return resultArray
      .concat(left.slice(leftIndex))
      .concat(right.slice(rightIndex));
  }
  ```

- **Quick Sort**

  ```javascript
  function quickSort(arr, low, high) {
    if (low < high) {
      let pi = partition(arr, low, high);
      quickSort(arr, low, pi - 1);
      quickSort(arr, pi + 1, high);
    }
    return arr;
  }

  function partition(arr, low, high) {
    let pivot = arr[high];
    let i = low - 1;
    for (let j = low; j <= high - 1; j++) {
      if (arr[j] < pivot) {
        i++;
        [arr[i], arr[j]] = [arr[j], arr[i]]; // Swap elements
      }
    }
    [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]]; // Swap pivot to correct position
    return i + 1;
  }
  ```

- **Heap Sort**

  ```javascript
  function heapSort(arr) {
    let n = arr.length;

    for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
      heapify(arr, n, i);
    }

    for (let i = n - 1; i > 0; i--) {
      [arr[0], arr[i]] = [arr[i], arr[0]]; // Move current root to end
      heapify(arr, i, 0);
    }
    return arr;
  }

  function heapify(arr, n, i) {
    let largest = i;
    let l = 2 * i + 1;
    let r = 2 * i + 2;

    if (l < n && arr[l] > arr[largest]) {
      largest = l;
    }

    if (r < n && arr[r] > arr[largest]) {
      largest = r;
    }

    if (largest != i) {
      [arr[i], arr[largest]] = [arr[largest], arr[i]]; // Swap
      heapify(arr, n, largest);
    }
  }
  ```

- **Radix Sort**

  ```javascript
  function radixSort(arr) {
    const maxNum = Math.max(...arr);
    let digit = 1;
    while (digit <= maxNum) {
      let buckets = [...Array(10)].map(() => []);
      for (let num of arr) {
        buckets[Math.floor(num / digit) % 10].push(num);
      }
      arr = [].concat(...buckets);
      digit *= 10;
    }
    return arr;
  }
  ```

- **Bucket Sort**

  ```javascript
  function bucketSort(arr, bucketSize = 5) {
    if (arr.length === 0) {
      return arr;
    }

    const minValue = Math.min(...arr);
    const maxValue = Math.max(...arr);

    const bucketCount = Math.floor((maxValue - minValue) / bucketSize) + 1;
    const buckets = new Array(bucketCount);
    for (let i = 0; i < buckets.length; i++) {
      buckets[i] = [];
    }

    for (let i = 0; i < arr.length; i++) {
      const bucketIndex = Math.floor((arr[i] - minValue) / bucketSize);
      buckets[bucketIndex].push(arr[i]);
    }

    let sortedArray = [];
    for (let i = 0; i < buckets.length; i++) {
      insertionSort(buckets[i]); // Using insertion sort for smaller buckets
      for (let j = 0; j < buckets[i].length; j++) {
        sortedArray.push(buckets[i][j]);
      }
    }

    return sortedArray;
  }
  ```
