function convertFirstLetter(string){
    return string.charAt(0).toUpperCase()+string.slice(1);

    // By using regular expression
    // return string.replace(/^./,string[0].toUpperCase)
}

const convertedString = convertFirstLetter("welcome to india");
console.log("convertedString - ", convertedString)
