> Question: Explain the rules of hooks and what happens if they are violated.

Hint: Discuss the two main rules (only call hooks at the top level, only call hooks in React function components or custom hooks) and the potential bugs (e.g., stale closures) from misuse.

> Question: Write a custom hook to fetch data from an API with loading and error states.
Hint: Demonstrate use of useState, useEffect, and proper cleanup to avoid memory leaks.

> Question: How would you implement a useDebounce custom hook? Provide a code example.
Hint: Show how to debounce user input (e.g., for search) using useEffect and setTimeout, ensuring cleanup of timers.

Question: What are the differences between useEffect, useLayoutEffect, and useInsertionEffect? When would you use each?
Hint: Explain their timing in the render cycle (e.g., useLayoutEffect runs synchronously before painting) and use cases like DOM measurements or CSS transitions.