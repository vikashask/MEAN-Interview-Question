# Real-time Communication: WebSockets

## Socket.io Basics

```javascript
const express = require("express");
const http = require("http");
const socketIO = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = socketIO(server, {
  cors: { origin: "*" },
});

// Connection
io.on("connection", (socket) => {
  console.log("User connected:", socket.id);

  // Listen for events
  socket.on("message", (data) => {
    console.log("Message:", data);
    // Broadcast to all clients
    io.emit("message", data);
  });

  // Disconnect
  socket.on("disconnect", () => {
    console.log("User disconnected:", socket.id);
  });
});

server.listen(3000);
```

## Rooms & Namespaces

```javascript
// Rooms
io.on("connection", (socket) => {
  // Join room
  socket.on("join-room", (roomId) => {
    socket.join(roomId);
    socket.to(roomId).emit("user-joined", socket.id);
  });

  // Send to room
  socket.on("room-message", (roomId, message) => {
    io.to(roomId).emit("message", message);
  });

  // Leave room
  socket.on("leave-room", (roomId) => {
    socket.leave(roomId);
    socket.to(roomId).emit("user-left", socket.id);
  });
});

// Namespaces
const chatNamespace = io.of("/chat");

chatNamespace.on("connection", (socket) => {
  socket.on("message", (data) => {
    chatNamespace.emit("message", data);
  });
});

// Client
const socket = io("http://localhost:3000/chat");
socket.emit("message", "Hello");
socket.on("message", (data) => console.log(data));
```

## Real-time Chat

```javascript
// Server
io.on("connection", (socket) => {
  // User joins
  socket.on("join", (username) => {
    socket.username = username;
    socket.broadcast.emit("user-joined", `${username} joined`);
  });

  // Send message
  socket.on("send-message", (message) => {
    io.emit("message", {
      username: socket.username,
      message,
      timestamp: new Date(),
    });
  });

  // Typing indicator
  socket.on("typing", () => {
    socket.broadcast.emit("user-typing", socket.username);
  });

  socket.on("stop-typing", () => {
    socket.broadcast.emit("user-stop-typing", socket.username);
  });

  // Disconnect
  socket.on("disconnect", () => {
    io.emit("user-left", `${socket.username} left`);
  });
});

// Client
const socket = io();

socket.emit("join", "John");

document.getElementById("send-btn").addEventListener("click", () => {
  const message = document.getElementById("input").value;
  socket.emit("send-message", message);
});

socket.on("message", (data) => {
  console.log(`${data.username}: ${data.message}`);
});

document.getElementById("input").addEventListener("input", () => {
  socket.emit("typing");
});

document.getElementById("input").addEventListener("blur", () => {
  socket.emit("stop-typing");
});
```

## Presence & Status

```javascript
// Track online users
const users = new Map();

io.on("connection", (socket) => {
  socket.on("user-online", (userData) => {
    users.set(socket.id, { ...userData, socketId: socket.id });
    io.emit("users-list", Array.from(users.values()));
  });

  socket.on("user-status", (status) => {
    const user = users.get(socket.id);
    if (user) {
      user.status = status;
      io.emit("user-status-changed", { socketId: socket.id, status });
    }
  });

  socket.on("disconnect", () => {
    users.delete(socket.id);
    io.emit("users-list", Array.from(users.values()));
  });
});
```

## Server-Sent Events (SSE)

```javascript
// Server
app.get("/events", (req, res) => {
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");

  // Send initial connection message
  res.write("data: Connected\n\n");

  // Send updates
  const interval = setInterval(() => {
    res.write(`data: ${JSON.stringify({ time: new Date() })}\n\n`);
  }, 1000);

  // Cleanup on disconnect
  req.on("close", () => {
    clearInterval(interval);
    res.end();
  });
});

// Client
const eventSource = new EventSource("/events");

eventSource.onmessage = (event) => {
  console.log("Event:", event.data);
};

eventSource.onerror = () => {
  console.error("Connection lost");
  eventSource.close();
};
```

## Broadcasting with Redis

```javascript
const redis = require("redis");
const socketIO = require("socket.io");
const { createAdapter } = require("@socket.io/redis-adapter");

const io = socketIO(server);
const pubClient = redis.createClient();
const subClient = pubClient.duplicate();

await Promise.all([pubClient.connect(), subClient.connect()]);

io.adapter(createAdapter(pubClient, subClient));

// Now broadcasts work across multiple server instances
io.on("connection", (socket) => {
  socket.on("message", (data) => {
    io.emit("message", data); // Broadcasts to all connected clients across all servers
  });
});
```
