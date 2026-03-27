# React Advanced Interview Questions

## Core Concepts

### 1. What is Virtual DOM?
Virtual DOM is a lightweight copy of the actual DOM. React uses it to improve performance by:
- Creating a virtual representation of UI
- Comparing it with previous version
- Only updating what has changed in the real DOM

```javascript
// Example of how Virtual DOM works conceptually
const virtualElement = React.createElement(
    'div',
    { className: 'container' },
    'Hello World'
);
```

### 2. Explain React Fiber
React Fiber is the new reconciliation engine in React 16. It enables:
- Incremental rendering
- Better error handling
- Priority-based rendering
- Improved performance

### 3. What are Higher-Order Components (HOC)?
HOCs are functions that take a component and return a new component with enhanced functionality.

```javascript
// HOC Example
const withLogger = (WrappedComponent) => {
    return class extends React.Component {
        componentDidMount() {
            console.log('Component is mounted');
        }
        
        render() {
            return <WrappedComponent {...this.props} />;
        }
    };
};

// Usage
const EnhancedComponent = withLogger(BaseComponent);
```

## Advanced Patterns

### 1. Render Props Pattern
```javascript
class MouseTracker extends React.Component {
    state = { x: 0, y: 0 };
    
    handleMouseMove = (event) => {
        this.setState({
            x: event.clientX,
            y: event.clientY
        });
    };
    
    render() {
        return (
            <div onMouseMove={this.handleMouseMove}>
                {this.props.render(this.state)}
            </div>
        );
    }
}

// Usage
<MouseTracker 
    render={({ x, y }) => (
        <h1>Mouse position: {x}, {y}</h1>
    )}
/>
```

### 2. Compound Components
```javascript
const Toggle = {
    On: ({ children }) => children,
    Off: ({ children }) => children,
    Button: ({ toggle, ...props }) => (
        <button onClick={toggle} {...props} />
    )
};

// Usage
<Toggle>
    <Toggle.On>The button is on</Toggle.On>
    <Toggle.Off>The button is off</Toggle.Off>
    <Toggle.Button />
</Toggle>
```

## Performance Optimization

### 1. React.memo vs useMemo
```javascript
// React.memo for functional components
const MyComponent = React.memo(function MyComponent(props) {
    return <div>{props.value}</div>;
});

// useMemo for expensive calculations
function Calculator() {
    const [value, setValue] = useState(0);
    const expensiveResult = useMemo(() => {
        return computeExpensiveValue(value);
    }, [value]);
    
    return <div>{expensiveResult}</div>;
}
```

### 2. useCallback
```javascript
function ParentComponent() {
    const [count, setCount] = useState(0);
    
    const handleClick = useCallback(() => {
        setCount(c => c + 1);
    }, []); // Empty deps array = function reference never changes
    
    return <ChildComponent onClick={handleClick} />;
}
```

## State Management

### 1. Context API vs Redux
```javascript
// Context API
const ThemeContext = React.createContext('light');

function App() {
    return (
        <ThemeContext.Provider value="dark">
            <ThemedButton />
        </ThemeContext.Provider>
    );
}

// Redux
const store = createStore(reducer);

function App() {
    return (
        <Provider store={store}>
            <ConnectedComponent />
        </Provider>
    );
}
```

### 2. Custom Hooks
```javascript
function useWindowSize() {
    const [size, setSize] = useState({
        width: window.innerWidth,
        height: window.innerHeight
    });
    
    useEffect(() => {
        const handleResize = () => {
            setSize({
                width: window.innerWidth,
                height: window.innerHeight
            });
        };
        
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);
    
    return size;
}
```

## Error Handling

### 1. Error Boundaries
```javascript
class ErrorBoundary extends React.Component {
    state = { hasError: false };
    
    static getDerivedStateFromError(error) {
        return { hasError: true };
    }
    
    componentDidCatch(error, errorInfo) {
        logErrorToService(error, errorInfo);
    }
    
    render() {
        if (this.state.hasError) {
            return <h1>Something went wrong.</h1>;
        }
        return this.props.children;
    }
}
```

## Testing

### 1. Unit Testing with Jest and React Testing Library
```javascript
import { render, fireEvent } from '@testing-library/react';

test('button click increments counter', () => {
    const { getByText } = render(<Counter />);
    const button = getByText('Increment');
    
    fireEvent.click(button);
    
    expect(getByText('Count: 1')).toBeInTheDocument();
});
```

## Best Practices

1. Component Organization
   - Keep components small and focused
   - Use meaningful names
   - Separate concerns

2. State Management
   - Keep state as local as possible
   - Use Context API for global state
   - Consider Redux for complex state

3. Performance
   - Use React.memo for pure components
   - Implement lazy loading
   - Optimize re-renders

4. Code Style
   - Use functional components
   - Implement proper PropTypes
   - Follow ESLint rules
