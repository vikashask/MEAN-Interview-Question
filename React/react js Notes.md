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
    Functional components are easy to test
    better performance , no state or lifecycle method
    Functional components are easy to debug
    Functional components are more reusable

```
function Hello(props){
   return <div>Hello {props.name}</div>
}
```

### Pure function

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