# Higher-Order Components (HOCs) in React

## Simple mental model

Think of an HOC as a **wrapper factory**: you give it a component, it returns a **new** component that does extra work, then renders yours.

You do **not** change `Profile`. You wrap it.

```
You write:     Profile
You wrap:      withAuth(Profile)
React uses:    AuthProfile   ← this is what actually renders
```

### Tiny analogy

`Profile` only knows how to show a name.

`withAuth` is like a security guard at the door:

1. Check if the user is logged in.
2. If no → show “Please login”.
3. If yes → let `Profile` render.

`Profile` never learns about login. The guard does.

### Flow

```
App
 └─ AuthProfile          ← HOC (logic)
      └─ Profile         ← original (UI)
```

```
App renders AuthProfile
        ↓
withAuth wrapper runs first
        ↓
   Logged in?
   /        \
 No          Yes
  ↓           ↓
Please     Render Profile + extra props
login           ↓
           Profile only draws UI
```

### Same idea as higher-order functions

You already know this in JS:

```js
function withLog(fn) {
  return function (...args) {
    console.log("called");
    return fn(...args);
  };
}
```

HOC is the same pattern for **components**:

```js
function withX(Component) {
  return function NewComponent(props) {
    // extra logic
    return <Component {...props} extra={...} />;
  };
}
```

Function + function → new function.
Component + HOC → new component.

---

## Definition and Concept

A **Higher-Order Component (HOC)** is an advanced technique in React for reusing component logic. It is a function that takes a component and returns a new component with enhanced behavior or additional props.

HOCs are not part of the React API but a pattern that emerges from React’s compositional nature. They are commonly used to:

- Share common functionality between components.
- Abstract stateful logic.
- Implement cross-cutting concerns such as logging, authentication, and loading states.

## Syntax Overview

A Higher-Order Component is a function with this general signature:

```jsx
const EnhancedComponent = higherOrderComponent(WrappedComponent);
```

Where `higherOrderComponent` is a function that receives a component (`WrappedComponent`) and returns a new component (`EnhancedComponent`), often adding props or behavior.

Example skeleton:

```jsx
function withEnhancement(WrappedComponent) {
  return function EnhancedComponent(props) {
    // Add extra logic or props here
    return <WrappedComponent {...props} />;
  };
}
```

`{...props}` means: keep whatever the parent already passed, then add extra props from the HOC.

---

## Simple examples

### 1. Inject a user (HOC adds a prop)

`Hello` only prints a name. It does not fetch a user.

```jsx
function Hello({ name }) {
  return <h1>Hello, {name}</h1>;
}

function withUser(WrappedComponent) {
  return function WithUser(props) {
    const user = { name: "Amit" }; // imagine this came from context / API
    return <WrappedComponent {...props} name={user.name} />;
  };
}

const HelloWithUser = withUser(Hello);

// <HelloWithUser />  →  Hello, Amit
```

| Piece | Job |
|---|---|
| `Hello` | UI only |
| `withUser` | Gets data, passes it as props |
| `HelloWithUser` | The new component you actually use |

### 2. Loading gate (HOC decides what to render)

```jsx
function UserList({ users }) {
  return users.map((u) => <p key={u}>{u}</p>);
}

function withLoading(WrappedComponent) {
  return function WithLoading({ isLoading, ...rest }) {
    if (isLoading) return <p>Loading...</p>;
    return <WrappedComponent {...rest} />;
  };
}

const UserListWithLoading = withLoading(UserList);

<UserListWithLoading isLoading={true} users={["A", "B"]} />
// shows Loading...

<UserListWithLoading isLoading={false} users={["A", "B"]} />
// shows A, B
```

`UserList` never checks `isLoading`. The wrapper does.

---

## Interview-style examples

### 1. Logging HOC

This HOC logs props whenever the wrapped component renders.

```jsx
function withLogging(WrappedComponent) {
  return function LoggingComponent(props) {
    console.log("Props:", props);
    return <WrappedComponent {...props} />;
  };
}
```

Usage:

```jsx
const MyComponentWithLogging = withLogging(MyComponent);
```

### 2. Loader HOC

This HOC displays a loading spinner until data is ready.

```jsx
function withLoader(WrappedComponent) {
  return function LoaderComponent({ isLoading, ...props }) {
    if (isLoading) {
      return <div>Loading...</div>;
    }
    return <WrappedComponent {...props} />;
  };
}
```

Usage:

```jsx
const MyComponentWithLoader = withLoader(MyComponent);
```

### 3. Authentication HOC

This HOC redirects or blocks access if the user is not authenticated.

```jsx
import { Redirect } from 'react-router-dom';

function withAuth(WrappedComponent) {
  return function AuthComponent(props) {
    const isAuthenticated = /* logic to check auth status */;

    if (!isAuthenticated) {
      return <Redirect to="/login" />;
    }
    return <WrappedComponent {...props} />;
  };
}
```

Usage:

```jsx
const ProtectedComponent = withAuth(MyComponent);
```

---

## Key Benefits and Pitfalls

### Benefits

- **Code reuse**: Extract common logic and reuse it across multiple components.
- **Separation of concerns**: Keep component code focused on UI while HOCs handle logic.
- **Enhance components**: Add features like logging, error handling, or theming without modifying the original component.

### Pitfalls

- **Wrapper hell**: Excessive nesting of HOCs can make debugging and component trees complex.
- **Static methods lost**: HOCs may not automatically copy static methods from wrapped components.
- **Ref forwarding**: HOCs need special handling to forward refs properly.
- **Name collisions**: Props added by HOCs may conflict with existing props.

## Comparison with Custom Hooks

| Aspect         | Higher-Order Components (HOCs)                 | Custom Hooks                                      |
| -------------- | ---------------------------------------------- | ------------------------------------------------- |
| Purpose        | Reuse component logic by wrapping components   | Reuse stateful logic inside functional components |
| Syntax         | Functions returning components                 | Functions returning state and functions           |
| Usage          | Wrap components to inject props or behavior    | Call hooks inside functional components           |
| Ref forwarding | Requires explicit handling                     | Not applicable                                    |
| Readability    | Can cause nested wrappers and harder debugging | More straightforward and composable               |
| Compatibility  | Works with class and functional components     | Only functional components                        |

### When to use what today

- **Need to reuse logic inside a component** (fetch, toggle, form) → **custom hook** (`useUser()`, `useAuth()`).
- **Need to wrap / replace the whole component** (auth gate, inject props without touching the child) → **HOC**.

In modern React, **Custom Hooks** are often preferred for logic reuse due to their simplicity and composability. However, HOCs remain useful when you need to manipulate component trees or inject props at a component level. Older libraries (for example Redux `connect`) also use this pattern.
