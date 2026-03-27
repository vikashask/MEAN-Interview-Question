### What is Flexbox?

> A Set of CSS Properties
> Creating Flexible Layouts
> Distributing Extra Space
> Aligning Content

- you can arrange item from right to left , left to right , top to bottom and bottom to top
- it provide reverse and rearrange the display item
- and easy to stretch item in there container

> flex-direction:

    row
    column
    column-reverse

> flex-wrap:

    wrap

> text-wrap:

    normal;
    nowrap;

> align-items : property is used to align the flex items vertically.

    center
    flex-start : aligns the flex items at the top of the container:
    flex-end : value aligns the flex items at the bottom of the container
    stretch :value stretches the flex items to fill the container
    baseline :value aligns the flex items such as their baselines aligns:

> align-content : property is used to align the flex lines.

    space-between :value displays the flex lines with equal space between them:
    space-around : value displays the flex lines with space before, between, and after them:
    stretch : value stretches the flex lines to take up the remaining space (this is default):
    center :value displays display the flex lines in the middle of the container:
    flex-start :value displays the flex lines at the start of the container:

> Perfect Centering : justify-content and align-items properties to center, and the flex item will be perfectly centered:

    .flex-container {
        display: flex;
        height: 300px;
        justify-content: center;
        align-items: center;
    }

> order

    <div style="order: 3">1</div>
    <div style="order: 2">2</div>

> flex-grow

    <div style="flex-grow: 1">1</div>
    <div style="flex-grow: 1">2</div>
    <div style="flex-grow: 8">3</div>

> flex-shrink

    <div style="flex-shrink: 0">3</div>

> flex-basis

      <div style="flex-basis: 200px">3</div>

> flex

    <div>2</div>
    <div style="flex: 0 0 200px">3</div>

> align-self

    <div style="align-self: center">3</div>

    <div style="align-self: flex-start">2</div>
    <div style="align-self: flex-end">3</div>

> flex-flow:

    like column wrap

## Display Order

order
