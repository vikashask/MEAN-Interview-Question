## Constants

## Scoping

    Block-Scoped Variables
    Block-Scoped Functions

## Arrow Functions

    Expression Bodies
    Statement Bodies
    Lexical this

## Extended Parameter Handling

    Default Parameter Values
    - Rest Parameter : The rest parameter syntax allows a function to accept an indefinite number of arguments as an array. It gathers all remaining arguments passed to a function into a single array.

        var myName = ["vikash" , "jay" , "raju"] ;
        const [firstName , ...familyName] = myName ;
        console.log(familyName); // [ "jay" , "raju"] ;

        function myData(...args){
        console.log(args) ; // ["vikash",24,"Front-End Developer"]
        }
        // myData("vikash",24,"Front-End Developer") ;
    - Spread Operator : It’s the opposite to rest parameter , where rest parameter collects items into an array, the spread operator unpacks
        the collected elements into single elements.
        var myName = ["vikash" , "jay" , "raju"];
        var newArr = [...myName ,"FrontEnd" , 24];
        console.log(newArr) ; // ["vikash" , "jay" , "raju" , "FrontEnd" , 24 ] ;

## Template Literals

    String Interpolation
    Custom Interpolation
    Raw String Access

## Extended Literals

    Binary & Octal Literal
    Unicode String & RegExp Literal

## Enhanced Regular Expression

    Regular Expression Sticky Matching

## Enhanced Object Properties

    Property Shorthand
    Computed Property Names
    Method Properties

## Promises

[Promises](https://www.geeksforgeeks.org/javascript-promises/)
A Promise has four states:
fulfilled: Action related to the promise succeeded
rejected: Action related to the promise failed
pending: Promise is still pending i.e. not fulfilled or rejected yet
settled: Promise has fulfilled or rejected

## Destructuring

## Symbols

## JavaScript Modules and Using npm

## Classes

## Generators

## Sets and WeakSets

## Map and Weak Map

## Async + Await Flow Control

[Async Await example](https://www.geeksforgeeks.org/async-await-function-in-javascript/)
It operates asynchronously via the event-loop. Async functions will always return a value

const getData = async() =>{
let data = "hello world";
return data
}
getData.then(da=>{
console.log("---data",da)
})
o/p
Hello world
const awaitExample = async () =>{
let a = await "hello world";
console.log(a)
}
console.log(1)
awaitExample()
console.log(1)
o/p = 1
2
hello world
