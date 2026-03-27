- Manage more complicated state than you would want to manage with useState

- useReducer returns an array of 2 elements, similar to the useState hook. The first is the current state, and the second is a dispatch function.

  const [sum, dispatch] = useReducer((state, action) => {
  return state + action;
  }, 0);

  <button onClick={() => dispatch(1)}>
  Add 1
  </button>

- codesandbox: link https://codesandbox.io/s/react-test-h3d7f?file=/src/component/ShopingListReducer.js

```jsx
import React, { useReducer, useRef } from "react";

const ShopingList = () => {
  const inputRef = useRef();

  const [items, dispatch] = useReducer((state, action) => {
    switch (action.type) {
      case "add":
        return [
          ...state,
          {
            id: state.length,
            name: action.name,
          },
        ];
        break;

      case "remove":
        return state.filter((_, index) => index !== action.index);
      default:
        return state;
    }
  }, []);
  const handelSubmit = (e) => {
    e.preventDefault();
    dispatch({
      type: "add",
      name: inputRef.current.value,
    });
    inputRef.current.value = "";
  };
  return (
    <>
      <form onSubmit={handelSubmit}>
        <input ref={inputRef} />
      </form>
      <ul>
        {items.map((item, index) => (
          <li>
            {item.name}
            <button onClick={() => dispatch({ type: "remove", index })}>
              X
            </button>
          </li>
        ))}
      </ul>
    </>
  );
};

export default ShopingList;
```

- Another example

```jsx
import { useReducer } from "react";

function reducer(state, action) {
  switch (action.type) {
    case "increment":
      return { count: state.count + 1 };
    case "decrement":
      return { count: state.count - 1 };
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: "increment" })}>+</button>
      <button onClick={() => dispatch({ type: "decrement" })}>-</button>
    </div>
  );
}
```
