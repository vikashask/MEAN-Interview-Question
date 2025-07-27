/**
 * Event Capturing Example
 *
 * In DOM event propagation, events travel through 3 phases:
 * 1. Capturing phase - from window to the target element
 * 2. Target phase - the event reaches the target element
 * 3. Bubbling phase - from the target back up to window
 *
 * The third parameter of addEventListener() specifies whether to use capturing:
 * - false (default): event handler is executed during bubbling phase
 * - true: event handler is executed during capturing phase
 */

document.addEventListener("DOMContentLoaded", function () {
  // Create a simple DOM structure
  const container = document.createElement("div");
  container.id = "container";
  container.style.padding = "25px";
  container.style.backgroundColor = "lightblue";

  const parent = document.createElement("div");
  parent.id = "parent";
  parent.style.padding = "25px";
  parent.style.backgroundColor = "lightgreen";

  const child = document.createElement("div");
  child.id = "child";
  child.style.padding = "25px";
  child.style.backgroundColor = "pink";
  child.textContent = "Click me!";

  // Build the DOM structure
  parent.appendChild(child);
  container.appendChild(parent);
  document.body.appendChild(container);

  // Add event listeners with capturing phase (3rd parameter set to true)
  document.body.addEventListener(
    "click",
    function (event) {
      console.log("Body captured the event");
    },
    true
  );

  container.addEventListener(
    "click",
    function (event) {
      console.log("Container captured the event");
    },
    true
  );

  parent.addEventListener(
    "click",
    function (event) {
      console.log("Parent captured the event");
    },
    true
  );

  child.addEventListener(
    "click",
    function (event) {
      console.log("Child captured the event");
    },
    true
  );

  // For comparison, add event listeners for bubbling phase
  document.body.addEventListener(
    "click",
    function (event) {
      console.log("Body bubbled the event");
    },
    false
  );

  container.addEventListener(
    "click",
    function (event) {
      console.log("Container bubbled the event");
    },
    false
  );

  parent.addEventListener(
    "click",
    function (event) {
      console.log("Parent bubbled the event");
    },
    false
  );

  child.addEventListener(
    "click",
    function (event) {
      console.log("Child bubbled the event");
    },
    false
  );

  // Add explanation text
  const explanation = document.createElement("div");
  explanation.innerHTML = `
    <h2>Event Capturing Example</h2>
    <p>Click on the innermost pink box to see event capturing in action.</p>
    <p>Check the console to see the order of event execution.</p>
    <p>When clicking on the innermost element, events will fire in this order:</p>
    <ol>
      <li>Body captured the event</li>
      <li>Container captured the event</li>
      <li>Parent captured the event</li>
      <li>Child captured the event</li>
      <li>Child bubbled the event</li>
      <li>Parent bubbled the event</li>
      <li>Container bubbled the event</li>
      <li>Body bubbled the event</li>
    </ol>
  `;
  document.body.insertBefore(explanation, container);

  // Function to stop event propagation example
  const stopPropagationExample = document.createElement("div");
  stopPropagationExample.innerHTML = `
    <h2>Stopping Event Propagation</h2>
    <div id="stop-container" style="padding: 20px; background-color: #ffcccc;">
      Container (with stopPropagation)
      <div id="stop-child" style="padding: 20px; background-color: #ccccff;">
        Child (Click me)
      </div>
    </div>
  `;
  document.body.appendChild(stopPropagationExample);

  // Add event listeners with stopPropagation
  document.getElementById("stop-container").addEventListener(
    "click",
    function (event) {
      console.log("Stop Container captured the event");
    },
    true
  );

  document.getElementById("stop-child").addEventListener(
    "click",
    function (event) {
      console.log("Stop Child captured the event");
      event.stopPropagation(); // Stop the event from further propagating
      console.log("Event propagation stopped!");
    },
    true
  );

  document.getElementById("stop-container").addEventListener(
    "click",
    function (event) {
      console.log(
        "This will not execute during capturing because propagation was stopped"
      );
    },
    false
  );
});
