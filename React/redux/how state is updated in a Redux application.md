## UI -> trigger -> Action -> Goes to -> Reducer -> returns new state - to Store -> UI

- Redux : It is commonly used with other libraries like React and Angular for better state management of the application.
- Redux is single state tree
- A store is a single unit that holds the state tree and the methods to interact with the state tree.

## Rule #1 — Single source of truth

- getState() — Returns the current state of the application.
- dispatch(action) — The only way to update a state.
- subscribe(listener) :Every time a state is changed, it will be called and will return the updated state.

## Rule #2 — State is read-only
