//1. what will be outout
var a = 1;
function b() {
    var a = 2;
    
    function c() {
      console.log(a)
    }
    
    return function() {
       var a = 3;
       c()
    }
}

var func = b();

// o/p 2
