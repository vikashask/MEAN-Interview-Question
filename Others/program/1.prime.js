// to check prime no
function check_prime(numberTocheck)
{
   for ( var c = 2 ; c <= numberTocheck - 1 ; c++ )
   {
      if ( numberTocheck %c === 0 )
     return 0;
   }
   if ( c == numberTocheck )
      return 1;
}

let result = check_prime(5);
let finalOutput = result === 0 ? 'Not Prime' : 'Prime Number';
console.log(finalOutput);

// get list of prime no
function listOfPrimeNumber(no) {
    let i=3
    for (var count = 2; count <= no;) {
        // console.log(count);
        
        for (var j = 2; j <= i-1; j++) {
            // console.log(i%j);
            
            if(i%j===0){
                break;
            }
            if(j===i){
                console.log(i);
                count++;
            }
            i++
        }
        count++;
    }
    // return 0
}

listOfPrimeNumber(3);