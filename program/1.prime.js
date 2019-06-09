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
