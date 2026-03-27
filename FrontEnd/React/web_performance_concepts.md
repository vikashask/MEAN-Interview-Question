# Web Performance and Rendering Concepts

- Critical Rendering Path - HTML examples showing how to defer non-critical CSS and JavaScript
  Core Web Vitals - Code examples for fixing LCP, CLS, and INP issues
- HTTP Caching - Express.js server example with cache headers and validation
- Content Negotiation - Node.js example showing language negotiation and Vary header usage
- Lazy Loading - Already had basic examples (kept as is)
- Bundle Splitting - React route-based and component-based splitting examples
- Critical CSS - HTML example with inline critical CSS and build tool usage
- Essential State Model - React examples comparing bad vs. good state loading patterns
- Reducer Pattern - Already had a good example (kept as is)
- Windowing - react-window example comparing performance with/without virtualization
- Server Side Rendering - Next.js and Express.js SSR examples
- Partial Pre-rendering - Next.js 14+ example with Suspense boundaries
- Rehydration - Examples showing hydration mismatch issues and solutions
- Server Side Components - Next.js App Router example with database access
- Microfrontends - Module Federation and iframe integration examples

This document explains various concepts related to web performance, rendering, and architecture.

## 🎯 Critical Rendering Path

The Critical Rendering Path (CRP) is the sequence of steps a browser goes through to convert HTML, CSS, and JavaScript into pixels on the screen. Understanding and optimizing this path is crucial for improving page load performance and providing a better user experience.

The process consists of the following key steps:

1.  **Document Object Model (DOM) Construction**: The browser parses the HTML document and builds the DOM tree. The DOM represents the page's content and structure.

2.  **CSS Object Model (CSSOM) Construction**: The browser parses the CSS files and inline styles to build the CSSOM tree. The CSSOM represents the styles associated with the DOM elements. CSS is **render-blocking**, which means the browser cannot render the page until it has downloaded and parsed all the CSS.

3.  **Render Tree Construction**: The browser combines the DOM and CSSOM into a Render Tree. This tree contains only the nodes required to render the page (e.g., elements with `display: none` are omitted).

4.  **Layout (or Reflow)**: The browser calculates the size and position of each object in the render tree. This phase determines the geometry of the page.

5.  **Paint (or Rasterization)**: The browser paints the pixels for each element onto the screen.

### Optimization Strategies:

- **Minimize Critical Resources**: Reduce the number of files that block rendering. This can be done by deferring the download of non-critical CSS and JavaScript.
- **Optimize Resource Order**: Load critical assets as early as possible to shorten the critical path length.
- **Reduce Resource Size**: Minify HTML, CSS, and JavaScript files to reduce download times.

### Example:

```html
<!-- Bad: Render-blocking CSS -->
<link rel="stylesheet" href="styles.css" />
<link rel="stylesheet" href="print.css" />

<!-- Good: Defer non-critical CSS -->
<link rel="stylesheet" href="critical.css" />
<link
  rel="preload"
  href="styles.css"
  as="style"
  onload="this.onload=null;this.rel='stylesheet'"
/>
<link rel="stylesheet" href="print.css" media="print" />

<!-- Defer non-critical JavaScript -->
<script src="analytics.js" defer></script>
```

## ❤️ Core Web Vitals

Core Web Vitals are a set of standardized metrics from Google that help developers understand and improve the user experience of a web page. They are a subset of Web Vitals and are crucial for search engine optimization (SEO), as Google uses them as a ranking factor.

The three main Core Web Vitals are:

1.  **Largest Contentful Paint (LCP)**: Measures the _loading performance_ of a page. Specifically, it reports the render time of the largest image or text block visible within the viewport. A good LCP score is **2.5 seconds or less**.

2.  **Interaction to Next Paint (INP)**: Measures the _interactivity and responsiveness_ of a page. It assesses the latency of all user interactions (clicks, taps, key presses) with a page and reports the longest duration. A good INP score is **200 milliseconds or less**.

3.  **Cumulative Layout Shift (CLS)**: Measures the _visual stability_ of a page. It quantifies how much unexpected layout shifts occur as the page loads. A low CLS helps ensure that the user's experience is not disrupted by content moving around unexpectedly. A good CLS score is **0.1 or less**.

Optimizing for these metrics is essential for delivering a high-quality user experience and improving a site's visibility in search results.

### Example Scenarios:

**LCP Issue:**

```html
<!-- Bad: Large unoptimized hero image -->
<img src="hero-5mb.jpg" alt="Hero" />

<!-- Good: Optimized and prioritized -->
<link rel="preload" as="image" href="hero-optimized.webp" />
<img src="hero-optimized.webp" alt="Hero" width="1200" height="600" />
```

**CLS Issue:**

```css
/* Bad: No dimensions specified */
img {
  width: 100%;
}

/* Good: Reserve space to prevent layout shift */
img {
  width: 100%;
  aspect-ratio: 16 / 9;
}
```

**INP Improvement:**

```javascript
// Bad: Heavy synchronous operation
button.addEventListener("click", () => {
  const result = heavyCalculation(); // Blocks main thread
  updateUI(result);
});

// Good: Use debouncing or web workers
button.addEventListener(
  "click",
  debounce(() => {
    requestIdleCallback(() => {
      const result = heavyCalculation();
      updateUI(result);
    });
  }, 300)
);
```

## ♻️ HTTP Caching

HTTP caching is a technique used to store copies of web resources (like HTML pages, images, and files) to reduce server load, decrease network traffic, and improve the perceived performance of a website. When a user requests a resource, the browser or an intermediary cache can serve the stored copy instead of fetching it from the origin server again.

There are two main types of HTTP caches:

- **Private Caches**: These are dedicated to a single user. A browser cache is a common example. It stores resources downloaded by the user, so they are available for subsequent visits.
- **Shared Caches**: These are shared by multiple users. Examples include proxy caches and CDNs (Content Delivery Networks).

### Cache Control Headers

Caching behavior is controlled by HTTP headers sent in the server's response. The most important header is `Cache-Control`.

- `Cache-Control: public`: The response can be stored by any cache (private or shared).
- `Cache-Control: private`: The response can only be stored by a private cache (e.g., the user's browser).
- `Cache-Control: no-store`: The response cannot be cached at all.
- `Cache-Control: no-cache`: The response can be cached, but it must be validated with the origin server before being used.
- `Cache-Control: max-age=<seconds>`: Specifies the maximum amount of time a resource is considered fresh.

### Cache Validation

When a cached resource expires, the browser can ask the server if the resource has changed. This is called validation. If the resource has not changed, the server can respond with a `304 Not Modified` status, saving the need to re-download the entire resource.

### Example:

```javascript
// Express.js server example
app.get("/api/data", (req, res) => {
  // Set caching headers
  res.set({
    "Cache-Control": "public, max-age=3600", // Cache for 1 hour
    ETag: '"abc123"', // Version identifier
  });

  // Check if client has valid cached version
  if (req.headers["if-none-match"] === '"abc123"') {
    return res.status(304).end(); // Not modified
  }

  res.json({ data: "fresh content" });
});
```

```html
<!-- HTML with cache-busting for static assets -->
<link rel="stylesheet" href="styles.css?v=1.2.3" />
<script src="app.js?v=1.2.3"></script>

<!-- Or use content-based hashing -->
<link rel="stylesheet" href="styles.a3f2b1c.css" />
<script src="app.d4e5f6g.js"></script>
```

## 🤝 Content Negotiation

Content negotiation is an HTTP mechanism that allows a server to serve different versions of a resource (e.g., a document) at the same URI. This enables the client (user agent) to specify which version is best suited for its capabilities.

There are two main types of content negotiation:

1.  **Server-Driven Negotiation (Proactive)**: This is the most common method. The client sends several HTTP headers with its request, indicating its preferences. The server then uses these headers to decide which representation of the resource to return.

    Common headers used for server-driven negotiation include:

    - `Accept`: Specifies the media types (MIME types) the client can handle (e.g., `text/html`, `application/json`).
    - `Accept-Language`: Indicates the preferred language for the response (e.g., `en-US`, `fr`).
    - `Accept-Encoding`: Specifies the content encoding (compression) formats the client can understand (e.g., `gzip`, `br`).

2.  **Agent-Driven Negotiation (Reactive)**: In this approach, the server responds with a list of available representations, and the client chooses one. This is often implemented with a `300 Multiple Choices` response or by using JavaScript to redirect the user to the appropriate version of the resource.

### The `Vary` Header

The `Vary` response header is crucial for content negotiation, especially when caching is involved. It tells caches which request headers the server used to select a representation. This ensures that the cache can correctly serve different versions of the resource to different clients based on their request headers.

### Example:

```javascript
// Node.js/Express server example
app.get("/api/content", (req, res) => {
  const acceptLanguage = req.headers["accept-language"];
  const acceptEncoding = req.headers["accept-encoding"];

  // Serve content based on language preference
  let content;
  if (acceptLanguage.includes("es")) {
    content = { message: "Hola Mundo" };
  } else if (acceptLanguage.includes("fr")) {
    content = { message: "Bonjour le monde" };
  } else {
    content = { message: "Hello World" };
  }

  // Tell caches to vary responses based on these headers
  res.set({
    Vary: "Accept-Language, Accept-Encoding",
    "Content-Type": "application/json",
  });

  // Apply compression if supported
  if (acceptEncoding.includes("gzip")) {
    res.set("Content-Encoding", "gzip");
    // ... compress and send
  }

  res.json(content);
});
```

## 🦥 Lazy Loading

Lazy loading is a performance optimization strategy that defers the loading of non-critical resources until they are actually needed. This can significantly improve the initial page load time by reducing the amount of data that needs to be downloaded and processed upfront.

### Common Lazy Loading Techniques:

- **Images and Iframes**: Off-screen images and iframes can be loaded as the user scrolls down the page. This can be achieved natively using the `loading="lazy"` attribute on `<img>` and `<iframe>` elements.

  ```html
  <img src="image.jpg" alt="..." loading="lazy" />
  <iframe src="video.html" title="..." loading="lazy"></iframe>
  ```

- **JavaScript**: Code splitting can be used to break up large JavaScript bundles into smaller chunks that are loaded on demand. This is often done using dynamic `import()` expressions.

- **CSS**: Non-critical CSS can be loaded asynchronously to avoid blocking the rendering of the page.

- **Fonts**: Web fonts can be loaded only when they are needed, using techniques like the CSS `font-display` property or the Font Loading API.

### Benefits of Lazy Loading:

- **Faster Initial Page Load**: By reducing the number of resources loaded initially, the page becomes interactive much faster.
- **Reduced Resource Consumption**: Users with slower network connections or limited data plans benefit from not having to download resources they may never see.
- **Improved User Experience**: A faster-loading page leads to a better overall user experience.

## ✂️ Bundle Splitting

Bundle splitting is a technique used by modern JavaScript bundlers (like Webpack, Rollup, and Parcel) to split a large bundle of code into smaller, more manageable chunks. Instead of serving a single, monolithic JavaScript file to the user, the application can load these smaller bundles on demand.

### Why is Bundle Splitting Important?

- **Improved Performance**: Smaller initial bundles mean faster download, parsing, and execution times. This leads to a quicker First Contentful Paint (FCP) and Time to Interactive (TTI).
- **Efficient Caching**: When you update your code, only the bundles that have changed need to be re-downloaded by the user, not the entire application.
- **On-Demand Loading**: Code that is not needed for the initial page load (e.g., for other routes or features) can be loaded lazily, only when the user needs it.

### Common Bundle Splitting Strategies:

- **Route-Based Splitting**: Create a separate bundle for each route or page in your application. The code for a specific page is only loaded when the user navigates to it.
- **Component-Based Splitting**: Isolate large components (like a complex modal or a heavy third-party library) into their own bundles and load them lazily.

Modern frameworks and build tools often provide easy ways to implement bundle splitting, typically using dynamic `import()` syntax.

### Example:

**Route-Based Splitting with React:**

```javascript
import React, { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

// Lazy load route components
const Home = lazy(() => import("./pages/Home"));
const About = lazy(() => import("./pages/About"));
const Dashboard = lazy(() => import("./pages/Dashboard"));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<div>Loading...</div>}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

**Component-Based Splitting:**

```javascript
import React, { useState } from "react";

function ProductPage() {
  const [showModal, setShowModal] = useState(false);
  const [Modal, setModal] = useState(null);

  const handleOpenModal = async () => {
    // Only load the modal component when needed
    const { default: ModalComponent } = await import("./HeavyModal");
    setModal(() => ModalComponent);
    setShowModal(true);
  };

  return (
    <div>
      <button onClick={handleOpenModal}>Open Modal</button>
      {showModal && Modal && <Modal onClose={() => setShowModal(false)} />}
    </div>
  );
}
```

## 🚨 Critical CSS

Critical CSS is the minimum amount of CSS required to render the visible part of a web page (the "above-the-fold" content). By inlining the critical CSS directly into the HTML document, the browser can start rendering the page immediately without having to wait for an external CSS file to download.

### How it Works:

1.  **Identify Critical CSS**: The first step is to determine which CSS rules are necessary to style the above-the-fold content. This can be a complex process, but there are automated tools available to help.

2.  **Inline Critical CSS**: The identified critical CSS is then placed inside a `<style>` tag in the `<head>` of the HTML document.

3.  **Load Remaining CSS Asynchronously**: The rest of the CSS (the non-critical CSS) is loaded asynchronously, so it doesn't block the initial rendering of the page. This can be done using JavaScript or by using `<link rel="preload">` with an `onload` event.

### Benefits of Critical CSS:

- **Faster First Contentful Paint (FCP)**: By eliminating the render-blocking request for the main CSS file, the browser can paint content on the screen much faster.
- **Improved Perceived Performance**: Users see content sooner, which makes the page feel faster, even if the full page load time is the same.
- **Better User Experience**: A faster-loading page leads to a better overall user experience and can reduce bounce rates.

### Example:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My Website</title>

    <!-- Inline critical CSS for above-the-fold content -->
    <style>
      /* Critical CSS */
      body {
        margin: 0;
        font-family: Arial, sans-serif;
      }
      .header {
        background: #333;
        color: white;
        padding: 20px;
      }
      .hero {
        height: 400px;
        background: #f0f0f0;
      }
      .hero h1 {
        font-size: 48px;
        margin: 0;
      }
    </style>

    <!-- Preload and async load non-critical CSS -->
    <link
      rel="preload"
      href="styles.css"
      as="style"
      onload="this.onload=null;this.rel='stylesheet'"
    />
    <noscript><link rel="stylesheet" href="styles.css" /></noscript>
  </head>
  <body>
    <header class="header">My Site</header>
    <div class="hero">
      <h1>Welcome!</h1>
    </div>
    <!-- Rest of content -->
  </body>
</html>
```

**Using a tool to extract critical CSS:**

```javascript
// Using critical package in build process
const critical = require("critical");

critical.generate({
  inline: true,
  base: "dist/",
  src: "index.html",
  target: "index-critical.html",
  width: 1300,
  height: 900,
});
```

## 💾 Essential State Model

"Essential State Model" is not a standard industry term but likely refers to the practice of identifying and managing only the **minimum essential state** required for a page or component to render its initial, critical view. The goal is to avoid loading a large, comprehensive state object upfront, which can slow down the initial render and hydration process.

### Core Principles:

1.  **Identify Essential State**: Determine the bare minimum data needed to render the "above-the-fold" content or the most critical parts of the UI.

2.  **Prioritize Essential State**: Load this essential state first. In Server-Side Rendering (SSR), this state would be fetched on the server and embedded in the initial HTML payload sent to the client.

3.  **Defer Non-Essential State**: Any state that is not immediately needed (e.g., for user interactions, content below the fold, or less critical UI elements) should be loaded asynchronously after the initial render is complete.

### Benefits:

- **Faster Time to Interactive (TTI)**: By reducing the amount of data that needs to be processed on the client for the initial render, the page becomes interactive sooner.
- **Smaller Initial Payload**: Sending less data over the network results in a faster initial load, especially on slow connections.
- **Improved SSR/SSG Performance**: This model is particularly effective with server-rendering strategies, as it minimizes the amount of data that needs to be serialized and sent to the client for hydration.

### Example:

```javascript
// Bad: Loading all data upfront
function ProductPage({ productId }) {
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [relatedProducts, setRelatedProducts] = useState([]);

  useEffect(() => {
    // Loading everything at once - slow initial render
    Promise.all([
      fetchProduct(productId),
      fetchReviews(productId),
      fetchRecommendations(productId),
      fetchRelatedProducts(productId),
    ]).then(([prod, rev, rec, rel]) => {
      setProduct(prod);
      setReviews(rev);
      setRecommendations(rec);
      setRelatedProducts(rel);
    });
  }, [productId]);

  return <div>...</div>;
}

// Good: Load essential state first, defer non-essential
function ProductPage({ productId }) {
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    // Load essential product data immediately
    fetchProduct(productId).then(setProduct);
  }, [productId]);

  useEffect(() => {
    // Defer loading of below-the-fold content
    if (product) {
      setTimeout(() => {
        fetchReviews(productId).then(setReviews);
      }, 100);
    }
  }, [product, productId]);

  return (
    <div>
      {product && <ProductDetails product={product} />}
      {reviews.length > 0 && <Reviews reviews={reviews} />}
    </div>
  );
}
```

## π Reducer Pattern

The Reducer Pattern is a state management pattern used to handle complex state logic in applications. It's particularly popular in the React ecosystem (with the `useReducer` hook and libraries like Redux), but the concept is applicable to any JavaScript application.

The core idea is to consolidate all state update logic into a single function called a **reducer**. Instead of updating the state directly, you dispatch **actions** that describe what happened. The reducer then takes the current state and an action, and returns the new state.

### Core Components:

1.  **State**: The current state of the application or component.
2.  **Action**: A plain JavaScript object that describes an event or user interaction. It typically has a `type` property (a string) and an optional payload with additional data.
3.  **Reducer**: A pure function that takes the current `state` and an `action` as arguments and returns the next `state`. It should not mutate the original state.
4.  **Dispatch**: A function that sends an action to the reducer.

### Example with React's `useReducer`:

```javascript
function tasksReducer(tasks, action) {
  switch (action.type) {
    case "added":
    // ... return new state with added task
    case "changed":
    // ... return new state with changed task
    case "deleted":
    // ... return new state without deleted task
    default:
      throw Error("Unknown action: " + action.type);
  }
}

function MyComponent() {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);

  function handleAddTask(text) {
    dispatch({ type: "added", text: text });
  }
  // ...
}
```

### Benefits:

- **Centralized Logic**: All state update logic is in one place, making it easier to understand and maintain.
- **Predictable State Changes**: By using pure functions, state changes become more predictable and easier to debug.
- **Separation of Concerns**: It separates the "what happened" (dispatching actions) from the "how it happened" (the reducer logic).

## 🖼️ Windowing

Windowing, also known as **list virtualization**, is a performance optimization technique used to efficiently render large lists of data. Instead of rendering all the items in a list at once, which can be very slow and consume a lot of memory, windowing only renders the items that are currently visible in the user's viewport (the "window").

### How it Works:

As the user scrolls through the list, the window of visible items moves. Items that scroll out of view are recycled or replaced by new items that are scrolling into view. This keeps the number of DOM elements on the page small and constant, regardless of the size of the list.

### Key Concepts:

- **Window**: The visible portion of the list.
- **Recycling**: Reusing the DOM nodes of items that have scrolled out of view to display new items that are scrolling into view.

### Benefits of Windowing:

- **Improved Rendering Performance**: By rendering only a small subset of the list, the initial render time is significantly reduced.
- **Smoother Scrolling**: With fewer DOM elements to manage, scrolling through the list is much smoother and more responsive.
- **Reduced Memory Usage**: Windowing dramatically reduces the memory footprint of the application, especially when dealing with very large lists.

Libraries like `react-window` and `react-virtualized` are commonly used to implement windowing in React applications.

### Example:

```javascript
import { FixedSizeList } from "react-window";

// Without windowing - renders all 10,000 items (slow!)
function SlowList({ items }) {
  return (
    <div>
      {items.map((item, index) => (
        <div key={index} style={{ height: 50 }}>
          {item.name}
        </div>
      ))}
    </div>
  );
}

// With windowing - only renders visible items (fast!)
function FastList({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}>{items[index].name}</div>
  );

  return (
    <FixedSizeList
      height={600} // Viewport height
      itemCount={items.length} // Total items: 10,000
      itemSize={50} // Height of each item
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
}

// Usage
const largeDataset = Array.from({ length: 10000 }, (_, i) => ({
  id: i,
  name: `Item ${i}`,
}));

<FastList items={largeDataset} />;
```

**Performance Comparison:**

- Without windowing: Renders 10,000 DOM nodes (~500ms initial render)
- With windowing: Renders ~12 DOM nodes (~50ms initial render)

## 🔥 Server Side Rendering

Server-Side Rendering (SSR) is a rendering technique where the server generates the full HTML for a page in response to a browser request. This is in contrast to Client-Side Rendering (CSR), where the browser downloads a minimal HTML file and then uses JavaScript to render the rest of the page.

### How it Works:

1.  A user or search engine crawler makes a request to a URL.
2.  The server fetches any necessary data, renders the React (or other framework) components into an HTML string, and sends this fully rendered HTML back to the client.
3.  The browser can immediately display the page, as it has all the necessary HTML.
4.  The client-side JavaScript bundle is then downloaded and executed, a process called **hydration**, which attaches event handlers and makes the page interactive.

### Benefits of SSR:

- **Faster First Contentful Paint (FCP)**: Since the browser receives a fully rendered HTML page, it can display content to the user much faster than with CSR.
- **Improved SEO**: Search engine crawlers can easily index the content of the page because the HTML is fully formed on the initial request.

### Drawbacks of SSR:

- **Slower Time to First Byte (TTFB)**: The server has to do more work to generate the HTML, which can lead to a slower initial response time.
- **More Complex Development**: SSR applications can be more complex to build and deploy than purely client-side applications.
- **Full Page Reloads**: Navigating between pages often requires a full page reload, which can feel slower than the near-instant transitions of a Single-Page Application (SPA).

### Example:

**Next.js SSR:**

```javascript
// pages/product/[id].js
import { getProduct } from "@/lib/api";

// This function runs on the server for each request
export async function getServerSideProps(context) {
  const { id } = context.params;

  // Fetch data on the server
  const product = await getProduct(id);

  // Pass data to the page component as props
  return {
    props: {
      product,
    },
  };
}

// This component receives the server-fetched data
export default function ProductPage({ product }) {
  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p>Price: ${product.price}</p>
    </div>
  );
}
```

**Express.js SSR with React:**

```javascript
import express from "express";
import React from "react";
import { renderToString } from "react-dom/server";
import App from "./App";

const server = express();

server.get("*", async (req, res) => {
  // Fetch data on server
  const data = await fetchData();

  // Render React component to HTML string
  const html = renderToString(<App data={data} />);

  // Send fully rendered HTML to client
  res.send(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>My App</title>
        <script>
          window.__INITIAL_DATA__ = ${JSON.stringify(data)};
        </script>
      </head>
      <body>
        <div id="root">${html}</div>
        <script src="/bundle.js"></script>
      </body>
    </html>
  `);
});

server.listen(3000);
```

## 🌗 Partial Pre-rendering

Partial Pre-rendering (PPR) is a modern rendering technique, prominently featured in Next.js, that combines the best of static site generation (SSG) and server-side rendering (SSR). It allows a page to be mostly pre-rendered at build time, with dynamic parts (or "holes") that are streamed in at request time.

### How it Works:

1.  **Static Shell**: At build time, a static HTML "shell" of the page is generated. This shell contains all the static content of the page.

2.  **Dynamic Holes**: Any dynamic content is replaced with fallback UI (e.g., a loading spinner). This is typically achieved by wrapping dynamic components in a `<Suspense>` boundary.

3.  **Request Time**: When a user requests the page, the static shell is served immediately, providing a very fast First Contentful Paint (FCP).

4.  **Streaming**: The dynamic parts of the page are then rendered on the server and streamed to the client, filling in the "holes" in the static shell.

### Benefits of Partial Pre-rendering:

- **Fast Initial Load**: Users get an instant response with the static shell, which greatly improves perceived performance.
- **Dynamic Content**: The page can still contain dynamic, personalized, or real-time content.
- **Good SEO**: The initial static shell is easily crawlable by search engines.
- **Reduced Server Load**: Since most of the page is static, the server only needs to render the small dynamic parts at request time.

### Example:

```javascript
// Next.js 14+ with Partial Pre-rendering
import { Suspense } from "react";
import { StaticHeader } from "@/components/StaticHeader";
import { DynamicUserProfile } from "@/components/DynamicUserProfile";
import { StaticFooter } from "@/components/StaticFooter";

export default function Dashboard() {
  return (
    <div>
      {/* Static: Pre-rendered at build time */}
      <StaticHeader />

      <main>
        <h1>Dashboard</h1>

        {/* Dynamic: Streamed at request time */}
        <Suspense fallback={<div>Loading user data...</div>}>
          <DynamicUserProfile />
        </Suspense>

        {/* Static: Pre-rendered at build time */}
        <div className="static-content">
          <h2>Features</h2>
          <p>This content is static and loads instantly.</p>
        </div>

        {/* Dynamic: Personalized recommendations */}
        <Suspense fallback={<div>Loading recommendations...</div>}>
          <RecommendationsWidget />
        </Suspense>
      </main>

      {/* Static: Pre-rendered at build time */}
      <StaticFooter />
    </div>
  );
}

// Dynamic component that fetches data
async function DynamicUserProfile() {
  const user = await fetchUserData(); // Runs on server at request time

  return (
    <div>
      <h2>Welcome, {user.name}!</h2>
      <p>Last login: {user.lastLogin}</p>
    </div>
  );
}
```

## 💧 Rehydration

Rehydration is the process of making a server-rendered HTML page interactive by attaching the necessary JavaScript event handlers. It's a critical step in the lifecycle of a Server-Side Rendered (SSR) or Static Site Generated (SSG) application.

### How it Works:

1.  **Server-Side Rendering**: The server generates the HTML for a page and sends it to the browser.

2.  **Initial Render**: The browser displays the static HTML, so the user sees the content quickly.

3.  **JavaScript Download**: The browser then downloads the client-side JavaScript bundle.

4.  **Rehydration**: The JavaScript framework (like React) executes on the client. Instead of re-creating the DOM from scratch, it "hydrates" the existing server-rendered HTML by attaching event listeners and setting up the initial application state. This makes the page interactive.

### The Importance of Matching HTML:

For rehydration to work correctly, the HTML generated on the client must match the HTML that was rendered on the server. If there's a mismatch, the framework may have to discard the server-rendered HTML and re-render the entire page on the client, which can cause performance issues and a noticeable flicker.

### Challenges with Rehydration:

- **Hydration Mismatch**: As mentioned above, if the client-side render produces different HTML than the server, it can lead to bugs and performance problems.
- **Time to Interactive (TTI)**: Even though the page is visible, it's not interactive until rehydration is complete. On slow devices or with large JavaScript bundles, this can lead to a frustrating user experience where the user sees a page but can't interact with it.

### Example:

```javascript
// Common hydration mismatch issue
function Clock() {
  // ❌ Bad: Will cause hydration mismatch
  const time = new Date().toLocaleTimeString();

  return <div>Current time: {time}</div>;
  // Server renders one time, client renders different time!
}

// ✅ Good: Two-pass rendering to avoid mismatch
function Clock() {
  const [time, setTime] = useState(null);

  useEffect(() => {
    // Only run on client after hydration
    setTime(new Date().toLocaleTimeString());

    const interval = setInterval(() => {
      setTime(new Date().toLocaleTimeString());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  // Show placeholder during SSR and initial hydration
  if (!time) {
    return <div>Current time: --:--:--</div>;
  }

  return <div>Current time: {time}</div>;
}

// Another example: User-specific content
function UserGreeting() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Don't render user-specific content until client-side
  if (!mounted) {
    return <div>Welcome!</div>;
  }

  const user = getUserFromLocalStorage();
  return <div>Welcome back, {user.name}!</div>;
}
```

## 🛰️ Server Side Components

Server-Side Components (or React Server Components, RSC) are a new paradigm in React that allows components to run exclusively on the server. This is a significant shift from traditional React components, which run on both the server (during SSR) and the client.

### Key Characteristics:

- **Server-Only Execution**: Server Components run only on the server. Their code is never sent to the client, which means they have zero impact on the client-side JavaScript bundle size.
- **Direct Data Access**: Because they run on the server, Server Components can directly access server-side resources like databases, file systems, and internal APIs without needing to make a separate network request.
- **No State or Lifecycle**: Server Components cannot use state (`useState`) or lifecycle effects (`useEffect`) because they do not re-render on the client.
- **Async/Await Support**: Server Components can be `async` functions, allowing you to use `await` for data fetching directly within the component.

### How They Work with Client Components:

In this new model, traditional React components are now called **Client Components**. To use client-side interactivity (like state and effects), you must explicitly mark a component with the `"use client"` directive at the top of the file.

- Server Components can import and render Client Components.
- Client Components _cannot_ import Server Components directly (though they can accept Server Components as props, e.g., `children`).

### Benefits of Server Components:

- **Reduced Bundle Size**: By keeping large dependencies and complex logic on the server, the amount of JavaScript sent to the client is significantly reduced.
- **Improved Performance**: Less JavaScript to download, parse, and execute leads to a faster Time to Interactive (TTI).
- **Simplified Data Fetching**: The data fetching logic can be co-located with the component, making the code easier to understand and maintain.
- **Enhanced Security**: Sensitive data and logic can be kept on the server, preventing it from being exposed to the client.

### Example:

```javascript
// app/page.js - Server Component (default in Next.js App Router)
import db from "@/lib/database";
import { ClientButton } from "./ClientButton";

// This is a Server Component - runs only on server
export default async function HomePage() {
  // Direct database access - no API route needed!
  const posts = await db.query("SELECT * FROM posts ORDER BY date DESC");

  return (
    <div>
      <h1>Blog Posts</h1>
      {posts.map((post) => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
          {/* Pass Server Component as children to Client Component */}
          <ClientButton>
            <LikeCount postId={post.id} />
          </ClientButton>
        </article>
      ))}
    </div>
  );
}

// Nested Server Component
async function LikeCount({ postId }) {
  const likes = await db.query("SELECT COUNT(*) FROM likes WHERE post_id = ?", [
    postId,
  ]);
  return <span>{likes} likes</span>;
}

// ClientButton.js - Client Component
("use client"); // This directive marks it as a Client Component

import { useState } from "react";

export function ClientButton({ children }) {
  const [liked, setLiked] = useState(false);

  return (
    <button onClick={() => setLiked(!liked)}>
      {liked ? "❤️" : "🤍"} {children}
    </button>
  );
}
```

**Key Points:**

- Server Components can use `async/await` directly
- They can access backend resources without API routes
- Client Components need `'use client'` directive
- Server Components can pass data to Client Components via props

## 🧩 Microfrontends

Microfrontends are an architectural pattern for web development where a single application is composed of multiple, independently developed and deployed frontend applications. It extends the concepts of microservices to the frontend.

### Core Idea:

Instead of a large, monolithic frontend codebase, a microfrontends architecture breaks the application down into smaller, business-domain-oriented pieces. Each piece (or microfrontend) is owned by a specific team, which has end-to-end responsibility for their feature, from the UI to the backend.

### Key Principles:

- **Technology Agnostic**: Each team can choose its own technology stack, allowing for greater flexibility and easier adoption of new technologies.
- **Isolated Code**: Microfrontends are developed in isolation and should not share a runtime or global state.
- **Independent Deployment**: Each microfrontend can be deployed independently, which allows for faster, more frequent releases.
- **Autonomous Teams**: The architecture enables small, autonomous teams to own their features and work independently.

### Common Integration Approaches:

- **Server-Side Composition**: The page is assembled on the server by fetching and combining the HTML from different microfrontends.
- **Build-Time Integration**: The microfrontends are published as packages and installed as dependencies in a container application.
- **Run-Time Integration**: The microfrontends are loaded and composed in the browser at runtime. This can be done using iframes, JavaScript, or Web Components.

### Downsides:

- **Increased Payload Size**: Duplication of dependencies across microfrontends can lead to a larger overall application size.
- **Operational Complexity**: Managing multiple repositories, build pipelines, and deployments can be more complex than with a monolith.
- **Governance**: Ensuring consistency in user experience and technical standards across teams can be challenging.

### Example:

**Using Module Federation (Webpack 5):**

```javascript
// Container App - webpack.config.js
module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: "container",
      remotes: {
        header: "header@http://localhost:3001/remoteEntry.js",
        products: "products@http://localhost:3002/remoteEntry.js",
        cart: "cart@http://localhost:3003/remoteEntry.js",
      },
      shared: ["react", "react-dom"],
    }),
  ],
};

// Container App - App.js
import React, { lazy, Suspense } from "react";

const Header = lazy(() => import("header/Header"));
const ProductList = lazy(() => import("products/ProductList"));
const Cart = lazy(() => import("cart/Cart"));

function App() {
  return (
    <div>
      <Suspense fallback={<div>Loading...</div>}>
        <Header />
        <ProductList />
        <Cart />
      </Suspense>
    </div>
  );
}
```

**Header Microfrontend - webpack.config.js:**

```javascript
module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: "header",
      filename: "remoteEntry.js",
      exposes: {
        "./Header": "./src/Header",
      },
      shared: ["react", "react-dom"],
    }),
  ],
};
```

**Using iframes (simpler but less flexible):**

```html
<!-- Container page -->
<!DOCTYPE html>
<html>
  <body>
    <!-- Header microfrontend -->
    <iframe
      src="https://header.example.com"
      style="width: 100%; height: 80px; border: none;"
    ></iframe>

    <!-- Main content microfrontend -->
    <iframe
      src="https://products.example.com"
      style="width: 100%; height: 600px; border: none;"
    ></iframe>

    <!-- Footer microfrontend -->
    <iframe
      src="https://footer.example.com"
      style="width: 100%; height: 100px; border: none;"
    ></iframe>
  </body>
</html>
```
