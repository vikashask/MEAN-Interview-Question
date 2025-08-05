/*
Quick Sort is a highly efficient, comparison-based sorting algorithm. It is a divide-and-conquer algorithm.
It works by selecting a 'pivot' element from the array and partitioning the other elements into two sub-arrays,
according to whether they are less than or greater than the pivot. The sub-arrays are then sorted recursively.

Algorithm:
1. Choose a pivot element from the array. (Common choices: first, last, middle, or random element).
2. Partitioning: Rearrange the array such that all elements less than the pivot come before it,
   and all elements greater than the pivot come after it. Elements equal to the pivot can go on either side.
   After this partitioning, the pivot is in its final sorted position.
3. Recursively apply the above steps to the sub-array of elements with smaller values and separately
   to the sub-array of elements with greater values.
4. The base case for the recursion is arrays of size 0 or 1, which are already sorted.
*/

function quickSort(arr) {
  // Base case: arrays with 0 or 1 element are already sorted
  if (arr.length <= 1) {
    return arr;
  }

  // Choose a pivot (here, we choose the last element)
  const pivot = arr[arr.length - 1];
  const left = [];
  const right = [];

  // Partition the array into two sub-arrays: left (elements < pivot) and right (elements >= pivot)
  // We iterate up to arr.length - 1 because the last element is the pivot itself.
  for (let i = 0; i < arr.length - 1; i++) {
    if (arr[i] < pivot) {
      left.push(arr[i]);
    } else {
      right.push(arr[i]);
    }
  }

  // Recursively sort the left and right sub-arrays and combine them with the pivot
  return [...quickSort(left), pivot, ...quickSort(right)];
}

// Example usage:
const unsortedArray = [10, 7, 8, 9, 1, 5];
console.log("Original array:", unsortedArray);

const sortedArray = quickSort(unsortedArray);
console.log("Sorted array:", sortedArray); // [1, 5, 7, 8, 9, 10]

const anotherArray = [3, 0, 2, 5, -1, 4];
console.log("Original array:", anotherArray);
console.log("Sorted array:", quickSort(anotherArray)); // [-1, 0, 2, 3, 4, 5]
