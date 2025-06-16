## React's useCallback Hook can be used to optimize the rendering behavior of your React function components

## Note: Don't mistake React's useCallback Hook with React's useMemo Hook. While useCallback is used to memoize functions, useMemo is used to memoize values.

## useCallback is used to memoize functions, React memo is used to wrap React components to prevent re-renderings.

! example here : https://www.robinwieruch.de/react-usecallback-hook
https://github.com/vikashask/react-basic/blob/master/src/components/hook/useCallback/example1/MainUseCallback1Com.js

- React.memo to turn it into a memoized component.
- This will force React to never re-render it, unless some of its properties change.
- In other words useMemo caches a computed value. This is useful when the computation requires significant resources and we don’t want to repeat it on every re-render, as in this example:

  const [c, setC] = useState(0);
  // This value will not be recomputed between re-renders
  // unless the value of c changes
  const sinOfC: number = useMemo(() => Math.sin(c) , [c])


- another example 
```
import { useCallback, useState } from 'react';

function ButtonComponent({ onClick }) {
  console.log('Button re-rendered');
  return <button onClick={onClick}>Click</button>;
}

function ParentComponent() {
  const [count, setCount] = useState(0);

  const handleClick = useCallback(() => {
    setCount(c => c + 1);
  }, []);

  return (
    <div>
      <p>Count: {count}</p>
      <ButtonComponent onClick={handleClick} />
    </div>
  );
}

```