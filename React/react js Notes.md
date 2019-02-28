### component
    Components let you split the UI into independent, reusable pieces, and think about each piece in isolation
    2 types of component
    * class component
    * functional component

### class component
    are es6 class
```
class Hello extends Component{
   render(){
      return <div>Hello {this.props.name}</div>
   }
}
```
### functional component
    are function
    functional component is to accept props as an argument and return valid JSX.
    better performance , no state or lifecycle method
    Functional components are easier to read, debug, and test. They offer performance benefits, decreased coupling, and
    greater reusability.

```
function Hello(props){
   return <div>Hello {props.name}</div>
}
```

### Pure function
    The function always returns the same result if the same arguments are passed in.It does not depend on any state, or data,
    change during a program’s execution.
    The function does not produce any observable side effects such as network requests, input and output devices, or data 
    mutation.
    -Making a HTTP request
    -Mutating data
    -Printing to a screen or console
    -DOM Query/Manipulation
    -Math.random()
    -Getting the current time

```
function priceAfterTax(productPrice) {
 return (productPrice * 0.20) + productPrice;
}
```
### Impure function

### Pure component

### stateless component

### statefull component

### Controlled component

### Uncontrolled component

### props vs state

### create react app

### virtual DOM

### Real DOM

### React DOM

### angular vs react

### jsx

### life cycle

### setState

### forceUpdate

### refs

### imutable 

cannot change

### mutable 

can change

### webpack

### lazy loading

### HOC higer order component

### redux saga vs thunk

### reselect

### react context