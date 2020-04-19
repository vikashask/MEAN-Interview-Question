### Grid Layout
The CSS Grid Layout Module offers a grid-based layout system, with rows and columns
> Grid Elements
A grid layout consists of a parent element, with one or more child elements.
> Display Property
An HTML element becomes a grid container when its display property is set to grid or inline-grid.
> Grid Columns
> Grid Rows
> Grid Gaps
    grid-column-gap
    grid-row-gap
    grid-gap
> Grid Lines
    The lines between columns are called `column lines`.
    The lines between rows are called `row lines`.
`
.item1 {
  grid-column-start: 1;
  grid-column-end: 3;
}

.item1 {
  grid-row-start: 1;
  grid-row-end: 3;
}
`

### CSS Grid Container
> The grid-template-columns Property
The grid-template-columns property defines the number of columns in your grid layout, and it can define the width of each column

    .grid-container {
    display: grid;
    grid-template-columns: auto auto auto auto;
    }

    grid-template-columns: auto auto auto auto;  4 columns
    grid-template-columns: auto auto auto auto auto;  5 columns
    grid-template-columns: auto auto auto;  3 columns

    Set a size for the 4 columns:
    grid-template-columns: 80px 200px auto 40px;

> The grid-template-rows Property
    The grid-template-rows property defines the height of each row.
    .grid-container {
    display: grid;
    grid-template-rows: 80px 200px;
    }
    1st row 80px
    2nd row 200px

>The justify-content Property
    The justify-content property is used to align the whole grid inside the container.

    .grid-container {
    display: grid;
    justify-content: space-evenly;
    }

    justify-content: space-around;
    justify-content: space-between;
    justify-content: center;
    justify-content: start;
    justify-content: end;

> The align-content Property
    The align-content property is used to vertically align the whole grid inside the container.

    .grid-container {
    display: grid;
    height: 400px;
    align-content: center;
    }
    align-content: space-evenly;
    align-content: space-around;
    align-content: space-between;
    align-content: start;
    align-content: end;
