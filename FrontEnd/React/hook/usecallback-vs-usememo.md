### Comparing `useCallback` and `useMemo` in React

Both `useCallback` and `useMemo` are React hooks for optimization, helping prevent unnecessary re-renders or computations by providing **referential equality** between renders. They use dependencies to decide when to recompute.

#### Key Differences

- **`useMemo`**: Memoizes a **value** (the result of a computation). It runs the function and caches the returned value.
- **`useCallback`**: Memoizes a **function**. It returns the same function reference unless dependencies change.

| Aspect           | `useMemo`                                   | `useCallback`                            |
| ---------------- | ------------------------------------------- | ---------------------------------------- |
| **Returns**      | A memoized value                            | A memoized function                      |
| **Use Case**     | Expensive calculations or derived values    | Passing functions to child components    |
| **Performance**  | Prevents re-computation of values           | Prevents re-creation of functions        |
| **Dependencies** | Array of values that affect the computation | Array of values that affect the function |

#### Example: `useMemo` (Memoizing a Computed Value)

```javascript
import React, { useMemo } from "react";

function ExpensiveComponent({ numbers }) {
  // Memoize the sum to avoid recalculating on every render
  const sum = useMemo(() => {
    console.log("Calculating sum...");
    return numbers.reduce((acc, num) => acc + num, 0);
  }, [numbers]); // Only recalculates if 'numbers' changes

  return <div>Sum: {sum}</div>;
}
```

- **Why?** If `numbers` doesn't change, `sum` isn't recalculated, saving CPU.

#### Example: `useCallback` (Memoizing a Function)

```javascript
import React, { useCallback, useState } from "react";

function ParentComponent() {
  const [count, setCount] = useState(0);

  // Memoize the increment function to prevent child re-renders
  const increment = useCallback(() => {
    setCount((c) => c + 1);
  }, []); // Empty deps: function never changes

  return (
    <div>
      <ChildComponent onIncrement={increment} />
      <p>Count: {count}</p>
    </div>
  );
}

function ChildComponent({ onIncrement }) {
  console.log("Child rendered");
  return <button onClick={onIncrement}>Increment</button>;
}
```

- **Why?** Without `useCallback`, `increment` is recreated on every render, causing `ChildComponent` to re-render unnecessarily (even with `React.memo`).

#### When to Use

- Use **`useMemo`** for expensive computations (e.g., filtering lists, API data processing).
- Use **`useCallback`** for functions passed as props to prevent child re-renders.
- **Overuse Warning**: Only use when profiling shows performance issues; they add complexity.

For more details, check the [React docs](https://react.dev/reference/react/useMemo) and [useCallback](https://react.dev/reference/react/useCallback).
