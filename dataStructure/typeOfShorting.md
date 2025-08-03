### Common Sorting Algorithms

Here are some of the most common types of sorting algorithms in Data Structures:

*   **Bubble Sort:** A simple sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order. The pass through the list is repeated until the list is sorted.

    *   **Time Complexity:** O(n<sup>2</sup>) in the average and worst cases, and O(n) in the best case.
    *   **Space Complexity:** O(1)

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

*   **Selection Sort:** An in-place comparison sorting algorithm. It has an O(n<sup>2</sup>) time complexity, which makes it inefficient on large lists, and generally performs worse than the similar insertion sort.

    *   **Time Complexity:** O(n<sup>2</sup>) in all cases.
    *   **Space Complexity:** O(1)

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

*   **Insertion Sort:** A simple sorting algorithm that builds the final sorted array (or list) one item at a time. It is much less efficient on large lists than more advanced algorithms such as quicksort, heapsort, or merge sort.

    *   **Time Complexity:** O(n<sup>2</sup>) in the average and worst cases, and O(n) in the best case.
    *   **Space Complexity:** O(1)

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

*   **Merge Sort:** An efficient, comparison-based, divide-and-conquer sorting algorithm. Most implementations produce a stable sort, which means that the order of equal elements is the same in the input and output.

    *   **Time Complexity:** O(n log n) in all cases.
    *   **Space Complexity:** O(n)

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
      let resultArray = [], leftIndex = 0, rightIndex = 0;

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

*   **Quick Sort:** An efficient sorting algorithm. When implemented well, it can be about two or three times faster than its main competitors, merge sort and heapsort.

    *   **Time Complexity:** O(n log n) on average, O(n<sup>2</sup>) in the worst case.
    *   **Space Complexity:** O(log n) on average for the recursion stack.

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
      let i = (low - 1);
      for (let j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
          i++;
          [arr[i], arr[j]] = [arr[j], arr[i]]; // Swap elements
        }
      }
      [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]]; // Swap pivot to correct position
      return (i + 1);
    }
    ```

*   **Heap Sort:** A comparison-based sorting technique based on a Binary Heap data structure. It is similar to selection sort where we first find the maximum element and place the maximum element at the end.

    *   **Time Complexity:** O(n log n) in all cases.
    *   **Space Complexity:** O(1)

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

*   **Radix Sort:** A non-comparative sorting algorithm that sorts data with integer keys by grouping keys by the individual digits which share the same significant position and value.

    *   **Time Complexity:** O(nk) where n is the number of elements and k is the number of digits in the largest number.
    *   **Space Complexity:** O(n+k)

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

*   **Bucket Sort:** A comparison sort algorithm that operates on elements by distributing them into a number of buckets. Each bucket is then sorted individually, either using a different sorting algorithm, or by recursively applying the bucket sorting algorithm.

    *   **Time Complexity:** O(n+k) on average, where k is the number of buckets. The worst-case time complexity is O(n<sup>2</sup>).
    *   **Space Complexity:** O(n+k)

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