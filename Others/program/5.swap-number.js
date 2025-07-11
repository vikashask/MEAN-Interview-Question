function swap(no1,no2) {
    let t;
    t = no1;
    no1 = no2;
    no2 = t;
    return `no1 is ${no1} and no2 is ${no2}`;
}
console.log(swap(3,4));

// swap 2 no without 3rd variable
function swapWithout3rdVariable(no1,no2) {
    no1 = no1+no2;  // no1 = 7
    no2 = no1-no2;  // no2 = -1 
    no1 = no1-no2;  // no1 = 4
    return `no1 is ${no1} and no2 is ${no2}`;    
}

console.log(swapWithout3rdVariable(3,4));


