// factorial program
function factorial(number) {
    let factorial = 1;
    for (let i = 1; i <= number; i++) {
        factorial = factorial * i;
    }
    return `factorial of ${number} is ${factorial} `;
}

console.log(factorial(5));

