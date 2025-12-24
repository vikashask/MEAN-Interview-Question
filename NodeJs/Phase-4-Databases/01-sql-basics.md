# SQL Databases

## SQL Basics

```javascript
// SQL queries
const query = `
  SELECT id, name, email FROM users WHERE age > 18
`;

const insertQuery = `
  INSERT INTO users (name, email, age) VALUES (?, ?, ?)
`;

const updateQuery = `
  UPDATE users SET email = ? WHERE id = ?
`;

const deleteQuery = `
  DELETE FROM users WHERE id = ?
`;
```

## Relationships

```sql
-- One-to-Many
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100)
);

CREATE TABLE posts (
  id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(200),
  user_id INT,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Many-to-Many
CREATE TABLE users_roles (
  user_id INT,
  role_id INT,
  PRIMARY KEY (user_id, role_id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Joins
SELECT u.name, p.title
FROM users u
INNER JOIN posts p ON u.id = p.user_id;

SELECT u.name, r.name
FROM users u
INNER JOIN users_roles ur ON u.id = ur.user_id
INNER JOIN roles r ON ur.role_id = r.id;
```

## Transactions

```javascript
// Transaction example
const connection = await pool.getConnection();

try {
  await connection.beginTransaction();

  await connection.query("INSERT INTO users (name) VALUES (?)", ["John"]);
  await connection.query("INSERT INTO logs (action) VALUES (?)", [
    "User created",
  ]);

  await connection.commit();
} catch (err) {
  await connection.rollback();
  throw err;
} finally {
  connection.release();
}
```

## Connection Pooling

```javascript
const mysql = require("mysql2/promise");

const pool = mysql.createPool({
  host: "localhost",
  user: "root",
  password: "password",
  database: "mydb",
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

// Get connection from pool
const connection = await pool.getConnection();
const [rows] = await connection.query("SELECT * FROM users");
connection.release();

// Or use pool directly
const [rows] = await pool.query("SELECT * FROM users");
```

## ACID Properties

```javascript
// Atomicity - all or nothing
// Consistency - valid state
// Isolation - concurrent transactions don't interfere
// Durability - committed data persists

// Isolation levels
// READ UNCOMMITTED - dirty reads possible
// READ COMMITTED - only committed data read
// REPEATABLE READ - consistent reads
// SERIALIZABLE - full isolation

const connection = await pool.getConnection();
await connection.query("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ");
```

## Query Optimization

```sql
-- Add indexes for faster queries
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_user_id ON posts(user_id);

-- Use EXPLAIN to analyze queries
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- Avoid SELECT *
SELECT id, name, email FROM users;

-- Use LIMIT
SELECT * FROM users LIMIT 10;

-- Use proper WHERE clauses
SELECT * FROM users WHERE age > 18 AND status = 'active';
```
