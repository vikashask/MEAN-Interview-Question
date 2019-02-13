## CSS Selectors
> element Selector = like <p>
> id Selector = write a hash (#) character
> class Selector = write a period (.) character
> Grouping Selectors
> group selectors, separate each selector with a comma.
    example 
    h1, h2, p {
    text-align: center;
    color: red;
    }
## Three Ways to Insert CSS
    External style sheet
    Internal style sheet
    Inline style
## The CSS Box Model
    All HTML elements can be considered as boxes
    It consists of: margins, borders, padding, and the actual content
## The position Property
>position: static = Static positioned elements are not affected by the top, bottom, left, and right properties.

>position: relative = Setting the top, right, bottom, and left properties of a relatively-positioned element will cause it to be adjusted away from its normal position. Other content will not be adjusted to fit into any gap left by the element.

>position: fixed = it always stays in the same place even if the page is scrolled.

>position: absolute = if an absolute positioned element has no positioned ancestors, it uses the document body, and moves along with page scrolling

>position: sticky = A sticky element toggles between relative and fixed, depending on the scroll position
    

CSS Positioning Properties
    
    Property	Description
    bottom	Sets the bottom margin edge for a positioned box
    clip	Clips an absolutely positioned element
    left	Sets the left margin edge for a positioned box
    position	Specifies the type of positioning for an element
    right	Sets the right margin edge for a positioned box
    top	Sets the top margin edge for a positioned box
    z-index Sets the stack order of an element
