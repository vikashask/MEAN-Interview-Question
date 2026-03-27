## UI -> trigger -> Action -> Goes to -> Reducer -> returns new state - to Store -> UI

- Redux : It is commonly used with other libraries like React and Angular for better state management of the application.
- Redux is single state tree
- A store is a single unit that holds the state tree and the methods to interact with the state tree.

## Rule #1 — Single source of truth

- getState() — Returns the current state of the application.
- dispatch(action) — The only way to update a state.
- subscribe(listener) :Every time a state is changed, it will be called and will return the updated state.

## Rule #2 — State is read-only

Step to configure

> index.js

```jsx
<Provider store={store}></Provider>
```

> Store.js

```jsx
export const store = createStore(
  rootReducer,
  initialState,
  composeEnhancers(applyMiddleware(thunk))
);
```

> card.reducer.js

```jsx
import { cartActionTypes } from "../actions/cart.actions";

export default function cartReducer(state = null, action) {
  switch (action.type) {
    case cartActionTypes.FETCH_CART_DATA_SUCCESS:
      return { items: [...action.data] };
    default:
      return state;
  }
}
```

> cart.action.js

```jsx
export const increaseCartDataAction = (productInfo) => (dispatch, getState) => {
  dispatch(loadingStart());
  const latestState = getState();
  const cartItemData = latestState.cart.items.find(
    (item) => item.id === productInfo.id
  );
  if (!cartItemData) {
    productInfo.count = parseInt(productInfo.count) + 1;
    latestState.cart.items.push(productInfo);
  } else {
    cartItemData.count++;
  }
  dispatch(fetchCartDataSuccessAction(latestState.cart.items));
  dispatch(loadingEnd());
};
```
