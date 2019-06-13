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
//2. what will be output
function add(a,b){
    var ddd = function (b){return a+b;};
    if(typeof b =='undefined'){
        return ddd;
    }else{
        return ddd(b);
    }
}

add(2)(3) // 5
add(2,3) // 5