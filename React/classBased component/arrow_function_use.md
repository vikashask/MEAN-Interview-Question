Arrow function automatic Bind event in class component
ex

```
handelClick = () => {
    this.setState({counter:1})
}

render(
    return(
        <button onClick={this.handelClick(event)}> /<button>
    )
)
```
