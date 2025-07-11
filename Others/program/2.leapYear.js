function checkLeap (inputYear){
    if((inputYear % 400 === 0) || (inputYear % 4 === 0) || (inputYear % 100 === 0) ){
        return `${inputYear} is leap year`;
    }else{
        return `${inputYear} is not leap year `;
    }
}

let isLeapYear = checkLeap(1992);
console.log(isLeapYear);
