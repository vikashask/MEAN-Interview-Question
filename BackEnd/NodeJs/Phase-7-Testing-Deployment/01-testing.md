# Testing

## Jest Setup

```bash
npm install -D jest @types/jest
npx jest --init
```

```javascript
// jest.config.js
module.exports = {
  testEnvironment: "node",
  coveragePathIgnorePatterns: ["/node_modules/"],
  testMatch: ["**/__tests__/**/*.js", "**/?(*.)+(spec|test).js"],
};
```

## Unit Testing

```javascript
// math.js
const sum = (a, b) => a + b;
const multiply = (a, b) => a * b;
module.exports = { sum, multiply };

// math.test.js
const { sum, multiply } = require("./math");

describe("Math functions", () => {
  test("sum adds two numbers", () => {
    expect(sum(2, 3)).toBe(5);
  });

  test("multiply multiplies two numbers", () => {
    expect(multiply(2, 3)).toBe(6);
  });

  test("sum handles negative numbers", () => {
    expect(sum(-2, 3)).toBe(1);
  });
});
```

## Async Testing

```javascript
// async.test.js
const fetchData = async () => {
  const res = await fetch("https://api.example.com/data");
  return res.json();
};

describe("Async operations", () => {
  test("fetches data", async () => {
    const data = await fetchData();
    expect(data).toBeDefined();
  });

  test("handles errors", async () => {
    await expect(fetchData()).rejects.toThrow();
  });
});
```

## Mocking

```javascript
// user.js
const User = require("./User");

const getUser = async (id) => {
  return await User.findById(id);
};

// user.test.js
jest.mock("./User");
const User = require("./User");
const { getUser } = require("./user");

describe("User service", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("gets user by id", async () => {
    User.findById.mockResolvedValue({ id: 1, name: "John" });
    const user = await getUser(1);
    expect(user.name).toBe("John");
    expect(User.findById).toHaveBeenCalledWith(1);
  });

  test("handles errors", async () => {
    User.findById.mockRejectedValue(new Error("DB error"));
    await expect(getUser(1)).rejects.toThrow("DB error");
  });
});
```

## API Testing

```javascript
const request = require("supertest");
const app = require("./app");

describe("API endpoints", () => {
  test("GET /users returns list", async () => {
    const res = await request(app)
      .get("/users")
      .expect(200)
      .expect("Content-Type", /json/);

    expect(Array.isArray(res.body)).toBe(true);
  });

  test("POST /users creates user", async () => {
    const res = await request(app)
      .post("/users")
      .send({ name: "John", email: "john@example.com" })
      .expect(201);

    expect(res.body).toHaveProperty("id");
  });

  test("GET /users/:id returns user", async () => {
    const res = await request(app).get("/users/1").expect(200);

    expect(res.body.id).toBe(1);
  });

  test("DELETE /users/:id deletes user", async () => {
    await request(app).delete("/users/1").expect(204);
  });
});
```

## Test Coverage

```bash
# Run tests with coverage
jest --coverage

# Coverage thresholds
```

```javascript
// jest.config.js
module.exports = {
  collectCoverageFrom: ["src/**/*.js"],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

## Fixtures & Factories

```javascript
// fixtures/user.js
const userFixture = {
  id: 1,
  name: "John Doe",
  email: "john@example.com",
  role: "user",
};

module.exports = { userFixture };

// factories/userFactory.js
const createUser = (overrides = {}) => ({
  id: Math.random(),
  name: "John",
  email: "john@example.com",
  ...overrides,
});

module.exports = { createUser };

// user.test.js
const { createUser } = require("./factories/userFactory");

test("creates user with custom name", () => {
  const user = createUser({ name: "Jane" });
  expect(user.name).toBe("Jane");
});
```

## Integration Testing

```javascript
// integration.test.js
const request = require("supertest");
const app = require("./app");
const User = require("./models/User");

describe("User flow", () => {
  beforeAll(async () => {
    await User.deleteMany({});
  });

  test("complete user lifecycle", async () => {
    // Create
    const createRes = await request(app)
      .post("/users")
      .send({ name: "John", email: "john@example.com" })
      .expect(201);

    const userId = createRes.body.id;

    // Read
    const getRes = await request(app).get(`/users/${userId}`).expect(200);

    expect(getRes.body.name).toBe("John");

    // Update
    await request(app)
      .put(`/users/${userId}`)
      .send({ name: "Jane" })
      .expect(200);

    // Delete
    await request(app).delete(`/users/${userId}`).expect(204);
  });
});
```

## Test Helpers

```javascript
// helpers/testHelpers.js
const createAuthToken = (userId) => {
  const jwt = require("jsonwebtoken");
  return jwt.sign({ userId }, process.env.JWT_SECRET);
};

const authenticatedRequest = (app, method, path) => {
  const request = require("supertest");
  const token = createAuthToken(1);
  return request(app)[method](path).set("Authorization", `Bearer ${token}`);
};

module.exports = { createAuthToken, authenticatedRequest };

// auth.test.js
const { authenticatedRequest } = require("./helpers/testHelpers");

test("protected route requires auth", async () => {
  const res = await authenticatedRequest(app, "get", "/profile").expect(200);

  expect(res.body).toHaveProperty("user");
});
```
