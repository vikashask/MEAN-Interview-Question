# RDS & Aurora

> **In plain English:** RDS is "a normal relational database (MySQL, PostgreSQL, etc), except AWS handles the patching, backups, and failover for you." Aurora is AWS's own faster, more resilient rebuild of MySQL/PostgreSQL, sold as a step up from standard RDS.

## Real-world analogy

- **RDS instance** = a fully-serviced apartment with a database inside — AWS handles maintenance (patching), but you still pick the layout (engine: MySQL/Postgres/etc).
- **Multi-AZ** = an identical backup apartment in a different building, always in sync, ready to take over instantly if the main one has a power outage.
- **Read Replica** = a second apartment that only ever *reads* the mail forwarded from the main one (asynchronous copy) — used to spread out read traffic, not for instant failover.
- **Aurora** = a newer, better-engineered apartment complex built by AWS itself specifically for speed and resilience — up to 15 read replicas, storage that auto-heals and auto-grows.
- **RDS Proxy** = a receptionist standing between your app and the database, pooling and reusing connections so the database doesn't get overwhelmed by too many direct connections (this is a huge deal for Lambda, which can spawn many concurrent connections).
- **Snapshot** = a full photograph of the apartment at a point in time, which you can use to instantly recreate an identical apartment elsewhere.

## Core concepts (memorize these first)

| Term | What it means |
|---|---|
| **Multi-AZ** | A synchronous standby copy in a different Availability Zone — automatic failover for *availability*, not for scaling reads. |
| **Read Replica** | An asynchronous copy used to offload read traffic — can be promoted to standalone if needed, but not built for instant failover. |
| **Automated Backups** | Daily snapshot + continuous transaction logs, enabling point-in-time restore to any second within the retention window. |
| **Manual Snapshot** | A snapshot you trigger yourself, kept until you delete it (automated backups expire after the retention period). |
| **Parameter Group** | Database engine configuration settings (like `my.cnf` for MySQL), applied at the RDS level. |
| **RDS Proxy** | A managed connection pooler sitting between app and database — critical for Lambda, which can otherwise exhaust DB connections. |
| **Aurora** | AWS's MySQL/PostgreSQL-compatible engine — faster, self-healing storage, up to 15 read replicas (vs 5 for standard RDS), and storage auto-scales up to 128TB. |
| **Aurora Serverless v2** | Aurora that scales capacity up/down automatically based on load — pay only for what you use. |
| **Aurora Global Database** | One primary region + up to 5 secondary read-only regions with typically <1 second replication lag — for global apps / disaster recovery. |
| **Performance Insights** | A built-in dashboard showing exactly what's slowing your database down (which queries, which wait events). |

**The #1 interview trap:** Multi-AZ is for **availability** (automatic failover if the primary dies), Read Replicas are for **scalability** (spreading out read traffic). People often confuse them — Multi-AZ standby is *not* used for serving read traffic by default (in a plain RDS Multi-AZ setup), it just sits ready to take over.

## Memory hooks

- **"Multi-AZ = insurance policy. Read Replica = extra hands for reading."**
- Aurora vs RDS-MySQL: Aurora = "MySQL, but AWS rebuilt the storage engine to be faster/self-healing and let you have way more replicas."
- **RDS Proxy exists mainly because Lambda + traditional DB connections = too many open connections, too fast.**

---

## Create RDS Instance

Multi-AZ + storage encryption + a backup window are the production-standard flags to remember.

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

Standard connection pooling for MySQL and PostgreSQL, plus a transaction example — note the `beginTransaction`/`commit`/`rollback` pattern for operations that must succeed or fail together.

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

Asynchronous copies for scaling reads — your app must be written to send writes to the primary and reads to the replica(s) ("read/write splitting").

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

Manual snapshots persist until you delete them (unlike automated backups, which expire per the retention period). You can also copy them across regions or share them with another AWS account.

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

Pools and reuses database connections on your behalf. Especially important for Lambda-based apps, where each concurrent invocation could otherwise open its own DB connection and exhaust the database's connection limit.

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

Aurora separates compute (instances) from a shared, self-healing storage layer — one primary writer instance, and up to 15 reader instances, all sharing the same underlying storage (so replicas don't need to re-copy data, unlike standard RDS read replicas).

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

Capacity (measured in ACUs) scales up/down automatically based on load, instead of you picking a fixed instance size — good for unpredictable or intermittent workloads.

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

One primary region handles writes; up to 5 secondary regions get near-real-time read-only copies (typically under 1 second lag) — used for global read latency and disaster recovery across regions.

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

A dashboard that shows exactly what's making the database slow right now — which SQL queries, which wait events — without needing to manually enable slow-query logging.

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

Whether you use an ORM like Sequelize/TypeORM or raw drivers, always configure a bounded connection pool — unbounded connections are the #1 cause of database outages under load.

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

Automated backups + transaction logs let you restore to almost any second within your retention window — not just to the moment of the last daily snapshot.

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

---

## Quick interview answers

**Q: Multi-AZ vs Read Replica — what's the real difference?**
Multi-AZ = a synchronous standby for automatic failover (availability). Read Replica = an asynchronous copy for spreading out read traffic (scalability). A standard Multi-AZ standby isn't normally used to serve reads; a read replica isn't automatically failed over to.

**Q: Why is Aurora often described as faster/more resilient than plain RDS-MySQL?**
Aurora's storage layer is distributed across multiple AZs automatically and self-heals from disk failures, it supports up to 15 low-lag read replicas (vs 5 on RDS), and storage auto-grows up to 128TB without manual resizing.

**Q: Why use RDS Proxy, specifically with Lambda?**
Lambda can spin up many concurrent executions instantly, each potentially opening its own DB connection — this can exhaust the database's max connections. RDS Proxy pools and reuses connections so the database sees far fewer, sustained connections.

**Q: What's the difference between a manual snapshot and an automated backup?**
Automated backups are on a schedule and auto-expire per your retention setting; they also enable point-in-time restore. Manual snapshots are taken on demand and persist until you explicitly delete them.

**Q: How do you achieve near-zero data loss in a region-wide outage?**
Aurora Global Database — one primary region with secondary read-only regions typically under 1 second behind, promotable to primary during a regional failure.
