# Browser APIs Interview Questions

## DOM (Document Object Model)

### What is the DOM?

The DOM is a programming interface for web documents. It represents the page so that programs can change the document structure, style, and content. The DOM represents the document as nodes and objects so that programming languages like JavaScript can interact with the page.

### Explain event delegation

Event delegation is a technique where you add a single event listener to a parent element instead of adding event listeners to multiple child elements. It takes advantage of event bubbling, where events propagate up from the target element to its ancestors.

```javascript
// Instead of this:
document.querySelectorAll(".button").forEach((button) => {
  button.addEventListener("click", handleClick);
});

// Do this:
document.getElementById("parent").addEventListener("click", (e) => {
  if (e.target.matches(".button")) {
    handleClick(e);
  }
});
```

### What is event bubbling and event capturing?

- **Event Bubbling**: Events start at the target element and "bubble up" through ancestors.
- **Event Capturing**: Events start at the top of the DOM tree and "capture down" to the target element.

You can specify which phase to use in the `addEventListener` method with the third parameter (`true` for capturing, `false` or omitted for bubbling).

### How do you create, append and remove elements from the DOM?

```javascript
// Create an element
const div = document.createElement("div");

// Set attributes/content
div.className = "new-element";
div.textContent = "Hello world";

// Append to DOM
document.body.appendChild(div);

// Remove from DOM
div.remove();
// Or
div.parentNode.removeChild(div);
```

## BOM (Browser Object Model)

### What is the difference between DOM and BOM?

- **DOM (Document Object Model)** represents the content of the webpage and provides methods to interact with it.
- **BOM (Browser Object Model)** represents the browser window and provides methods to interact with it, including browser history, location, screen, and navigator objects.

### Explain the window object

The `window` object represents the browser window and serves as the global object for JavaScript in the browser. It contains properties like `document`, `location`, `history`, `localStorage`, etc.

### What is the navigator object?

The `navigator` object contains information about the browser, such as browser name, version, OS platform, and user agent.

```javascript
// Check if browser supports geolocation
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition((position) => {
    console.log(position.coords.latitude, position.coords.longitude);
  });
}
```

## Storage APIs

### Describe localStorage and sessionStorage

Both are part of the Web Storage API but differ in persistence:

- **localStorage**: Data persists until explicitly deleted, even after closing browser
- **sessionStorage**: Data persists only for the duration of the page session

```javascript
// localStorage example
localStorage.setItem("key", "value");
const value = localStorage.getItem("key");
localStorage.removeItem("key");
localStorage.clear(); // clear all data

// sessionStorage works the same way
sessionStorage.setItem("key", "value");
```

### What are cookies? How do they differ from localStorage?

Cookies are small pieces of data stored by the browser that are sent to the server with every HTTP request.

Differences from localStorage:

- Size limit (4KB for cookies vs 5MB for localStorage)
- Automatically sent with HTTP requests
- Can set expiration dates
- Can be httpOnly (inaccessible to JavaScript)

```javascript
// Create a cookie that expires in 7 days
document.cookie =
  "username=John; expires=" +
  new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toUTCString();
```

### What is IndexedDB?

IndexedDB is a low-level API for client-side storage of significant amounts of structured data, including files/blobs. It uses indexes to enable high-performance searches and supports transactions for reliability.

## Fetch API & AJAX

### What is the Fetch API and how does it differ from XMLHttpRequest?

The Fetch API provides a more powerful and flexible feature set than XMLHttpRequest, with a cleaner, promise-based interface.

```javascript
// Fetch example
fetch("https://api.example.com/data")
  .then((response) => {
    if (!response.ok) throw new Error("Network response was not ok");
    return response.json();
  })
  .then((data) => console.log(data))
  .catch((error) => console.error("Error:", error));

// XMLHttpRequest equivalent
const xhr = new XMLHttpRequest();
xhr.open("GET", "https://api.example.com/data");
xhr.onload = function () {
  if (xhr.status === 200) {
    const data = JSON.parse(xhr.responseText);
    console.log(data);
  } else {
    console.error("Error:", xhr.statusText);
  }
};
xhr.onerror = function () {
  console.error("Network Error");
};
xhr.send();
```

### Explain CORS (Cross-Origin Resource Sharing)

CORS is a security mechanism that allows a web page from one domain to request resources from another domain. Browsers enforce the same-origin policy, which restricts how resources from one origin can interact with resources from another.

The server must include appropriate CORS headers (like `Access-Control-Allow-Origin`) to allow cross-origin requests.

## History API

### How do single page applications (SPAs) use the History API?

SPAs use the History API to change the URL without triggering a page reload:

```javascript
// Navigate to a new "page" without reloading
history.pushState({ page: "about" }, "About Page", "/about");

// Replace current history entry
history.replaceState({ page: "about" }, "About Page", "/about");

// Listen for navigation events (back/forward)
window.addEventListener("popstate", (event) => {
  console.log(event.state);
});
```

## Web Workers

### What are Web Workers?

Web Workers allow running scripts in background threads, separate from the main execution thread. This prevents blocking the UI during intensive calculations.

```javascript
// Main script
const worker = new Worker("worker.js");
worker.postMessage({ data: "some data" });
worker.onmessage = function (e) {
  console.log("Message received from worker:", e.data);
};

// worker.js
self.onmessage = function (e) {
  const result = performComplexCalculation(e.data);
  self.postMessage(result);
};
```

## Geolocation API

### How do you access a user's location using JavaScript?

```javascript
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(
    // Success callback
    (position) => {
      console.log(`Latitude: ${position.coords.latitude}`);
      console.log(`Longitude: ${position.coords.longitude}`);
    },
    // Error callback
    (error) => {
      console.error("Error getting location:", error.message);
    },
    // Options
    {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0,
    }
  );
}
```

## Notification API

### How can you display browser notifications?

```javascript
// Request permission first
Notification.requestPermission().then((permission) => {
  if (permission === "granted") {
    const notification = new Notification("Title", {
      body: "This is the notification body",
      icon: "/path/to/icon.png",
    });

    notification.onclick = () => {
      window.focus();
      notification.close();
    };
  }
});
```

## Canvas API

### What is the Canvas API used for?

The Canvas API provides a means for drawing graphics via JavaScript and the HTML `<canvas>` element. It can be used for animations, game graphics, data visualization, photo manipulation, and real-time video processing.

```javascript
const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");

// Draw a rectangle
ctx.fillStyle = "red";
ctx.fillRect(10, 10, 100, 100);

// Draw text
ctx.font = "24px Arial";
ctx.fillStyle = "white";
ctx.fillText("Hello world", 20, 60);
```

## Service Workers

### What are Service Workers and how are they used?

Service Workers are scripts that run in the background, separate from a web page, enabling features like offline capabilities, background sync, and push notifications.

```javascript
// Register a service worker
if ("serviceWorker" in navigator) {
  navigator.serviceWorker
    .register("/service-worker.js")
    .then((registration) => {
      console.log("Service Worker registered with scope:", registration.scope);
    })
    .catch((error) => {
      console.error("Service Worker registration failed:", error);
    });
}

// In service-worker.js
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open("v1").then((cache) => {
      return cache.addAll([
        "/",
        "/styles/main.css",
        "/script/main.js",
        "/images/logo.png",
      ]);
    })
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

## WebSockets API

### What are WebSockets and how do they differ from HTTP?

WebSockets provide a persistent connection between a client and server, allowing bidirectional communication with lower overhead than HTTP.

```javascript
const socket = new WebSocket("wss://example.com/socketserver");

socket.onopen = (event) => {
  socket.send("Hello Server!");
};

socket.onmessage = (event) => {
  console.log("Message from server:", event.data);
};

socket.onclose = (event) => {
  console.log("Connection closed");
};

socket.onerror = (error) => {
  console.error("WebSocket error:", error);
};
```

## Intersection Observer API

### What is the Intersection Observer API used for?

The Intersection Observer API provides a way to asynchronously observe changes in the intersection of a target element with an ancestor element or the viewport. It's commonly used for lazy-loading images, implementing "infinite scroll", and triggering animations when elements become visible.

```javascript
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        // Element is visible in viewport
        entry.target.classList.add("visible");
        // Stop observing once animation is triggered
        observer.unobserve(entry.target);
      }
    });
  },
  {
    root: null, // viewport
    threshold: 0.1, // 10% of element is visible
  }
);

// Start observing elements
document.querySelectorAll(".animate-on-scroll").forEach((el) => {
  observer.observe(el);
});
```

## Performance API

### How can you measure page performance using JavaScript?

The Performance API provides access to performance-related information about the current page:

```javascript
// Navigation Timing API
const pageNav = performance.getEntriesByType("navigation")[0];
console.log("Page load time:", pageNav.loadEventEnd - pageNav.startTime);

// Resource Timing API
const resources = performance.getEntriesByType("resource");
resources.forEach((resource) => {
  console.log(`${resource.name}: ${resource.duration}ms`);
});

// User Timing API
performance.mark("start-calculation");
// ... do something
performance.mark("end-calculation");
performance.measure("calculation", "start-calculation", "end-calculation");
const measure = performance.getEntriesByName("calculation")[0];
console.log(`Calculation took ${measure.duration}ms`);
```

## Media APIs

### How do you work with audio and video in the browser?

HTML5 provides `<audio>` and `<video>` elements that can be controlled via JavaScript:

```javascript
const video = document.querySelector("video");

// Play/pause
video.play();
video.pause();

// Change source
video.src = "movie.mp4";

// Listen for events
video.addEventListener("ended", () => {
  console.log("Video playback finished");
});

// MediaRecorder API for recording media
if (navigator.mediaDevices) {
  navigator.mediaDevices
    .getUserMedia({ audio: true, video: true })
    .then((stream) => {
      const mediaRecorder = new MediaRecorder(stream);
      const chunks = [];

      mediaRecorder.ondataavailable = (e) => {
        chunks.push(e.data);
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: "video/webm" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "recording.webm";
        a.click();
      };

      mediaRecorder.start();
      setTimeout(() => mediaRecorder.stop(), 5000); // 5 seconds
    });
}
```

## File API

### How can you work with files using JavaScript?

The File API allows web applications to interact with files on the user's device:

```javascript
// From file input
const fileInput = document.querySelector('input[type="file"]');
fileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  console.log(`File name: ${file.name}`);
  console.log(`File type: ${file.type}`);
  console.log(`File size: ${file.size} bytes`);

  // Read file contents
  const reader = new FileReader();

  reader.onload = (e) => {
    console.log("File contents:", e.target.result);
  };

  reader.onerror = (e) => {
    console.error("File reading failed:", e.target.error);
  };

  // Read as text, dataURL, or ArrayBuffer depending on file type
  reader.readAsText(file); // for text files
  // reader.readAsDataURL(file); // for images
  // reader.readAsArrayBuffer(file); // for binary data
});

// File saving
function saveFile(data, filename, type) {
  const blob = new Blob([data], { type: type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

saveFile("Hello World", "hello.txt", "text/plain");
```

## Security-Related Questions

### What is Content Security Policy (CSP)?

Content Security Policy is a security standard that helps prevent cross-site scripting (XSS) and other code injection attacks by allowing website owners to specify which sources of content browsers should be allowed to load.

### What are the security concerns with localStorage vs cookies?

- **localStorage**: Vulnerable to XSS attacks since any JavaScript can access it; no automatic expiration
- **Cookies**: Can be marked as httpOnly to prevent JavaScript access; vulnerable to CSRF attacks unless using SameSite attribute

### How can you protect against XSS attacks?

- Use Content Security Policy
- Sanitize user input
- Escape output when rendering dynamic content
- Use HttpOnly cookies
- Use frameworks that automatically escape content (React, Angular, etc.)

## Advanced Browser APIs

### What is the Web Audio API?

The Web Audio API provides a powerful system for controlling audio on the web, allowing developers to choose audio sources, add effects, create visualizations, and more.

### What is WebGL and how does it differ from Canvas 2D?

WebGL is a JavaScript API for rendering high-performance 3D and 2D graphics within the browser. It's based on OpenGL ES and runs on the GPU, while Canvas 2D is CPU-based and simpler to use but less powerful.

### What is the Battery Status API?

The Battery Status API provides information about the system's battery charge level and lets you be notified by events related to the battery.

```javascript
if (navigator.getBattery) {
  navigator.getBattery().then((battery) => {
    console.log(`Battery level: ${battery.level * 100}%`);
    console.log(`Charging: ${battery.charging}`);

    battery.addEventListener("levelchange", () => {
      console.log(`Battery level changed: ${battery.level * 100}%`);
    });
  });
}
```
