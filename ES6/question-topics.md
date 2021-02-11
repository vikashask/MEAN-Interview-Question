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
    - Rest Parameter : It is a collection of all remaining elements into an array
        var myName = ["vikash" , "jay" , "raju"] ;
        const [firstName , ...familyName] = myName ;
        console.log(familyName); // [ "jay" , "raju"] ;

        function myData(...args){
        console.log(args) ; // ["vikash",24,"Front-End Developer"]
        }
        myData("vikash",24,"Front-End Developer") ;
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

## Destructuring

## Symbols

## JavaScript Modules and Using npm

## Classes

## Generators

## Sets and WeakSets

## Map and Weak Map

## Async + Await Flow Control
