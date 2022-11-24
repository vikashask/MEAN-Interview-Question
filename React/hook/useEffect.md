## useEffect Hook replaces the componentDidMount, componentDidUpdate, and componentWillUnmount lifecycle methods.

- deal with side effects like data fetching and state or variable changes for React functional components. It takes 2 arguments:

1. function
2. dependency array: run every time if value is updated.

## Runs Once on First Render and conditionally

```
useEffect(() => {
    console.log('This runs once on first render');
}, []);
```

### runs on each render and each update

```
useEffect(() => {
    console.log('This runs once on first render');
});
```

## Runs On a Specified Dependency

```
 useEffect(() => {
    console.log("Count variable has changed!")
 }, [count]);
```

## for multiple variable changes?

```
 useEffect(() => {
   console.log("Some count variable has changed!")
}, [count, count1, count2]);
```

## useEffect with Cleanup

run right before the component unmounts, just like componentWillUnmount,
simply use its return function like so:

```
useEffect(() => {
    console.log('This hook is running.');

    return () => {
        console.log('This hook is now unmounting.');
    };
});
```
