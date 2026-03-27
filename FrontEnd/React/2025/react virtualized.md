# React Virtualized

**React Virtualized** is a popular React library used for efficiently rendering large lists, grids, and tabular data. It solves the performance issues associated with rendering thousands or millions of items in the DOM at once by using a technique called **Windowing** (or Virtualization).

## What is Windowing (Virtualization)?

Normally, if you have a list of 10,000 items, React would create 10,000 DOM nodes. This is slow, consumes a lot of memory, and causes "jank" (stuttering) when scrolling.

**Windowing** only renders the items that are currently visible in the user's viewport (plus a small buffer). As the user scrolls, items likely to leave the screen are destroyed (or recycled), and new items entering the screen are created.

At any given time, you might only be rendering ~20 items instead of 10,000.

## Key Components

1.  **List**: For rendering a simple vertical list of items.
2.  **Grid**: For rendering tabular data (rows and columns).
3.  **AutoSizer**: A Higher-Order Component (HOC) that automatically calculates the width and height of a single child so it fills the available space.
4.  **WindowScroller**: Allows a `List` or `Grid` to scroll with the window's scrollbar instead of its own container.
5.  **CellMeasurer**: Automatically measures the size of cell contents (useful for dynamic row heights).

## Installation

```bash
npm install react-virtualized
```

## Example: Rendering a List

Here is a simple example using the `List` component to render 1,000 rows.

```jsx
import React from 'react';
import ReactDOM from 'react-dom';
import { List } from 'react-virtualized';
import 'react-virtualized/styles.css'; // only needs to be imported once

// 1. Data to render
const list = Array(1000).fill().map((val, idx) => {
  return {
    id: idx,
    name: `John Doe ${idx}`,
    image: 'http://via.placeholder.com/40',
    text: `Description for item ${idx}`
  }
});

function RowRenderer({
  key,         // Unique key
  index,       // Index of row within collection
  isScrolling, // The List is currently being scrolled
  isVisible,   // This row is visible within the List (eg it is not an overscanned row)
  style        // Style object to be applied to row (to position it)
}) {
  return (
    <div key={key} style={style} className="row">
      <div className="image">
        <img src={list[index].image} alt="" />
      </div>
      <div className="content">
        <div>{list[index].name}</div>
        <div>{list[index].text}</div>
      </div>
    </div>
  );
}

function MyList() {
  return (
    <div className="list-container">
      <List
        width={800}          // Width of the List
        height={600}         // Height of the List
        rowCount={list.length} // Total number of items
        rowHeight={50}       // Height of each row (can be a function)
        rowRenderer={RowRenderer} // Function to render a row
      />
    </div>
  );
}

ReactDOM.render(<MyList />, document.getElementById('root'));
```

### Explaining the props:

-   **width/height**: The explicit dimensions of the list. (Use `AutoSizer` to make this flexible).
-   **rowCount**: How many items are in the list.
-   **rowHeight**: Fixed height makes calculations faster. You can use dynamic heights but it requires more configuration (CellMeasurer).
-   **rowRenderer**: The function responsible for returning the JSX for a specific row. **Crucial**: You must apply the `style` prop passed to this function to your row element, as this contains the absolute positioning data required for virtualization to work.

## React Virtualized vs React Window

**react-window** is a newer, lighter, and faster library written by the same author (Brian Vaughn). 
-   **react-virtualized**: More features, heavier, "kitchen sink" approach.
-   **react-window**: Core features only, smaller bundle size, harder to implement edge cases (like dynamic heavy layouts) manually but often sufficient for 90% of use cases.

If starting a new project, it is often recommended to try **react-window** first.
