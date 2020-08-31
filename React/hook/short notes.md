## let you use state and other React features without writing a class.

## 📌 State Hook
```
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
```

### Declaring multiple state variables
function ExampleWithManyStates() {
  // Declare multiple state variables!
  const [age, setAge] = useState(42);
  const [fruit, setFruit] = useState('banana');
  const [todos, setTodos] = useState([{ text: 'Learn Hooks' }]);
}

## ⚡️ Effect Hook
useEffect, adds the ability to perform side effects from a function component,It serves the same purpose as componentDidMount, componentDidUpdate, and componentWillUnmount in React classes. React runs the effects after every render — including the first render. 

## 🔌 Other Hooks
useContext lets you subscribe to React context without introducing nesting.
And useReducer lets you manage local state of complex components with a reducer:

Hooks don’t work inside classes. But you can use them instead of writing classes.

Tip: Use Multiple Effects to Separate Concerns

## 🔌 Hooks rules
✅ Call Hooks from React function components.
✅ Only call Hooks inside at the top level
✅ Call Hooks from custom Hooks

## 🔌 Custom Hooks
A custom Hook is a JavaScript function whose name starts with ”use” and that may call other Hooks. For example, useFriendStatus

import { useState, useEffect } from 'react';
function useFriendStatus(friendID) {
  const [isOnline, setIsOnline] = useState(null);
  useEffect(() => {
    function handleStatusChange(status) {
      setIsOnline(status.isOnline);
    }
    ChatAPI.subscribeToFriendStatus(friendID, handleStatusChange);
    return () => {
      ChatAPI.unsubscribeFromFriendStatus(friendID, handleStatusChange);
    };
  });
  return isOnline;
}

