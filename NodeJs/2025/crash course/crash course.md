# 🟢 Node.js Crash Course: From Zero to Production

## Target Audience

- Developers new to Node.js
- Developers with some JavaScript experience
- Backend or full-stack devs looking to learn Node.js

---

## 1. Introduction to Node.js

- **What is Node.js?**  
  Node.js is a runtime environment that lets you run JavaScript on the server side, outside of a browser.

- **Why use Node.js (vs other backends)?**  
  Node.js is fast, lightweight, and great for handling many simultaneous connections due to its non-blocking, event-driven architecture.

- **Node.js event loop and non-blocking I/O**  
  The event loop lets Node.js handle many tasks asynchronously, making I/O operations efficient and non-blocking.

- **Use cases and real-world examples**  
  Node.js is ideal for real-time apps (chat apps), REST APIs, streaming services, and build tools.

---

## 2. Setting Up Node.js

- **Installing Node.js (Windows, macOS, Linux):**  
  Download from the official site or use a package manager like Homebrew (macOS) or Chocolatey (Windows).

- **Using Node Version Manager (nvm):**  
  NVM lets you install and switch between different Node.js versions easily.

- **Setting up a first project (`npm init`):**  
  Use `npm init` to create a `package.json` file which tracks project dependencies and metadata.

- **Project structure: What files go where?:**  
  Organize code in folders like `routes/`, `controllers/`, `models/`, and keep entry file as `index.js` or `app.js`.

---

## 3. Core Concepts

- Node.js REPL
- Modules (CommonJS, ES6 imports)
- `require`, `exports`, `module.exports`
- Core modules: `fs`, `http`, `os`, `path`, `events`, etc.

_Exercise: Write a script to read/write files and create a simple HTTP server._

---

## 4. Asynchronous Programming

- **Callbacks:**  
  A function passed as an argument to another function and executed after some operation is completed.  
  Example:

  ```js
  function fetchData(callback) {
    setTimeout(() => {
      callback("Data received");
    }, 1000);
  }

  fetchData((data) => {
    console.log(data);
  });
  ```

- **Promises:**  
  An object representing the eventual completion or failure of an async operation.  
  Example:

  ```js
  const fetchData = () => {
    return new Promise((resolve, reject) => {
      setTimeout(() => resolve("Data received"), 1000);
    });
  };

  fetchData().then((data) => console.log(data));
  ```

- **Async/await:**  
  A cleaner syntax to work with Promises, using `async` functions and the `await` keyword.  
  Example:

  ```js
  const fetchData = () => {
    return new Promise((resolve) => {
      setTimeout(() => resolve("Data received"), 1000);
    });
  };

  async function showData() {
    const data = await fetchData();
    console.log(data);
  }

  showData();
  ```

- **Error handling:**  
  Use `.catch()` with Promises or `try...catch` with async/await to manage errors.  
  Example:
  ```js
  async function showData() {
    try {
      const data = await fetchData();
      console.log(data);
    } catch (error) {
      console.error("Error:", error);
    }
  }
  ```

_Exercise: Convert callback-based code to Promises and then to async/await._

---

## 5. Building a Simple HTTP Server

- Using the `http` module
- Request and response objects
- Handling routes
- Serving static files

_Exercise: Serve a basic HTML file with Node.js._

---

## 6. NPM & Dependency Management

- What is npm?
- Installing packages (local vs global)
- `package.json` and `package-lock.json`
- Semantic Versioning
- Popular packages: `express`, `dotenv`, `nodemon`

---

## 7. Express.js Fundamentals

- Why Express?
- Setting up Express
- Routing (GET, POST, PUT, DELETE)
- Middleware
- Handling JSON and forms
- Error handling

_Project: Build a CRUD REST API for a "tasks" or "users" resource._

---

## 8. Working with Databases

- Introduction to MongoDB (use Mongoose or native driver)
- Connecting to MongoDB
- CRUD operations with MongoDB
- Data modeling

_Project: Connect Express API to MongoDB and persist data._

---

## 9. Authentication & Authorization

- What is authentication vs. authorization?
- JWT tokens (jsonwebtoken library)
- Secure password storage (bcrypt)
- Middleware for protecting routes

---

## 10. Environment Variables & Configuration

- Using `dotenv`
- Creating `.env` files
- Best practices for managing secrets

---

## 11. Error Handling & Logging

- Centralized error handlers
- Logging (using `winston` or similar)

---

## 12. Writing Unit Tests

- Why test?
- Using Jest or Mocha
- Testing routes, controllers, and services
- Mocking data and dependencies

---

## 13. Building & Running in Production

- Using PM2 to run apps
- Environment configs (dev, prod)
- Handling crashes and restarts
- Deploying on Heroku or AWS

---

## 14. Bonus: Real-Time with Socket.io

- What is WebSockets?
- Setting up Socket.io with Node.js
- Simple chat app

---

## 15. Additional Topics (for reference or future modules)

- Working with file uploads (`multer`)
- Caching (Redis)
- Rate limiting and security
- Using TypeScript with Node.js

---

## Example Structure for Each Module

You can create a markdown file for each module. Here’s a template for each:

---

### Module X: Title

**Topics Covered:**

- topic 1
- topic 2

**Step-by-step Guide:**

1. Explanation
2. Code Example
3. Common Gotchas

**Practice:**

- [ ] Task 1
- [ ] Task 2

**Further Reading:**

- [Link1](#)
- [Link2](#)
