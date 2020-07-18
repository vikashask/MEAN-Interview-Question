let you use state and other React features without writing a class.
📌 State Hook
import React, { useState } from 'react';
function Example() {
  // Declare a new state variable, which we'll call "count"
  const [count, setCount] = useState(0);
  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
📌 correct way to set state
📌      <button onClick={() => setCount(prevCount => prevCount + 1)}>
📌       Click me
📌    </button>
    </div>
  );
}
