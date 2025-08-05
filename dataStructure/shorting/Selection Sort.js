/*
Selection sort is a simple sorting algorithm. This sorting algorithm is an in-place comparison-based sorting algorithm.
In this algorithm, the array is divided into two parts: a sorted part and an unsorted part.
The algorithm repeatedly finds the minimum element from the unsorted part and puts it at the beginning of the unsorted part (which is the end of the sorted part).

Algorithm:
1. Initialize `min_idx` to the first element of the unsorted array.
2. Iterate through the unsorted array to find the minimum element.
3. If a smaller element is found, update `min_idx`.
4. After iterating through the unsorted array, swap the minimum element with the first element of the unsorted array.
5. Move the boundary of the sorted part one element to the right.
6. Repeat steps 1-5 until the entire array is sorted.
*/

function selectionSort(arr) {
  const n = arr.length;
  for (let i = 0; i < n - 1; i++) {
    let min_idx = i;
    for (let j = i + 1; j < n; j++) {
      if (arr[j] < arr[min_idx]) {
        min_idx = j;
      }
    }
    // Swap the found minimum element with the first element
    [arr[i], arr[min_idx]] = [arr[min_idx], arr[i]];
  }
  return arr;
}

// Example usage:
const unsortedArray = [64, 25, 12, 22, 11];
console.log("Original array:", unsortedArray);

const sortedArray = selectionSort(unsortedArray);
console.log("Sorted array:", sortedArray); // [11, 12, 22, 25, 64]

const anotherArray = [5, 1, 4, 2, 8];
console.log("Original array:", anotherArray);
console.log("Sorted array:", selectionSort(anotherArray)); // [1, 2, 4, 5, 8]
