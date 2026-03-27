# RDS & Aurora

## Create RDS Instance

```bash
# Create MySQL RDS instance
aws rds create-db-instance \
  --db-instance-identifier mydb \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --master-username admin \
  --master-user-password MyPassword123! \
  --allocated-storage 20 \
  --storage-type gp3 \
  --vpc-security-group-ids sg-12345 \
  --db-subnet-group-name my-subnet-group \
  --backup-retention-period 7 \
  --preferred-backup-window "03:00-04:00" \
  --preferred-maintenance-window "mon:04:00-mon:05:00" \
  --multi-az \
  --publicly-accessible false \
  --storage-encrypted

# Create PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier mypgdb \
  --engine postgres \
  --engine-version 15.3 \
  --db-instance-class db.t3.small \
  --master-username postgres \
  --master-user-password MyPassword123! \
  --allocated-storage 100
```

## RDS with Node.js

```javascript
// MySQL with mysql2
import mysql from "mysql2/promise";

const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: 3306,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
  enableKeepAlive: true,
  keepAliveInitialDelay: 0,
});

// Execute query
const getUsers = async () => {
  const [rows] = await pool.execute("SELECT * FROM users WHERE active = ?", [
    true,
  ]);
  return rows;
};

// Transaction
const createUserWithProfile = async (userData, profileData) => {
  const connection = await pool.getConnection();

  try {
    await connection.beginTransaction();

    const [userResult] = await connection.execute(
      "INSERT INTO users (name, email) VALUES (?, ?)",
      [userData.name, userData.email]
    );

    const userId = userResult.insertId;

    await connection.execute(
      "INSERT INTO profiles (user_id, bio) VALUES (?, ?)",
      [userId, profileData.bio]
    );

    await connection.commit();
    return userId;
  } catch (error) {
    await connection.rollback();
    throw error;
  } finally {
    connection.release();
  }
};

// PostgreSQL with pg
import pg from "pg";

const pgPool = new pg.Pool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: 5432,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Query
const getUserById = async (id) => {
  const result = await pgPool.query("SELECT * FROM users WHERE id = $1", [id]);
  return result.rows[0];
};

// Parameterized query
const searchUsers = async (searchTerm) => {
  const query = {
    text: "SELECT * FROM users WHERE name ILIKE $1 OR email ILIKE $1",
    values: [`%${searchTerm}%`],
  };
  const result = await pgPool.query(query);
  return result.rows;
};
```

## Read Replicas

```bash
# Create read replica
aws rds create-db-instance-read-replica \
  --db-instance-identifier mydb-replica \
  --source-db-instance-identifier mydb \
  --db-instance-class db.t3.micro \
  --availability-zone us-east-1b

# Promote replica to standalone
aws rds promote-read-replica \
  --db-instance-identifier mydb-replica
```

```javascript
// Read/Write splitting
const writePool = mysql.createPool({
  host: process.env.DB_WRITE_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

const readPool = mysql.createPool({
  host: process.env.DB_READ_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

// Write operation
const createUser = async (userData) => {
  const [result] = await writePool.execute(
    "INSERT INTO users (name, email) VALUES (?, ?)",
    [userData.name, userData.email]
  );
  return result.insertId;
};

// Read operation
const getUsers = async () => {
  const [rows] = await readPool.execute("SELECT * FROM users");
  return rows;
};
```

## RDS Snapshots

```bash
# Create snapshot
aws rds create-db-snapshot \
  --db-snapshot-identifier mydb-snapshot-2024 \
  --db-instance-identifier mydb

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier mydb-restored \
  --db-snapshot-identifier mydb-snapshot-2024

# Copy snapshot to another region
aws rds copy-db-snapshot \
  --source-db-snapshot-identifier arn:aws:rds:us-east-1:123456789012:snapshot:mydb-snapshot \
  --target-db-snapshot-identifier mydb-snapshot-copy \
  --region us-west-2

# Share snapshot
aws rds modify-db-snapshot-attribute \
  --db-snapshot-identifier mydb-snapshot-2024 \
  --attribute-name restore \
  --values-to-add 123456789012
```

## RDS Proxy

```bash
# Create RDS Proxy
aws rds create-db-proxy \
  --db-proxy-name mydb-proxy \
  --engine-family MYSQL \
  --auth '[{
    "AuthScheme": "SECRETS",
    "SecretArn": "arn:aws:secretsmanager:us-east-1:123456789012:secret:db-secret",
    "IAMAuth": "DISABLED"
  }]' \
  --role-arn arn:aws:iam::123456789012:role/rds-proxy-role \
  --vpc-subnet-ids subnet-12345 subnet-67890

# Register target
aws rds register-db-proxy-targets \
  --db-proxy-name mydb-proxy \
  --db-instance-identifiers mydb
```

```javascript
// Connect via RDS Proxy
const proxyPool = mysql.createPool({
  host: "mydb-proxy.proxy-abc123.us-east-1.rds.amazonaws.com",
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: 3306,
  connectionLimit: 100, // Higher limit with proxy
});
```

## Aurora Cluster

```bash
# Create Aurora cluster
aws rds create-db-cluster \
  --db-cluster-identifier myaurora \
  --engine aurora-mysql \
  --engine-version 8.0.mysql_aurora.3.02.0 \
  --master-username admin \
  --master-user-password MyPassword123! \
  --database-name mydb \
  --vpc-security-group-ids sg-12345 \
  --db-subnet-group-name my-subnet-group \
  --backup-retention-period 7 \
  --storage-encrypted

# Add instances to cluster
aws rds create-db-instance \
  --db-instance-identifier myaurora-instance-1 \
  --db-instance-class db.r6g.large \
  --engine aurora-mysql \
  --db-cluster-identifier myaurora

aws rds create-db-instance \
  --db-instance-identifier myaurora-instance-2 \
  --db-instance-class db.r6g.large \
  --engine aurora-mysql \
  --db-cluster-identifier myaurora
```

## Aurora Serverless v2

```bash
# Create Aurora Serverless v2 cluster
aws rds create-db-cluster \
  --db-cluster-identifier myaurora-serverless \
  --engine aurora-mysql \
  --engine-mode provisioned \
  --serverless-v2-scaling-configuration MinCapacity=0.5,MaxCapacity=1.0 \
  --master-username admin \
  --master-user-password MyPassword123!

# Add serverless instance
aws rds create-db-instance \
  --db-instance-identifier myaurora-serverless-1 \
  --db-instance-class db.serverless \
  --engine aurora-mysql \
  --db-cluster-identifier myaurora-serverless
```

## Aurora Global Database

```bash
# Create global cluster
aws rds create-global-cluster \
  --global-cluster-identifier myglobal \
  --engine aurora-mysql \
  --engine-version 8.0.mysql_aurora.3.02.0

# Add primary cluster
aws rds create-db-cluster \
  --db-cluster-identifier myaurora-primary \
  --engine aurora-mysql \
  --global-cluster-identifier myglobal \
  --master-username admin \
  --master-user-password MyPassword123! \
  --region us-east-1

# Add secondary cluster
aws rds create-db-cluster \
  --db-cluster-identifier myaurora-secondary \
  --engine aurora-mysql \
  --global-cluster-identifier myglobal \
  --region eu-west-1
```

## Performance Insights

```bash
# Enable Performance Insights
aws rds modify-db-instance \
  --db-instance-identifier mydb \
  --enable-performance-insights \
  --performance-insights-retention-period 7

# Get metrics
aws pi get-resource-metrics \
  --service-type RDS \
  --identifier db-ABCDEFGHIJK \
  --metric-queries '[{
    "Metric": "db.load.avg",
    "GroupBy": {"Group": "db.wait_event"}
  }]' \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T23:59:59Z
```

## Connection Pooling Best Practices

```javascript
// Sequelize ORM with connection pool
import { Sequelize } from "sequelize";

const sequelize = new Sequelize({
  dialect: "mysql",
  host: process.env.DB_HOST,
  username: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  pool: {
    max: 10,
    min: 0,
    acquire: 30000,
    idle: 10000,
  },
  logging: false,
});

// Define model
const User = sequelize.define("User", {
  name: { type: DataTypes.STRING, allowNull: false },
  email: { type: DataTypes.STRING, unique: true },
});

// CRUD operations
const users = await User.findAll({ where: { active: true } });
const user = await User.findByPk(123);
await User.create({ name: "John", email: "john@example.com" });
await User.update({ name: "Jane" }, { where: { id: 123 } });
await User.destroy({ where: { id: 123 } });

// TypeORM configuration
import { DataSource } from "typeorm";

const AppDataSource = new DataSource({
  type: "postgres",
  host: process.env.DB_HOST,
  port: 5432,
  username: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  entities: ["src/entity/**/*.ts"],
  migrations: ["src/migration/**/*.ts"],
  synchronize: false,
  logging: ["error"],
  extra: {
    max: 20,
    connectionTimeoutMillis: 2000,
  },
});
```

## Automated Backups

```bash
# Modify backup settings
aws rds modify-db-instance \
  --db-instance-identifier mydb \
  --backup-retention-period 30 \
  --preferred-backup-window "03:00-04:00"

# Point-in-time restore
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier mydb \
  --target-db-instance-identifier mydb-restored \
  --restore-time 2024-01-15T10:30:00Z
```
