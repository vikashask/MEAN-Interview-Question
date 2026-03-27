# Cookies vs Web Storage

## Question

What are the key differences between cookies and Web Storage (localStorage and sessionStorage) in terms of storage capacity, lifespan, data transfer to server, and usability?

## Answer

### Storage Capacity

- **Cookies:** Limited to about 4KB of data.
- **Web Storage:** Both localStorage and sessionStorage provide at least 5MB of storage capacity per domain (varies by browser).

### Lifespan

- **Cookies:** Can be set to expire at a specific date/time using the `Expires` attribute or after a specific duration using the `Max-Age` attribute. If neither is set, cookies are deleted when the browser session ends (session cookies).
- **localStorage:** Persists indefinitely until explicitly deleted by code, browser settings, or clearing browser data.
- **sessionStorage:** Exists only for the duration of the page session. Data is cleared when the tab or browser is closed.

### Data Transfer to Server

- **Cookies:** Automatically sent to the server with every HTTP request to the domain, included in the request headers.
- **Web Storage:** Not automatically sent to the server. Data is only available client-side, but can be manually sent using JavaScript.

### Accessibility

- **Cookies:** Can be accessed by both server-side and client-side code.
- **Web Storage:** Accessible only via client-side JavaScript code.

### Security

- **Cookies:** Can be secured with flags like `HttpOnly` (preventing JavaScript access), `Secure` (only sent over HTTPS), and `SameSite` (prevents CSRF attacks).
- **Web Storage:** No built-in security mechanisms like `HttpOnly` flag. Always accessible by JavaScript on the same domain.

### Use Cases

- **Cookies:** Best for:
  - Authentication tokens
  - Server-side reading
  - Small amounts of data
  - Cross-browser compatibility
- **localStorage:** Best for:
  - Persistent application data
  - Caching data for offline use
  - Settings that should persist between sessions
- **sessionStorage:** Best for:
  - Temporary data specific to a single browser tab
  - Form data that should persist during navigation
  - Per-tab state management

### Code Examples

**Setting and reading cookies:**

```javascript
// Setting a cookie that expires in 7 days
document.cookie =
  "username=John; expires=" +
  new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toUTCString();

// Reading cookies
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

const username = getCookie("username");
```

**Using localStorage:**

```javascript
// Storing data
localStorage.setItem("user", JSON.stringify({ name: "John", role: "Admin" }));

// Retrieving data
const user = JSON.parse(localStorage.getItem("user"));

// Removing data
localStorage.removeItem("user");
```

**Using sessionStorage:**

```javascript
// Storing data
sessionStorage.setItem("activeTab", "profile");

// Retrieving data
const currentTab = sessionStorage.getItem("activeTab");

// Clearing all sessionStorage data
sessionStorage.clear();
```
