# Caching

## In-Memory Caching

```javascript
// Simple in-memory cache
const cache = new Map();

const getOrSet = async (key, fn) => {
  if (cache.has(key)) {
    return cache.get(key);
  }
  const value = await fn();
  cache.set(key, value);
  return value;
};

// Usage
const user = await getOrSet(`user:${id}`, () => User.findById(id));

// Cache with expiration
class CacheWithTTL {
  constructor() {
    this.cache = new Map();
  }

  set(key, value, ttl = 60000) {
    this.cache.set(key, { value, expires: Date.now() + ttl });
  }

  get(key) {
    const item = this.cache.get(key);
    if (!item) return null;
    if (Date.now() > item.expires) {
      this.cache.delete(key);
      return null;
    }
    return item.value;
  }

  clear() {
    this.cache.clear();
  }
}

const cache = new CacheWithTTL();
cache.set("key", "value", 5000); // 5 second TTL
```

## Redis Caching

```javascript
const redis = require("redis");

const client = redis.createClient({
  host: "localhost",
  port: 6379,
});

await client.connect();

// Set value
await client.set("key", "value");
await client.setEx("key", 3600, "value"); // With expiration

// Get value
const value = await client.get("key");

// Delete
await client.del("key");

// Increment
await client.incr("counter");

// List operations
await client.lPush("list", "item1", "item2");
const items = await client.lRange("list", 0, -1);

// Hash operations
await client.hSet("user:1", { name: "John", email: "john@example.com" });
const user = await client.hGetAll("user:1");
```

## Cache Invalidation

```javascript
// Cache-aside pattern
const getUser = async (id) => {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);

  const user = await User.findById(id);
  await redis.setEx(`user:${id}`, 3600, JSON.stringify(user));
  return user;
};

// Invalidate on update
app.put("/users/:id", async (req, res) => {
  const user = await User.findByIdAndUpdate(req.params.id, req.body);
  await redis.del(`user:${req.params.id}`); // Invalidate cache
  res.json(user);
});

// Write-through pattern
const updateUser = async (id, data) => {
  const user = await User.findByIdAndUpdate(id, data);
  await redis.setEx(`user:${id}`, 3600, JSON.stringify(user));
  return user;
};

// Write-back pattern (async write to DB)
const updateUserAsync = async (id, data) => {
  await redis.setEx(`user:${id}`, 3600, JSON.stringify(data));
  // Write to DB asynchronously
  User.findByIdAndUpdate(id, data).catch((err) => console.error(err));
};
```

## Cache Warming

```javascript
// Pre-load cache on startup
const warmCache = async () => {
  const users = await User.find();
  for (const user of users) {
    await redis.setEx(`user:${user.id}`, 3600, JSON.stringify(user));
  }
  console.log("Cache warmed");
};

app.listen(3000, async () => {
  await warmCache();
  console.log("Server started");
});

// Periodic cache refresh
setInterval(async () => {
  await warmCache();
}, 60 * 60 * 1000); // Every hour
```

## Cache Stampede Prevention

```javascript
// Probabilistic early expiration
const getWithEarlyExpiration = async (key, fn, ttl = 3600) => {
  const cached = await redis.get(key);
  if (cached) {
    const ttlRemaining = await redis.ttl(key);
    // Refresh if less than 10% of TTL remains
    if (ttlRemaining < ttl * 0.1) {
      // Refresh in background
      fn()
        .then((value) => {
          redis.setEx(key, ttl, JSON.stringify(value));
        })
        .catch((err) => console.error(err));
    }
    return JSON.parse(cached);
  }

  const value = await fn();
  await redis.setEx(key, ttl, JSON.stringify(value));
  return value;
};

// Lock-based approach
const getWithLock = async (key, fn, ttl = 3600) => {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);

  const lockKey = `lock:${key}`;
  const lockValue = Date.now();

  // Try to acquire lock
  const acquired = await redis.set(lockKey, lockValue, {
    NX: true,
    EX: 10,
  });

  if (acquired) {
    try {
      const value = await fn();
      await redis.setEx(key, ttl, JSON.stringify(value));
      return value;
    } finally {
      await redis.del(lockKey);
    }
  } else {
    // Wait for lock to be released
    let attempts = 0;
    while (attempts < 10) {
      await new Promise((resolve) => setTimeout(resolve, 100));
      const cached = await redis.get(key);
      if (cached) return JSON.parse(cached);
      attempts++;
    }
    // Fallback to computing value
    return fn();
  }
};
```

## Cache Metrics

```javascript
// Track cache hits/misses
class CacheMetrics {
  constructor() {
    this.hits = 0;
    this.misses = 0;
  }

  recordHit() {
    this.hits++;
  }

  recordMiss() {
    this.misses++;
  }

  getHitRate() {
    const total = this.hits + this.misses;
    return total === 0 ? 0 : (this.hits / total) * 100;
  }

  getStats() {
    return {
      hits: this.hits,
      misses: this.misses,
      hitRate: this.getHitRate(),
    };
  }
}

const metrics = new CacheMetrics();

const getUser = async (id) => {
  const cached = await redis.get(`user:${id}`);
  if (cached) {
    metrics.recordHit();
    return JSON.parse(cached);
  }

  metrics.recordMiss();
  const user = await User.findById(id);
  await redis.setEx(`user:${id}`, 3600, JSON.stringify(user));
  return user;
};

app.get("/cache/stats", (req, res) => {
  res.json(metrics.getStats());
});
```
