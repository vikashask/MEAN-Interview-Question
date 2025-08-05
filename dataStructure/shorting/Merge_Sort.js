/*
Merge Sort is a divide and conquer algorithm. It divides the input array into two halves, calls itself for the two halves, and then merges the two sorted halves.
The merge() function is used for merging two halves.

Algorithm:
1. Divide the unsorted list into n sublists, each containing one element (a list of one element is considered sorted).
2. Repeatedly merge sublists to produce new sorted sublists until there is only one sublist remaining. This will be the sorted list.
*/

function mergeSort(arr) {
  const n = arr.length;

  // Base case: if the array has 0 or 1 element, it's already sorted
  if (n <= 1) {
    return arr;
  }

  // Divide the array into two halves
  const mid = Math.floor(n / 2);
  const leftHalf = arr.slice(0, mid);
  const rightHalf = arr.slice(mid);

  // Recursively sort both halves
  const sortedLeft = mergeSort(leftHalf);
  const sortedRight = mergeSort(rightHalf);

  // Merge the sorted halves
  let i = 0; // pointer for sortedLeft
  let j = 0; // pointer for sortedRight
  let k = 0; // pointer for merged array
  const mergedArr = [];

  while (i < sortedLeft.length && j < sortedRight.length) {
    if (sortedLeft[i] < sortedRight[j]) {
      mergedArr[k++] = sortedLeft[i++];
    } else {
      mergedArr[k++] = sortedRight[j++];
    }
  }

  // Copy remaining elements of sortedLeft (if any)
  while (i < sortedLeft.length) {
    mergedArr[k++] = sortedLeft[i++];
  }

  // Copy remaining elements of sortedRight (if any)
  while (j < sortedRight.length) {
    mergedArr[k++] = sortedRight[j++];
  }

  return mergedArr;
}

// Example usage:
const unsortedArray = [38, 27, 43, 3, 9, 82, 10];
console.log("Original array:", unsortedArray);

const sortedArray = mergeSort(unsortedArray);
console.log("Sorted array:", sortedArray); // [3, 9, 10, 27, 38, 43, 82]

const anotherArray = [5, 1, 4, 2, 8];
console.log("Original array:", anotherArray);
console.log("Sorted array:", mergeSort(anotherArray)); // [1, 2, 4, 5, 8]
