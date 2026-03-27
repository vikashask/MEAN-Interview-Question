# Redux Guide

## Core Concepts

### Store
```javascript
import { createStore } from 'redux';

const initialState = {
    count: 0,
    todos: []
};

const store = createStore(reducer, initialState);
```

### Actions
```javascript
// Action Types
const ADD_TODO = 'ADD_TODO';
const TOGGLE_TODO = 'TOGGLE_TODO';

// Action Creators
const addTodo = (text) => ({
    type: ADD_TODO,
    payload: {
        text,
        completed: false
    }
});

const toggleTodo = (id) => ({
    type: TOGGLE_TODO,
    payload: id
});
```

### Reducers
```javascript
function todoReducer(state = [], action) {
    switch (action.type) {
        case ADD_TODO:
            return [
                ...state,
                {
                    id: Date.now(),
                    ...action.payload
                }
            ];
            
        case TOGGLE_TODO:
            return state.map(todo =>
                todo.id === action.payload
                    ? { ...todo, completed: !todo.completed }
                    : todo
            );
            
        default:
            return state;
    }
}
```

## Redux with React

### Provider Setup
```javascript
import { Provider } from 'react-redux';

function App() {
    return (
        <Provider store={store}>
            <TodoApp />
        </Provider>
    );
}
```

### Connecting Components
```javascript
import { useSelector, useDispatch } from 'react-redux';

function TodoList() {
    const todos = useSelector(state => state.todos);
    const dispatch = useDispatch();
    
    const handleToggle = (id) => {
        dispatch(toggleTodo(id));
    };
    
    return (
        <ul>
            {todos.map(todo => (
                <TodoItem
                    key={todo.id}
                    {...todo}
                    onToggle={() => handleToggle(todo.id)}
                />
            ))}
        </ul>
    );
}
```

## Middleware

### Redux Thunk
```javascript
import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';

const store = createStore(
    reducer,
    applyMiddleware(thunk)
);

// Async Action Creator
const fetchTodos = () => async dispatch => {
    dispatch({ type: 'FETCH_TODOS_REQUEST' });
    
    try {
        const response = await fetch('/api/todos');
        const todos = await response.json();
        dispatch({
            type: 'FETCH_TODOS_SUCCESS',
            payload: todos
        });
    } catch (error) {
        dispatch({
            type: 'FETCH_TODOS_FAILURE',
            error
        });
    }
};
```

### Custom Middleware
```javascript
const logger = store => next => action => {
    console.group(action.type);
    console.log('prev state', store.getState());
    console.log('action', action);
    
    const result = next(action);
    
    console.log('next state', store.getState());
    console.groupEnd();
    
    return result;
};

const store = createStore(
    reducer,
    applyMiddleware(thunk, logger)
);
```

## Redux Toolkit

### Slice Creation
```javascript
import { createSlice } from '@reduxjs/toolkit';

const todoSlice = createSlice({
    name: 'todos',
    initialState: [],
    reducers: {
        addTodo: (state, action) => {
            state.push({
                id: Date.now(),
                text: action.payload,
                completed: false
            });
        },
        toggleTodo: (state, action) => {
            const todo = state.find(todo => todo.id === action.payload);
            if (todo) {
                todo.completed = !todo.completed;
            }
        }
    }
});

export const { addTodo, toggleTodo } = todoSlice.actions;
export default todoSlice.reducer;
```

### Store Configuration
```javascript
import { configureStore } from '@reduxjs/toolkit';
import todoReducer from './todoSlice';

const store = configureStore({
    reducer: {
        todos: todoReducer
    }
});
```

### CreateAsyncThunk
```javascript
import { createAsyncThunk } from '@reduxjs/toolkit';

export const fetchTodos = createAsyncThunk(
    'todos/fetchTodos',
    async () => {
        const response = await fetch('/api/todos');
        return response.json();
    }
);

const todoSlice = createSlice({
    name: 'todos',
    initialState: {
        items: [],
        loading: false,
        error: null
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchTodos.pending, (state) => {
                state.loading = true;
            })
            .addCase(fetchTodos.fulfilled, (state, action) => {
                state.loading = false;
                state.items = action.payload;
            })
            .addCase(fetchTodos.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message;
            });
    }
});
```

## Best Practices

### 1. State Shape
```javascript
// Good - Normalized State
{
    todos: {
        byId: {
            "1": { id: "1", text: "Buy milk", completed: false },
            "2": { id: "2", text: "Walk dog", completed: true }
        },
        allIds: ["1", "2"]
    }
}
```

### 2. Action Naming
```javascript
// Domain/Event pattern
const ADD_TODO = 'todos/add';
const TOGGLE_TODO = 'todos/toggle';
const FETCH_TODOS = 'todos/fetch';
```

### 3. Selectors
```javascript
// Create reusable selectors
const selectTodos = state => state.todos.items;
const selectTodoById = (state, id) =>
    state.todos.items.find(todo => todo.id === id);

// Use with hooks
function TodoList() {
    const todos = useSelector(selectTodos);
    // ...
}
```

### 4. Immutable Updates
```javascript
// Use spread operator or Immer
const todoReducer = (state, action) => {
    switch (action.type) {
        case UPDATE_TODO:
            return {
                ...state,
                todos: state.todos.map(todo =>
                    todo.id === action.payload.id
                        ? { ...todo, ...action.payload }
                        : todo
                )
            };
        default:
            return state;
    }
};
```

### 5. Error Handling
```javascript
const fetchTodosReducer = (state, action) => {
    switch (action.type) {
        case 'FETCH_TODOS_REQUEST':
            return {
                ...state,
                loading: true,
                error: null
            };
        case 'FETCH_TODOS_SUCCESS':
            return {
                ...state,
                loading: false,
                items: action.payload
            };
        case 'FETCH_TODOS_FAILURE':
            return {
                ...state,
                loading: false,
                error: action.error,
                items: []
            };
        default:
            return state;
    }
};
```