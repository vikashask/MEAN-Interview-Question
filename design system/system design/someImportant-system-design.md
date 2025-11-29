# System Design Interview Preparation Guide

---

## 1. What is System Design Process in Software Engineering?

**System Design** is the process of defining the architecture, components, modules, interfaces, and data flow of a system to satisfy specified requirements.

### System Design Process Steps:

**Step 1: Requirements Clarification**

- **Functional Requirements**: What the system should do (user registration, login, posting content)
- **Non-Functional Requirements**: How the system should perform (scalability, availability, latency, consistency)

**Step 2: Back-of-the-Envelope Estimation**

```
- Daily Active Users (DAU): 10 million
- Requests per second: 10M / (24 * 3600) ≈ 115 RPS
- Storage: 10M users × 1KB = 10GB/day
- Bandwidth: 115 × 1KB = 115 KB/s
```

**Step 3: System Interface Definition**

```
createUser(name, email, password) → user_id
getUser(user_id) → user_object
updateUser(user_id, user_data) → success/failure
```

**Step 4: Data Model Definition**

```sql
Users: user_id, name, email, created_at
Posts: post_id, user_id, content, timestamp
```

**Step 5: High-Level Design**

```
Clients → Load Balancer → App Servers → Cache/Database/CDN
```

**Step 6: Detailed Component Design** - Deep dive into each component

**Step 7: Identifying Bottlenecks** - Single points of failure, data bottlenecks

---

## 2. Monolithic Architecture

**Monolithic Architecture** is a traditional model where the entire application is built as a single, unified unit.

### Characteristics:

- **Single Codebase**: All functionality in one repository
- **Single Deployment**: Entire app deployed together
- **Shared Database**: All modules share one database
- **Tightly Coupled**: Components are interdependent

### Advantages:

- Simple development initially
- Simple testing (end-to-end in one place)
- Simple deployment (single artifact)
- Low latency (no network calls between modules)

### Disadvantages:

- Difficult to scale (must scale entire app)
- Technology lock-in
- Slow development as codebase grows
- Risk of failure (one bug can bring down entire system)

### When to Use:

- Small teams (< 5 developers)
- Simple applications / MVP / prototypes

---

## 3. Difference Between Monolithic and Microservices Architecture

| Aspect             | Monolithic               | Microservices                             |
| ------------------ | ------------------------ | ----------------------------------------- |
| **Architecture**   | Single unified unit      | Collection of small, independent services |
| **Codebase**       | Single repository        | Multiple repositories                     |
| **Deployment**     | All-or-nothing           | Independent deployment per service        |
| **Scaling**        | Scale entire application | Scale individual services                 |
| **Technology**     | Single tech stack        | Different tech per service                |
| **Database**       | Single shared database   | Database per service                      |
| **Failure Impact** | Entire app fails         | Only affected service fails               |
| **Complexity**     | Simple initially         | Higher operational complexity             |

### When to Choose Microservices:

- Large, complex applications
- Multiple development teams
- Need for independent scaling
- High availability requirements

---

## 4. What is Latency in Networking | How to Reduce Latency | CDN vs Caching

### What is Latency?

**Latency** is the time delay between a user's action and the system's response (measured in ms).

### Common Latency Numbers:

```
L1 Cache Reference:           0.5 ns
Main Memory Reference:        100 ns
SSD Random Read:              16,000 ns (16 μs)
Round trip within DC:         500,000 ns (0.5 ms)
Round trip CA to EU:          150,000,000 ns (150 ms)
```

### How to Reduce Latency:

1. **Use CDN** - Edge servers reduce geographic latency
2. **Implement Caching** - Avoid repeated database queries
3. **Database Optimization** - Indexing, query optimization
4. **Load Balancing** - Distribute requests
5. **Compression** - GZIP reduces data transfer

### CDN vs Caching:

| Aspect           | CDN                       | Caching                    |
| ---------------- | ------------------------- | -------------------------- |
| **Location**     | Edge servers globally     | In-memory on app servers   |
| **Purpose**      | Reduce geographic latency | Reduce DB/computation load |
| **Content Type** | Static (images, CSS, JS)  | Dynamic data, queries      |
| **Examples**     | CloudFlare, CloudFront    | Redis, Memcached           |

---

## 5. What is Throughput? (How to Improve Throughput?)

### What is Throughput?

**Throughput** is the amount of data or operations processed per unit of time.

**Measured As:** RPS, TPS, QPS, bps

### Throughput vs Latency:

```
Latency: How FAST a single request is processed
Throughput: How MANY requests are processed
Highway analogy: Latency = Speed of car, Throughput = Cars per hour
```

### How to Improve Throughput:

1. **Horizontal Scaling** - Add more machines
2. **Caching** - Reduce DB load
3. **Database Optimization** - Connection pooling, read replicas
4. **Asynchronous Processing** - Queue + background workers
5. **Batch Processing** - Combine operations
6. **Code Optimization** - Efficient algorithms

---

## 6. What is Availability? (Replication vs Redundancy)

### What is Availability?

**Availability** = Uptime / (Uptime + Downtime) × 100%

### The Nines of Availability:

| Availability      | Downtime/Year |
| ----------------- | ------------- |
| 99% (Two 9s)      | 3.65 days     |
| 99.9% (Three 9s)  | 8.77 hours    |
| 99.99% (Four 9s)  | 52.60 min     |
| 99.999% (Five 9s) | 5.26 min      |

### How to Achieve High Availability:

1. Eliminate Single Points of Failure
2. Use redundant components
3. Implement replication

### Replication vs Redundancy:

| Aspect         | Redundancy                   | Replication                    |
| -------------- | ---------------------------- | ------------------------------ |
| **Definition** | Backup components/systems    | Copying data across nodes      |
| **Purpose**    | Failover protection          | Data availability & durability |
| **Example**    | Backup power, standby server | Database replicas              |

---

## 7. What is Consistency in System Design (Strong vs Eventual Consistency)

### Strong Consistency

Every read receives the most recent write or an error.

- Synchronous replication
- Higher latency, lower availability
- **Use Cases:** Banking, inventory, booking systems

### Eventual Consistency

Given enough time, all reads will return the last updated value.

- Asynchronous replication
- Lower latency, higher availability
- **Use Cases:** Social media, DNS, shopping carts

| Aspect             | Strong Consistency  | Eventual Consistency    |
| ------------------ | ------------------- | ----------------------- |
| **Read Guarantee** | Latest value always | Latest value eventually |
| **Latency**        | Higher              | Lower                   |
| **Availability**   | Lower               | Higher                  |

---

## 8. What is CAP Theorem?

In a distributed system, you can only guarantee **two out of three**:

- **C**onsistency: All nodes see same data
- **A**vailability: Every request gets a response
- **P**artition Tolerance: System works despite network failures

### CAP Combinations:

- **CP (Consistency + Partition)**: MongoDB, HBase, Redis
- **AP (Availability + Partition)**: Cassandra, CouchDB, DynamoDB
- **CA**: Only possible in single node (traditional RDBMS)

### Real-World Choices:

| System       | Choice | Reasoning                         |
| ------------ | ------ | --------------------------------- |
| Banking      | CP     | Financial accuracy critical       |
| Social Media | AP     | High availability, stale posts OK |

---

## 9. What is Lamport Logical Clock?

A **logical clock** algorithm providing partial ordering of events in distributed systems without relying on physical time.

### Algorithm Rules:

1. Each process maintains a counter (clock)
2. Before any event: `clock = clock + 1`
3. When sending message: include clock value
4. When receiving: `clock = max(local_clock, received_clock) + 1`

### Use Cases:

- Distributed databases (conflict detection)
- Version control systems
- Event ordering in message queues

---

## 10. Difference Between Horizontal and Vertical Scaling

### Vertical Scaling (Scale Up)

Adding more power to existing machine (CPU, RAM, Storage).

### Horizontal Scaling (Scale Out)

Adding more machines to the system.

| Aspect         | Vertical         | Horizontal              |
| -------------- | ---------------- | ----------------------- |
| **Method**     | Upgrade hardware | Add machines            |
| **Cost**       | Expensive        | Cost-effective          |
| **Limit**      | Hardware limits  | Theoretically unlimited |
| **Downtime**   | Required         | Zero downtime           |
| **Complexity** | Simple           | Complex                 |
| **Failure**    | Single point     | Fault tolerant          |

---

## 11. Difference Between Redundancy and Replication (Master-Slave Replication)

### Master-Slave Replication:

```
Master (Read + Write) → Slaves (Read Only)
```

### Replication Types:

- **Synchronous**: Wait for all replicas before acknowledging (strong consistency)
- **Asynchronous**: Acknowledge immediately, replicate later (eventual consistency)

### Master-Master Replication:

Both masters accept writes; requires conflict resolution.

---

## 12. What is Load Balancer and How It Works (Load Balancing Algorithms)

### Load Balancing Algorithms:

1. **Round Robin**: Sequential distribution
2. **Weighted Round Robin**: Higher weight = more requests
3. **Least Connections**: Route to server with fewest connections
4. **IP Hash**: Same client → same server
5. **Least Response Time**: Fastest server selected
6. **Random**: Random selection

### Types:

- **Layer 4**: TCP/UDP level (faster)
- **Layer 7**: HTTP level (content-based routing)

### Popular Load Balancers:

Nginx, HAProxy, AWS ELB/ALB/NLB

---

## 13. What is Caching (Complete Explanation)

### Caching Strategies:

**1. Cache-Aside (Lazy Loading)**

- Read: Check cache → if miss, read DB → store in cache
- Write: Write to DB → invalidate cache

**2. Write-Through**

- Write to cache → cache writes to DB synchronously

**3. Write-Behind (Write-Back)**

- Write to cache → return immediately → async DB write

### Cache Invalidation:

- **TTL**: Data expires after set time
- **Event-based**: Invalidate on data change

### Popular Solutions:

Redis, Memcached, Varnish

---

## 14. Cache Eviction Techniques (LRU, LFU, MRU, LIFO, FIFO & RR)

| Policy   | Description                 | Best For               |
| -------- | --------------------------- | ---------------------- |
| **LRU**  | Evict least recently used   | General purpose        |
| **LFU**  | Evict least frequently used | Frequency matters      |
| **MRU**  | Evict most recently used    | Scanning workloads     |
| **FIFO** | Evict oldest                | Simple needs           |
| **LIFO** | Evict newest                | Stack patterns         |
| **RR**   | Random eviction             | Unpredictable patterns |

---

## 15. File Based Storage System

### Types:

- **Local File System**: ext4, NTFS
- **Network File System**: NFS, SMB
- **Distributed File System**: HDFS, GlusterFS
- **Object Storage**: AWS S3, Azure Blob

### Use Cases:

Large binary files, logs, backups, static assets

---

## 16. Can RDBMS Scale Horizontally? (Why Is It Hard?)

### Challenges:

1. **ACID Compliance** across nodes (requires 2-Phase Commit)
2. **JOINs Across Shards** (expensive network calls)
3. **Foreign Key Constraints** across shards
4. **Auto-Increment IDs** don't work distributed

### Solutions:

- Read Replicas
- Sharding (horizontal partitioning)
- Vitess, CockroachDB, TiDB, Citus

---

## 17. Types of NoSQL Databases

| Type              | Examples           | Use Case                         |
| ----------------- | ------------------ | -------------------------------- |
| **Key-Value**     | Redis, DynamoDB    | Caching, Sessions                |
| **Document**      | MongoDB, Firestore | CMS, User profiles               |
| **Column-Family** | Cassandra, HBase   | Time-series, Logs                |
| **Graph**         | Neo4j, Neptune     | Social networks, Recommendations |

---

## 18. What is Polyglot Persistence?

Using different database technologies for different data storage needs.

**Example (E-commerce):**

- Sessions → Redis
- Products → MongoDB
- Orders → PostgreSQL
- Search → Elasticsearch
- Recommendations → Neo4j

---

## 19. What is Denormalization in RDBMS?

**Denormalization** adds redundant data to improve read performance by reducing JOINs.

| Aspect          | Normalized | Denormalized |
| --------------- | ---------- | ------------ |
| **Storage**     | Less       | More         |
| **Read Speed**  | Slower     | Faster       |
| **Write Speed** | Faster     | Slower       |
| **Consistency** | Easier     | Harder       |

---

## 20. How Does Indexing Work in Databases?

### What is an Index?

A data structure (typically B-Tree) that speeds up data retrieval.

```sql
-- Without index: Full table scan O(n)
-- With index: B-Tree lookup O(log n)
CREATE INDEX idx_user_email ON users(email);
```

### Index Types:

- **B-Tree**: Default, good for range queries
- **Hash**: Fast equality lookups
- **Composite**: Multiple columns
- **Full-text**: Text search

### SQL Query Optimization:

1. Use `EXPLAIN ANALYZE` to understand query plans
2. Add indexes on WHERE, JOIN, ORDER BY columns
3. Avoid `SELECT *`
4. Use pagination (LIMIT/OFFSET)
5. Avoid functions on indexed columns

---

## 21-22. Synchronous vs Asynchronous Communication

### Synchronous:

- Caller waits for response
- Blocking
- Example: HTTP request/response

### Asynchronous:

- Caller doesn't wait
- Non-blocking
- Example: Message queues, WebSockets

| Aspect         | Synchronous | Asynchronous    |
| -------------- | ----------- | --------------- |
| **Blocking**   | Yes         | No              |
| **Coupling**   | Tight       | Loose           |
| **Latency**    | Higher      | Lower perceived |
| **Complexity** | Simpler     | More complex    |

---

## 23. What is Message Based Communication?

Services communicate via messages through a message broker.

### Components:

- **Producer**: Sends messages
- **Message Broker**: Stores and routes messages (Kafka, RabbitMQ, SQS)
- **Consumer**: Receives messages

### Patterns:

- **Point-to-Point**: One consumer per message
- **Pub/Sub**: Multiple subscribers

### Benefits:

- Decoupling, scalability, fault tolerance, load leveling

---

## 24. What is Web Server?

Software that serves web content over HTTP/HTTPS.

### Functions:

- Serve static files
- Reverse proxy
- Load balancing
- SSL termination

### Popular Web Servers:

Nginx, Apache, IIS, Caddy

---

## 25. What is Communication Protocol in Computer Network?

Rules governing data exchange between systems.

### Common Protocols:

| Layer           | Protocols                    |
| --------------- | ---------------------------- |
| **Application** | HTTP, HTTPS, WebSocket, gRPC |
| **Transport**   | TCP, UDP                     |
| **Network**     | IP, ICMP                     |

### HTTP vs WebSocket vs gRPC:

| Protocol      | Use Case                | Connection         |
| ------------- | ----------------------- | ------------------ |
| **HTTP**      | Request/Response        | Stateless          |
| **WebSocket** | Real-time bidirectional | Persistent         |
| **gRPC**      | Service-to-service      | Persistent, binary |

---

## 26. REST API | SOA | Microservices | Tier Architecture

### REST API:

- Stateless, resource-based
- HTTP methods: GET, POST, PUT, DELETE
- JSON responses

### SOA (Service-Oriented Architecture):

- Services communicate via ESB
- SOAP/XML typically
- Enterprise integration

### Microservices:

- Small, independent services
- Own database per service
- Lightweight communication (REST/gRPC)

### N-Tier Architecture:

```
Presentation Tier → Business Logic Tier → Data Tier
```

---

## 27. Difference Between Authentication and Authorization

| Aspect       | Authentication | Authorization        |
| ------------ | -------------- | -------------------- |
| **What**     | Who are you?   | What can you do?     |
| **Verifies** | Identity       | Permissions          |
| **When**     | First          | After authentication |
| **Example**  | Login          | Access control       |

---

## 28. Basic Authentication

Credentials sent in HTTP header (Base64 encoded).

```
Authorization: Basic base64(username:password)
```

**Cons:** Credentials sent every request, requires HTTPS

---

## 29. Token Based Authentication

### Flow:

1. User logs in with credentials
2. Server validates and returns token (JWT)
3. Client stores token
4. Token sent with each request
5. Server validates token

### JWT Structure:

```
Header.Payload.Signature
```

**Benefits:** Stateless, scalable, cross-domain

---

## 30. OAuth Authentication

### OAuth 2.0 Flow:

1. User clicks "Login with Google"
2. Redirect to authorization server
3. User grants permission
4. Authorization code returned
5. Exchange code for access token
6. Use token to access resources

### Grant Types:

- Authorization Code (web apps)
- Client Credentials (server-to-server)
- Refresh Token

---

## 31. Forward Proxy and Reverse Proxy Explained

### Forward Proxy:

```
Client → Forward Proxy → Internet → Server
```

- Hides client identity
- Content filtering, caching
- Example: VPN, corporate proxy

### Reverse Proxy:

```
Client → Internet → Reverse Proxy → Server(s)
```

- Hides server identity
- Load balancing, SSL termination
- Example: Nginx, AWS ALB

---

## 32. Reverse Proxy Server

### Functions:

- **Load Balancing**: Distribute traffic
- **SSL Termination**: Handle HTTPS
- **Caching**: Cache responses
- **Compression**: Reduce response size
- **Security**: Hide backend servers, WAF

### Popular: Nginx, HAProxy, Traefik, Envoy

---

## 33. URL Shortener System Design (TinyURL / Bitly)

### Requirements:

- Shorten long URLs
- Redirect short URLs to original
- Analytics (optional)

### High-Level Design:

```
POST /shorten → Generate short code → Store mapping → Return short URL
GET /{code} → Lookup mapping → 301 Redirect
```

### Key Decisions:

**1. Short Code Generation:**

- Base62 encoding (a-z, A-Z, 0-9)
- 7 characters = 62^7 = 3.5 trillion URLs

**2. Database:**

- Key-Value store (Redis) for fast lookups
- SQL for analytics

**3. Scaling:**

- Cache popular URLs
- Consistent hashing for distribution

### Schema:

```
urls: short_code, long_url, created_at, user_id, clicks
```

---

## 34. Dropbox / Google Drive System Design

### Requirements:

- Upload/download files
- Sync across devices
- Share files/folders
- Version history

### High-Level Architecture:

```
Client → Load Balancer → API Servers → Metadata DB + Object Storage
```

### Components:

**1. Block Server:**

- Split files into 4MB chunks
- Deduplicate blocks
- Delta sync (only changed blocks)

**2. Metadata Database:**

- File info, user info, sharing
- PostgreSQL/MySQL

**3. Object Storage:**

- Store file blocks
- AWS S3, Azure Blob

**4. Sync Service:**

- Track file changes
- Notify clients of updates
- WebSocket for real-time sync

### Key Optimizations:

- **Chunking**: Only transfer changed blocks
- **Deduplication**: Same content = same block ID
- **Compression**: Reduce storage/bandwidth
- **CDN**: Fast downloads globally

### Database Schema:

```
users: id, email, storage_used
files: id, user_id, name, path, size, hash, version
blocks: id, file_id, block_hash, order
shares: id, file_id, shared_with, permission
```
