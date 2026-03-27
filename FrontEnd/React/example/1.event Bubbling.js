import React, { useState } from "react";

/**
 * Event Bubbling Example
 *
 * This example demonstrates how events in React bubble up from child to parent elements.
 * When you click on the inner button, the event propagates (bubbles up) to its parent divs.
 * The handlers will execute from the innermost element outward.
 */

const EventBubblingExample = () => {
  const [logs, setLogs] = useState([]);

  // Helper function to add log messages
  const addLog = (message) => {
    setLogs((prevLogs) => [message, ...prevLogs]);
  };

  // Event handlers for different levels
  const handleGrandparentClick = (e) => {
    addLog("3. Grandparent div clicked (event bubbled up to here)");
    // To stop event bubbling further, you could use:
    // e.stopPropagation();
  };

  const handleParentClick = (e) => {
    addLog("2. Parent div clicked (event bubbled up to here)");
    // e.stopPropagation();
  };

  const handleButtonClick = (e) => {
    addLog("1. Button clicked (event originated here)");
    // e.stopPropagation();
  };

  const clearLogs = () => {
    setLogs([]);
  };

  // Demonstrating how to stop event bubbling
  const handleStopPropagationExample = (e) => {
    addLog("Clicked on stop propagation example - event stops here!");
    e.stopPropagation(); // This prevents the event from bubbling up
  };

  return (
    <div className="event-bubbling-example">
      <h1>Event Bubbling in React</h1>

      <div
        className="grandparent"
        onClick={handleGrandparentClick}
        style={{
          padding: "30px",
          backgroundColor: "#f0f0f0",
          border: "2px solid #333",
        }}
      >
        Grandparent Div
        <div
          className="parent"
          onClick={handleParentClick}
          style={{
            padding: "20px",
            margin: "10px",
            backgroundColor: "#d0d0d0",
            border: "2px solid #666",
          }}
        >
          Parent Div
          <button
            onClick={handleButtonClick}
            style={{
              padding: "10px",
              margin: "10px",
              backgroundColor: "#3498db",
              color: "white",
              border: "none",
            }}
          >
            Click me! (Child Button)
          </button>
        </div>
      </div>

      <div
        style={{
          marginTop: "20px",
          padding: "10px",
          backgroundColor: "#e8e8e8",
        }}
      >
        <h3>Event Propagation Demonstration</h3>
        <p>
          Click on the nested elements above to see how the event bubbles up.
        </p>

        <div
          onClick={() =>
            addLog("Outer div clicked in stop propagation example")
          }
          style={{
            padding: "20px",
            backgroundColor: "#f5f5f5",
            border: "1px solid #999",
          }}
        >
          Outer div (with bubbling)
          <button
            onClick={handleStopPropagationExample}
            style={{
              padding: "10px",
              margin: "10px",
              backgroundColor: "#e74c3c",
              color: "white",
              border: "none",
            }}
          >
            Stop Propagation Example
          </button>
        </div>
      </div>

      <div style={{ marginTop: "20px" }}>
        <h3>Event Log:</h3>
        <button
          onClick={clearLogs}
          style={{
            padding: "5px 10px",
            backgroundColor: "#7f8c8d",
            color: "white",
            border: "none",
            marginBottom: "10px",
          }}
        >
          Clear Logs
        </button>
        <div
          style={{
            maxHeight: "200px",
            overflowY: "auto",
            border: "1px solid #ddd",
            padding: "10px",
          }}
        >
          {logs.length === 0 ? (
            <p>No events logged yet. Click on the elements above.</p>
          ) : (
            <ul style={{ listStyleType: "none", padding: 0 }}>
              {logs.map((log, index) => (
                <li
                  key={index}
                  style={{ padding: "5px", borderBottom: "1px solid #eee" }}
                >
                  {log}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <div
        style={{
          marginTop: "30px",
          padding: "10px",
          backgroundColor: "#f9f9f9",
          border: "1px solid #ddd",
        }}
      >
        <h3>Notes on Event Bubbling:</h3>
        <ol>
          <li>
            Events start from the target element and bubble up through ancestors
          </li>
          <li>You can stop bubbling with e.stopPropagation()</li>
          <li>
            React's event system is actually a synthetic wrapper over browser
            events
          </li>
          <li>Event bubbling is useful for event delegation patterns</li>
          <li>
            React event handlers are attached at the root DOM element in React
            16 and earlier, but use modern event delegation in React 17+
          </li>
        </ol>
      </div>
    </div>
  );
};

export default EventBubblingExample;

// Usage:
// import EventBubblingExample from './path/to/event Bubbling';
//
// function App() {
//   return (
//     <div className="App">
//       <EventBubblingExample />
//     </div>
//   );
// }
