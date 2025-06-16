Example of use memo you will get here : https://github.com/vikashask/react-basic/blob/master/src/components/hook/useMemo/MainUseMemo.js
: https://reactjs.org/docs/hooks-reference.html#usememo

- useMemo is a hook used in the functional component of react that returns a memoized value
  const memoizedValue = useMemo(functionThatReturnsValue,arrayDepencies)
- You may rely on useMemo as a performance optimization, not as a semantic guarantee.


- Example 
```
import { useState, useMemo } from 'react';

function ExpensiveComponent({ number }) {
  const expensiveValue = useMemo(() => {
    console.log('Calculating...');
    return number * 1000;
  }, [number]);

  return <p>Expensive Value: {expensiveValue}</p>;
}
```