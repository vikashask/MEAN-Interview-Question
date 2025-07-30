/**
 * Checks if a given year is a leap year based on the Gregorian calendar rules.
 * @param {number} year The year to check.
 * @returns {boolean} Returns true if the year is a leap year, otherwise false.
 */
function isLeapYear(year) {
  // A year is a leap year if it's divisible by 4,
  // except for century years (divisible by 100) which must also be divisible by 400.
  return (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
}

// --- Examples ---
const year1 = 2024; // Correctly identifies as a leap year.
console.log(`${year1} is ${isLeapYear(year1) ? "" : "not "}a leap year.`);

const year2 = 1900; // Correctly identifies as NOT a leap year.
console.log(`${year2} is ${isLeapYear(year2) ? "" : "not "}a leap year.`);

const year3 = 2000; // Correctly identifies as a leap year.
console.log(`${year3} is ${isLeapYear(year3) ? "" : "not "}a leap year.`);
