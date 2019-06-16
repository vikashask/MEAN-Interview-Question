
function reverseInt(n) {
    const reversed = n.toString().split('').reverse().join(''); // turn a number into a string, then turn it into an array to reverse. 
    return Math.sign(n) * parseInt(reversed); // Math.sign will return -1 as for negative number, 1 as for position number, 0 as for zero.
  }

console.log(reverseInt(123));
  
