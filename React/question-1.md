## How to use componentWillMount() in React Hooks?

Code inside componentDidMount run once when the component is mounted. useEffect hook equivalent for this behaviour is

useEffect(() => {
// Your code here
}, []);
Without the second parameter the useEffect hook will be called on every render of the component which can be dangerous.

you are adding a event listener in componentDidMount and removing it in componentWillUnmount as below.

    componentDidMount() {
    window.addEventListener('mousemove', () => {})
    }

    componentWillUnmount() {
    window.removeEventListener('mousemove', () => {})
    }

## How to unmount component in react hook

```
useEffect(() => {
	//your code goes here
    return () => {
      //your cleanup code codes here
    };
},[]);

useEffect(() => {
  window.addEventListener('mousemove', () => {});

  // returned function will be called on component unmount
  return () => {
    window.removeEventListener('mousemove', () => {})
  }
}, [])

```
