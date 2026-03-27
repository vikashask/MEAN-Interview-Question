### JavaScript: Difference between .forEach() and .map()
`forEach:` This iterates over a list and applies some operation with side effects to each list member `and does not return anything`.

`map:` returns another list of the same size with the transformed members, It does not mutate the array on which it is called


### for loop vs forEach method
1. forEach keeps the variable’s scope to the block
    const num = 4;
    const arr = [0, 1, 2];

    arr.forEach(num => {
    console.log(num);
    });

    // Result:
    // 0
    // 1
    // 2
    console.log(num);

    // Result:
    // 4
2. Lower chance of accidental errors with forEach

3. forEach is easier to read
4. You can break out of a for loop earlier
    for (let i = 0; i < foodArray.length; i++) {
    if (foodArray[i].name === 'Pizza') {
        console.log('I LOVE PIZZA');
        break;
    }
    }


### Difference for..in and for..of:
- for..in iterates over all enumerable property keys of an object
- for..of iterates over the values of an iterable object. Examples of iterable objects are arrays, strings, and NodeLists.

let arr = ['vik', 'jay', 'rohit'];

arr.addedProp = 'arrProp';

// elKey are the property keys
for (let elKey in arr) {
  console.log(elKey);   // 0,1,2
}

// elValue are the property values
for (let elValue of arr) {
  console.log(elValue)  //  'vik', 'jay', 'rohit'
}