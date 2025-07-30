/**
 * Checks if a number is a prime number.
 * This version is more efficient and handles edge cases.
 * @param {number} num The number to check.
 * @returns {boolean} True if the number is prime, otherwise false.
 */
function isPrime(num) {
  // Prime numbers must be greater than 1.
  if (num <= 1) {
    return false;
  }

  // Check for divisors from 2 up to the square root of the number.
  // If we find a divisor, the number is not prime.
  for (let i = 2; i * i <= num; i++) {
    if (num % i === 0) {
      return false;
    }
  }

  // If no divisors were found, the number is prime.
  return true;
}

let numberToCheck = 7;
let finalOutput = isPrime(numberToCheck)
  ? `${numberToCheck} is a Prime Number`
  : `${numberToCheck} is Not a Prime Number`;
console.log(finalOutput);

/**
 * Generates a list of prime numbers up to a given limit.
 * @param {number} limit The upper bound to generate primes up to.
 * @returns {number[]} An array of prime numbers.
 */
function getPrimesUpTo(limit) {
  const primes = [];
  for (let i = 2; i <= limit; i++) {
    if (isPrime(i)) {
      primes.push(i);
    }
  }
  return primes;
}

console.log("Prime numbers up to 20:", getPrimesUpTo(20));
