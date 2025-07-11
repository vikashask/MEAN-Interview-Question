# React.js Interview Questions and Answers

## What is React?
React is a free and open-source front-end JavaScript library developed by Facebook (Meta) for building user interfaces based on components. It's used for handling the view layer in web and mobile applications. React allows developers to create reusable UI components that manage their own state.

## Pros and Cons of React

### Pros:
- Virtual DOM for better performance
- Reusable components
- Unidirectional data flow
- Large ecosystem and community
- JSX makes code readable and maintainable
- Great developer tools
- SEO friendly

### Cons:
- Only handles UI layer, needs additional libraries for complete application
- JSX complexity for beginners
- Frequent updates and changes
- Documentation can be challenging due to rapid updates
- Complex initial learning curve

## How to create React application?
There are several ways to create a React application:

1. Using Create React App (CRA):
```bash
npx create-react-app my-app
cd my-app
npm start
```

2. Using Vite:
```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev
```

3. Using Next.js:
```bash
npx create-next-app@latest my-app
cd my-app
npm run dev
```

## What is Virtual DOM?
Virtual DOM is a lightweight copy of the actual DOM in memory. React uses it to improve performance by:
1. Creating a virtual representation of UI
2. When state changes, React creates a new Virtual DOM tree
3. Compares it with the previous Virtual DOM tree (diffing)
4. Updates only the changed elements in the real DOM
5. This process is called Reconciliation

## What is JSX?
JSX (JavaScript XML) is a syntax extension for JavaScript that allows you to write HTML-like code within JavaScript. Example:

```jsx
const element = (
  <div className="greeting">
    <h1>Hello, {name}!</h1>
  </div>
);
```

## Why do we use className and not class?
We use className instead of class in React because:
1. class is a reserved keyword in JavaScript
2. React uses camelCase naming convention for attributes
3. This helps avoid naming conflicts with JavaScript classes

## What are functional components and props?
Functional components are JavaScript functions that accept props and return React elements:

```jsx
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

// Usage
<Welcome name="John" />
```

Props are read-only inputs to components that allow passing data from parent to child components.

## What are class components, props and state?
Class components are ES6 classes that extend React.Component:

```jsx
class Welcome extends React.Component {
  constructor(props) {
    super(props);
    this.state = { count: 0 }; // State initialization
  }

  render() {
    return <h1>Hello, {this.props.name}</h1>;
  }
}
```

- Props: External inputs passed to the component
- State: Internal data managed by the component

## What are dumb vs smart components?
### Dumb Components (Presentational):
- Focus on UI presentation
- Don't manage state (usually)
- Receive data via props
- Highly reusable
- Example: buttons, cards, input fields

### Smart Components (Container):
- Focus on functionality
- Manage state and data
- Pass data to dumb components
- Handle business logic
- Example: forms, data fetching components

## What is a key index map?
Keys help React identify which items have changed, been added, or been removed in lists:

```jsx
const items = ['apple', 'banana', 'orange'];
return (
  <ul>
    {items.map((item, index) => (
      <li key={index}>{item}</li>
    ))}
  </ul>
);
```

Note: Using index as key is not recommended if list items can change, as it may cause performance issues and bugs.

## What is React.Fragment?
React.Fragment lets you group multiple children without adding extra nodes to the DOM:

```jsx
return (
  <React.Fragment>
    <ChildA />
    <ChildB />
  </React.Fragment>
);

// Shorthand syntax
return (
  <>
    <ChildA />
    <ChildB />
  </>
);
```

## What is conditional rendering in React?
Conditional rendering allows you to show different content based on conditions:

```jsx
// Using ternary operator
return condition ? <ComponentA /> : <ComponentB />;

// Using && operator
return condition && <Component />;

// Using if statements
if (condition) {
  return <ComponentA />;
}
return <ComponentB />;
```

## How to apply styles in React?
There are multiple ways to style React components:

1. Inline Styles:
```jsx
<div style={{ color: 'blue', fontSize: '16px' }}>
```

2. CSS Classes:
```jsx
import './styles.css';
<div className="my-class">
```

3. CSS Modules:
```jsx
import styles from './Button.module.css';
<button className={styles.button}>
```

4. Styled Components:
```jsx
const StyledButton = styled.button`
  color: blue;
  padding: 10px;
`;
```

## How parent child communication works in React?
1. Parent to Child: Using props
```jsx
// Parent
const Parent = () => {
  return <Child message="Hello" />;
};

// Child
const Child = (props) => {
  return <div>{props.message}</div>;
};
```

2. Child to Parent: Using callback functions
```jsx
// Parent
const Parent = () => {
  const handleClick = (data) => {
    console.log(data);
  };
  return <Child onAction={handleClick} />;
};

// Child
const Child = (props) => {
  return <button onClick={() => props.onAction('Hello')}>Click</button>;
};
```

## What is useState hook?
useState is a Hook that lets you add state to functional components:

```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

## What is useEffect hook?
useEffect handles side effects in functional components:

```jsx
import { useEffect, useState } from 'react';

function UserData() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Runs after every render
    fetchData().then(result => setData(result));

    return () => {
      // Cleanup function
      // Runs before component unmounts
    };
  }, []); // Empty dependency array = run once

  return <div>{/* render data */}</div>;
}
```

## What is useReducer hook?
useReducer manages complex state logic in components:

```jsx
import { useReducer } from 'react';

const reducer = (state, action) => {
  switch (action.type) {
    case 'INCREMENT':
      return { count: state.count + 1 };
    case 'DECREMENT':
      return { count: state.count - 1 };
    default:
      return state;
  }
};

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });

  return (
    <>
      Count: {state.count}
      <button onClick={() => dispatch({ type: 'INCREMENT' })}>+</button>
      <button onClick={() => dispatch({ type: 'DECREMENT' })}>-</button>
    </>
  );
}
```

## What is useContext hook?
useContext subscribes to React context without introducing nesting:

```jsx
const ThemeContext = React.createContext('light');

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <ThemedButton />
    </ThemeContext.Provider>
  );
}

function ThemedButton() {
  const theme = useContext(ThemeContext);
  return <button className={theme}>Themed Button</button>;
}
```

## What is useRef hook?
useRef creates a mutable reference that persists across renders:

```jsx
function TextInputWithFocusButton() {
  const inputEl = useRef(null);

  const onButtonClick = () => {
    inputEl.current.focus();
  };

  return (
    <>
      <input ref={inputEl} type="text" />
      <button onClick={onButtonClick}>Focus the input</button>
    </>
  );
}
```

## What is useMemo hook?
useMemo memoizes expensive computations:

```jsx
const memoizedValue = useMemo(() => {
  return computeExpensiveValue(a, b);
}, [a, b]);
```

## What is useCallback hook?
useCallback memoizes callbacks to prevent unnecessary renders:

```jsx
const memoizedCallback = useCallback(
  () => {
    doSomething(a, b);
  },
  [a, b],
);
```

## Custom Hook: useFetch
```jsx
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url);
        const json = await response.json();
        setData(json);
        setLoading(false);
      } catch (error) {
        setError(error);
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
}
```

## Custom Hook: useLocalStorage
```jsx
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      return initialValue;
    }
  });

  const setValue = value => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
}
```

## React.memo - Rendering Optimization
React.memo is a higher-order component that memoizes component renders:

```jsx
const MyComponent = React.memo(function MyComponent(props) {
  /* render using props */
});
```

## Best React File Structure
```
src/
├── components/         # Reusable components
│   ├── Button/
│   │   ├── Button.jsx
│   │   ├── Button.test.js
│   │   └── Button.css
├── pages/             # Page components
├── hooks/             # Custom hooks
├── context/           # React context
├── services/          # API calls
├── utils/             # Helper functions
├── assets/            # Images, fonts
└── styles/            # Global styles
```

## React Router
```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
```

## React Portals
Portals render children into a DOM node that exists outside the parent component's hierarchy:

```jsx
import ReactDOM from 'react-dom';

function Modal({ children }) {
  return ReactDOM.createPortal(
    children,
    document.getElementById('modal-root')
  );
}
```

## React Lazy and Suspense
```jsx
import React, { Suspense, lazy } from 'react';

const OtherComponent = lazy(() => import('./OtherComponent'));

function MyComponent() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <OtherComponent />
    </Suspense>
  );
}
```

## TypeScript in React
```tsx
interface Props {
  name: string;
  age: number;
  optional?: boolean;
}

const Person: React.FC<Props> = ({ name, age, optional = false }) => {
  return (
    <div>
      <h1>{name}</h1>
      <p>Age: {age}</p>
    </div>
  );
};
```

## Higher Order Components (HOC)
```jsx
function withLogging(WrappedComponent) {
  return function WithLoggingComponent(props) {
    useEffect(() => {
      console.log('Component mounted');
      return () => console.log('Component will unmount');
    }, []);

    return <WrappedComponent {...props} />;
  }
}

// Usage
const EnhancedComponent = withLogging(MyComponent);
```

## React Form Example
```jsx
function Form() {
  const [formData, setFormData] = useState({
    username: '',
    email: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="username"
        value={formData.username}
        onChange={handleChange}
      />
      <input
        name="email"
        value={formData.email}
        onChange={handleChange}
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

## Strict Mode Rendering Twice
React.StrictMode intentionally double-renders components in development to:
- Help find bugs caused by impure rendering
- Catch side effects in the render phase
- Identify potential issues with legacy lifecycle methods

This only happens in development mode, not in production.

## Class Components vs Hooks
You don't need to rewrite existing class components with hooks because:
- Class components are still supported
- Both can coexist in the same application
- Gradual migration is possible
- Some legacy libraries might still use class components

## Force Re-render Without setState
Several ways to force a re-render:
1. Using forceUpdate (class components):
```jsx
this.forceUpdate();
```

2. Using key prop:
```jsx
<Component key={Date.now()} />
```

3. Using useState with same value:
```jsx
const [, setToggle] = useState(false);
const forceUpdate = () => setToggle(t => !t);
```

## React Fiber
React Fiber is the new reconciliation engine in React 16:
- Enables incremental rendering
- Better prioritizes updates
- Improves performance for complex UIs
- Enables better error handling
- Supports async rendering

## Server Side Rendering (SSR)
SSR renders React components on the server:
- Better SEO
- Faster initial page load
- Better performance on low-end devices
- Common frameworks: Next.js, Gatsby

## React Query
```jsx
import { useQuery } from 'react-query';

function TodoList() {
  const { data, isLoading } = useQuery('todos', fetchTodos);

  if (isLoading) return 'Loading...';

  return (
    <ul>
      {data.map(todo => (
        <li key={todo.id}>{todo.title}</li>
      ))}
    </ul>
  );
}
```

## Redux in Plain JavaScript
```javascript
// Action Types
const INCREMENT = 'INCREMENT';
const DECREMENT = 'DECREMENT';

// Reducer
function counter(state = 0, action) {
  switch (action.type) {
    case INCREMENT:
      return state + 1;
    case DECREMENT:
      return state - 1;
    default:
      return state;
  }
}

// Store
const store = Redux.createStore(counter);
```

## Redux with React
```jsx
import { Provider, useSelector, useDispatch } from 'react-redux';

function Counter() {
  const count = useSelector(state => state.count);
  const dispatch = useDispatch();

  return (
    <div>
      <span>{count}</span>
      <button onClick={() => dispatch({ type: 'INCREMENT' })}>
        Increment
      </button>
    </div>
  );
}

function App() {
  return (
    <Provider store={store}>
      <Counter />
    </Provider>
  );
}
```

## Redux Toolkit
```jsx
import { createSlice, configureStore } from '@reduxjs/toolkit';

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: state => {
      state.value += 1;
    },
    decrement: state => {
      state.value -= 1;
    }
  }
});

const store = configureStore({
  reducer: {
    counter: counterSlice.reducer
  }
});

export const { increment, decrement } = counterSlice.actions;
```

