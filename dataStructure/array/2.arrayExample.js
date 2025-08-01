// 1. need to reverse the array
let array = [1, 2, 3, 4, 5];
let reverseArr = [];
for (let i = 0; i < array.length; i++) {
  reverseArr[array.length - 1 - i] = array[i];
}
console.log("🚀 ~ reverseArr:", reverseArr);

// 2. sort the array in ascending order
let array2 = [5, 3, 8, 1, 2];
let sortedArr = [];
for (let i = 0; i < array2.length; i++) {
  let minIndex = i;
  for (let j = i + 1; j < array2.length; j++) {
    if (array2[j] < array2[minIndex]) {
      minIndex = j;
    }
  }
  sortedArr[i] = array2[minIndex];
  array2[minIndex] = array2[i];
}
console.log("🚀 ~ sortedArr:", sortedArr);

// 3. remove duplicates from the array
let array3 = [1, 2, 2, 3, 4, 4, 5];
let uniqueArr = [];
for (let i = 0; i < array3.length; i++) {
  if (!uniqueArr.includes(array3[i])) {
    uniqueArr.push(array3[i]);
  }
}
console.log("🚀 ~ uniqueArr:", uniqueArr);

// 3. remove duplicates from the array using core data structure
let array4 = [1, 2, 2, 3, 4, 4, 5];
for (let i = 0; i < array4.length; i++) {
  for (let j = i + 1; j < array4.length; j++) {
    if (array4[i] === array4[j]) {
      array4.splice(j, 1);
      j--; // Adjust index after removal
    }
  }
}
console.log("🚀 ~ array4 after removing duplicates:", array4);

// 4. fine the kth largest element in the array
let array5 = [3, 2, 1, 5, 6, 4];
let k = 2; // Find the 2nd largest element
let kthLargest = array5.sort((a, b) => b - a)[k - 1];
console.log("🚀 ~ kthLargest:", kthLargest);

//5. find the kth smallest element in the array
let array6 = [3, 2, 1, 5, 6, 4];
let l = 2; // Find the 2nd smallest element
for (let i = 0; i < k; i++) {
  let minIndex = i;
  for (let j = i + 1; j < array6.length; j++) {
    if (array6[j] < array6[minIndex]) {
      minIndex = j;
    }
  }
  // Swap the found minimum element with the first element
  [array6[i], array6[minIndex]] = [array6[minIndex], array6[i]];
}
console.log("🚀 ~ kth smallest element:", array6[l - 1]);

// 6. find the intersection of two arrays
let array7 = [1, 2, 3, 4, 5];
let array8 = [4, 5, 6, 7, 8];
let intersection = [];
for (let i = 0; i < array7.length; i++) {
  for (let j = 0; j < array8.length; j++) {
    if (array7[i] === array8[j]) {
      intersection.push(array7[i]);
    }
  }
}
console.log("🚀 ~ intersection:", intersection);

// 7. push element to the end of the array
let array9 = [1, 2, 3];
let elementToAdd = 4;
for (let i = 0; i < array9.length; i++) {
  if (i === array9.length - 1) {
    array9[i + 1] = elementToAdd; // Add element at the end
  }
}
console.log("🚀 ~ array9 after adding element:", array9);
