- Handles synchronous side effects that need to read or modify the DOM before the browser paints.
- Executes synchronously after React updates the DOM but before the browser paints.

```
import { useLayoutEffect, useRef, useState } from 'react';

function Tooltip({ targetRef, text }) {
  const tooltipRef = useRef(null);
  const [position, setPosition] = useState({ top: 0, left: 0 });

  useLayoutEffect(() => {
    const target = targetRef.current;
    const tooltip = tooltipRef.current;

    if (target && tooltip) {
      const { top, left, height } = target.getBoundingClientRect();
      setPosition({
        top: top + height + window.scrollY,
        left: left + window.scrollX,
      });
    }
  }, [targetRef]);

  return (
    <div
      ref={tooltipRef}
      style={{
        position: 'absolute',
        top: position.top,
        left: position.left,
        background: 'black',
        color: 'white',
        padding: '5px',
      }}
    >
      {text}
    </div>
  );
}
```
Explanation: Measures the target element’s position and sets the tooltip’s position before the browser paints, preventing flickering.

