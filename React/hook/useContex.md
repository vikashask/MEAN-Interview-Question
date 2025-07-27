> > > useContext lets you subscribe to React context without introducing nesting.

```jsx
// main component (WishlistContext)
export const WishlistContext = createContext();

const WishlistContextProvider = (props) => {
<WishlistContext.Provider
        value={{
            wishlistDataProvider,
            handelRMAQty,
            handleUnitType,
          }} >

        {children}

</WishlistContext.Provider
}

// child component
import { WishlistContext } from "./WishlistContext";
const WishlistDetails = ({ wishlistDataProvider, props }) => {
const { wishlistDataProvider, handelRMAQty, handleUnitType } =
useContext(WishlistContext);
}
```
