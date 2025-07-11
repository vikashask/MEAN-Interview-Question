# React Hooks Guide

## Basic Hooks

### useState
```javascript
// Basic state
const [count, setCount] = useState(0);

// Object state
const [user, setUser] = useState({
    name: '',
    email: ''
});

// Function update
setCount(prevCount => prevCount + 1);

// Object update
setUser(prev => ({
    ...prev,
    name: 'John'
}));
```

### useEffect
```javascript
// Run on every render
useEffect(() => {
    document.title = `Count: ${count}`;
});

// Run only on mount
useEffect(() => {
    fetchData();
}, []);

// Run when dependencies change
useEffect(() => {
    console.log(`Count changed: ${count}`);
}, [count]);

// Cleanup
useEffect(() => {
    const subscription = subscribe();
    return () => {
        subscription.unsubscribe();
    };
}, []);
```

### useContext
```javascript
const ThemeContext = React.createContext('light');

// Provider
function App() {
    return (
        <ThemeContext.Provider value="dark">
            <ThemedButton />
        </ThemeContext.Provider>
    );
}

// Consumer using hook
function ThemedButton() {
    const theme = useContext(ThemeContext);
    return <button className={theme}>Click Me</button>;
}
```

## Additional Hooks

### useReducer
```javascript
const initialState = { count: 0 };

function reducer(state, action) {
    switch (action.type) {
        case 'increment':
            return { count: state.count + 1 };
        case 'decrement':
            return { count: state.count - 1 };
        default:
            throw new Error();
    }
}

function Counter() {
    const [state, dispatch] = useReducer(reducer, initialState);
    
    return (
        <>
            Count: {state.count}
            <button onClick={() => dispatch({ type: 'increment' })}>+</button>
            <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
        </>
    );
}
```

### useCallback
```javascript
function ParentComponent() {
    const [count, setCount] = useState(0);
    
    const handleClick = useCallback(() => {
        setCount(c => c + 1);
    }, []); // Empty deps = function reference never changes
    
    return <ChildComponent onClick={handleClick} />;
}

// Memoized child component
const ChildComponent = React.memo(({ onClick }) => {
    return <button onClick={onClick}>Click me</button>;
});
```

### useMemo
```javascript
function ExpensiveComponent({ data }) {
    // Memoize expensive calculation
    const processedData = useMemo(() => {
        return data.map(item => expensiveOperation(item));
    }, [data]);
    
    // Memoize object to prevent unnecessary re-renders
    const memoizedValue = useMemo(() => ({
        x: 100,
        y: 200
    }), []);
    
    return <div>{processedData}</div>;
}
```

### useRef
```javascript
function TextInputWithFocusButton() {
    const inputRef = useRef(null);
    
    const focusInput = () => {
        inputRef.current.focus();
    };
    
    // Preserve value between renders
    const countRef = useRef(0);
    useEffect(() => {
        countRef.current = countRef.current + 1;
    });
    
    return (
        <>
            <input ref={inputRef} type="text" />
            <button onClick={focusInput}>Focus Input</button>
            <div>Render count: {countRef.current}</div>
        </>
    );
}
```

## Custom Hooks

### useLocalStorage
```javascript
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
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            setStoredValue(valueToStore);
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (error) {
            console.error(error);
        }
    };
    
    return [storedValue, setValue];
}

// Usage
function App() {
    const [name, setName] = useLocalStorage('name', 'Bob');
    return <input value={name} onChange={e => setName(e.target.value)} />;
}
```

### useWindowSize
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

// Usage
function App() {
    const { width, height } = useWindowSize();
    return <div>Window size: {width} x {height}</div>;
}
```

### useFetch
```javascript
function useFetch(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
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

// Usage
function UserProfile({ userId }) {
    const { data, loading, error } = useFetch(`/api/users/${userId}`);
    
    if (loading) return 'Loading...';
    if (error) return 'Error!';
    
    return <div>{data.name}</div>;
}
```

## Best Practices

1. Rules of Hooks
   - Only call hooks at the top level
   - Only call hooks from React functions
   - Use the eslint-plugin-react-hooks

2. Dependencies
   - Include all values used in the effect
   - Use exhaustive-deps lint rule
   - Consider useCallback for function dependencies

3. Performance
   - Use useMemo for expensive calculations
   - Use useCallback for callback functions
   - Avoid premature optimization

4. Custom Hooks
   - Start names with "use"
   - Extract common stateful logic
   - Keep them focused and reusable

5. Error Handling
```javascript
function useAPI(url) {
    const [state, setState] = useState({
        data: null,
        loading: true,
        error: null
    });
    
    useEffect(() => {
        let mounted = true;
        
        async function fetchData() {
            try {
                const response = await fetch(url);
                const data = await response.json();
                
                if (mounted) {
                    setState({
                        data,
                        loading: false,
                        error: null
                    });
                }
            } catch (error) {
                if (mounted) {
                    setState({
                        data: null,
                        loading: false,
                        error
                    });
                }
            }
        }
        
        fetchData();
        
        return () => {
            mounted = false;
        };
    }, [url]);
    
    return state;
}
```