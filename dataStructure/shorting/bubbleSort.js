function bubbleSort(arr) {
  const n = arr.length;
  for (let i = 0; i < n - 1; i++) {
    for (let j = 0; j < n - 1 - i; j++) {
      if (arr[j] > arr[j + 1]) {
        // Swap elements
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
      }
    }
  }
  return arr;
}

// Example usage:
const unsortedArray = [64, 34, 25, 12, 22, 11, 90];
console.log("Original array:", unsortedArray);

const sortedArray = bubbleSort(unsortedArray);
console.log("Sorted array:", sortedArray); // [11, 12, 22, 25, 34, 64, 90]

const anotherArray = [5, 1, 4, 2, 8];
console.log("Original array:", anotherArray);
console.log("Sorted array:", bubbleSort(anotherArray)); // [1, 2, 4, 5, 8]
