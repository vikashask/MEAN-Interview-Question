# 12 — Must-Know Interview Questions

> **Purpose:** The mandatory conceptual questions you MUST be able to answer clearly to clear any system design or fullstack interview. Organized by topic. Each question has a crisp, interview-ready answer — memorize the bold parts, elaborate from there.
>
> **How to use:** Cover the answer, try to explain it out loud, then check. If you can't explain it in 30 seconds, re-read the linked deep-dive file.

---

## Table of Contents

1. [Scalability & Fundamentals](#1-scalability--fundamentals)
2. [Architecture](#2-architecture)
3. [Networking & Traffic](#3-networking--traffic)
4. [Databases & Data Layer](#4-databases--data-layer)
5. [Caching](#5-caching)
6. [Communication & Messaging](#6-communication--messaging)
7. [Security & Authentication](#7-security--authentication)
8. [Design Patterns & SOLID](#8-design-patterns--solid)
9. [System Design Scenarios](#9-system-design-scenarios)
10. [Distributed Systems](#10-distributed-systems)
11. [DevOps & Reliability](#11-devops--reliability)
12. [Behavioral / Trade-off Questions](#12-behavioral--trade-off-questions)

---

## 1. Scalability & Fundamentals

> Deep dive: [01-fundamentals.md](./01-fundamentals.md)

### Q1. What is scalability? What are the two types?

**Scalability** is a system's ability to handle growing load by adding resources.

| Type | How | Analogy | Limit |
|------|-----|---------|-------|
| **Vertical (Scale Up)** | Add CPU/RAM to one machine | Bigger engine | Hardware ceiling, SPOF |
| **Horizontal (Scale Out)** | Add more machines behind a load balancer | More lanes on highway | Near-infinite |

**Interview tip:** Always say "we'd start vertical for simplicity, then go horizontal when we hit hardware limits or need fault tolerance."

---

### Q2. What is the difference between latency and throughput?

- **Latency** = time to process **one** request (measured in ms)
- **Throughput** = number of requests processed **per second** (RPS)

**Analogy:** Latency = speed of a car. Throughput = cars passing per hour.

They're related but different — you can have low latency but low throughput (fast but one lane), or high throughput with higher latency (many lanes but speed limit).

---

### Q3. What is availability? What are the "nines"?

**Availability** = `Uptime / (Uptime + Downtime) x 100%`

| Nines | Availability | Downtime/Year |
|-------|-------------|---------------|
| Two 9s | 99% | 3.65 days |
| Three 9s | 99.9% | 8.77 hours |
| Four 9s | 99.99% | 52.6 minutes |
| Five 9s | 99.999% | 5.26 minutes |

**How to achieve:** Eliminate single points of failure + redundancy + replication + health checks + auto-failover.

---

### Q4. What is the CAP theorem?

In a **distributed system**, you can guarantee at most **2 of 3**:

- **C**onsistency — all nodes see the same data at the same time
- **A**vailability — every request gets a response
- **P**artition Tolerance — system works despite network failures

**Key insight:** Network partitions **will** happen, so the real choice is **CP vs AP**.

| Choice | Sacrifices | Examples |
|--------|-----------|----------|
| **CP** | Availability during partition | MongoDB, HBase, Redis Cluster |
| **AP** | Consistency (stale reads OK) | Cassandra, DynamoDB, CouchDB |

---

### Q5. What is the difference between strong and eventual consistency?

| Aspect | Strong Consistency | Eventual Consistency |
|--------|-------------------|---------------------|
| **Guarantee** | Every read returns latest write | Reads eventually catch up |
| **Replication** | Synchronous (wait for all replicas) | Asynchronous (ack immediately) |
| **Latency** | Higher | Lower |
| **Availability** | Lower | Higher |
| **Use case** | Banking, inventory, booking | Social media, DNS, shopping carts |

**One-liner:** "Strong = correct but slow. Eventual = fast but temporarily stale."

---

## 2. Architecture

> Deep dive: [02-architecture-styles.md](./02-architecture-styles.md)

### Q6. What is the difference between monolithic and microservices architecture?

| Aspect | Monolithic | Microservices |
|--------|-----------|--------------|
| **Codebase** | Single repo | Multiple repos |
| **Deployment** | All-or-nothing | Independent per service |
| **Scaling** | Scale entire app | Scale individual services |
| **Database** | Shared DB | Database per service |
| **Failure** | One bug = whole system down | Only affected service fails |
| **Complexity** | Low initially, grows fast | High upfront (ops/networking) |

**When to pick:**
- **Monolith:** Small team, MVP, simple app, speed to market
- **Microservices:** Large team, independent scaling needs, high availability required

---

### Q7. What is N-Tier architecture?

Separates an app into **layers** with clear responsibilities:

```
Presentation Tier (UI) -> Business Logic Tier (API/Services) -> Data Tier (Database)
```

Each tier can be scaled, deployed, and developed independently. Most web apps follow this pattern.

---

## 3. Networking & Traffic

> Deep dive: [03-networking-and-traffic.md](./03-networking-and-traffic.md)

### Q8. What is a load balancer? Name the common algorithms.

A **load balancer** distributes incoming traffic across multiple servers to prevent any single server from being overwhelmed.

**Algorithms:** Round Robin, Weighted Round Robin, Least Connections, IP Hash, Least Response Time, Random.

**Layer 4 vs Layer 7:**
- **Layer 4 (Transport):** Routes based on IP/port. Fast, no content inspection.
- **Layer 7 (Application):** Routes based on HTTP headers, URL, cookies. Smarter, slightly slower.

---

### Q9. What is the difference between a load balancer and an API gateway?

| | Load Balancer | API Gateway |
|---|---|---|
| **Job** | Spread traffic evenly | Smart front-door |
| **Features** | Traffic distribution, health checks | Auth, rate limiting, routing, aggregation, transformation |
| **Layer** | L4/L7 | L7 only |
| **Examples** | Nginx, HAProxy, AWS ALB | Kong, AWS API Gateway, Apigee |

**One-liner:** "LB spreads traffic. API Gateway is a smart front-door with auth + rate limiting + routing."

---

### Q10. What is the difference between forward proxy and reverse proxy?

| | Forward Proxy | Reverse Proxy |
|---|---|---|
| **Sits in front of** | Client | Server |
| **Hides** | Client identity | Server identity |
| **Use case** | VPN, corporate proxy, content filtering | Load balancing, SSL termination, caching, WAF |
| **Examples** | Squid, VPN | Nginx, HAProxy, AWS ALB |

**One-liner:** "Forward hides the client. Reverse hides the server."

---

### Q11. Explain HTTP vs WebSocket vs gRPC.

| Protocol | Connection | Format | Best For |
|----------|-----------|--------|----------|
| **HTTP** | Stateless, request-response | Text (JSON) | REST APIs, CRUD operations |
| **WebSocket** | Persistent, bidirectional | Text/Binary | Real-time (chat, notifications, live data) |
| **gRPC** | Persistent, multiplexed | Binary (Protobuf) | Service-to-service, low latency, streaming |

---

## 4. Databases & Data Layer

> Deep dive: [04-data-layer.md](./04-data-layer.md)

### Q12. When would you choose SQL vs NoSQL?

| Criteria | SQL (Relational) | NoSQL |
|----------|-----------------|-------|
| **Schema** | Fixed, structured | Flexible, schema-less |
| **Scaling** | Vertical (hard to shard) | Horizontal (built for it) |
| **Joins** | Powerful, native | Limited or none |
| **ACID** | Full support | Varies (some support it) |
| **Best for** | Transactions, complex queries, relationships | High throughput, flexible data, massive scale |

**Rule of thumb:** "If your data has relationships and you need transactions -> SQL. If you need scale and flexibility -> NoSQL."

---

### Q13. What are the types of NoSQL databases?

| Type | Examples | Use Case |
|------|----------|----------|
| **Key-Value** | Redis, DynamoDB | Caching, sessions, simple lookups |
| **Document** | MongoDB, Firestore | CMS, user profiles, catalogs |
| **Column-Family** | Cassandra, HBase | Time-series, logs, analytics |
| **Graph** | Neo4j, Neptune | Social networks, recommendations, fraud detection |

---

### Q14. What is database sharding? Why is it hard with RDBMS?

**Sharding** = splitting data across multiple database servers using a shard key (e.g., `hash(user_id) % num_shards`).

**Why RDBMS sharding is hard:**
1. **ACID across shards** requires 2-Phase Commit (slow)
2. **JOINs across shards** = expensive network calls
3. **Foreign keys** don't work across shards
4. **Auto-increment IDs** collide across shards

**Solutions:** Read replicas, application-level sharding, distributed SQL (Vitess, CockroachDB, TiDB).

---

### Q15. What is master-slave replication?

- **Master** handles all writes
- **Slaves** (replicas) handle reads only
- Data flows: Master -> Slaves via sync or async replication

**Sync replication:** Strong consistency, higher write latency.
**Async replication:** Eventual consistency, lower write latency.
**Master-Master:** Both accept writes; needs conflict resolution (harder to manage).

---

### Q16. How does database indexing work?

An **index** is a data structure (typically B-Tree) that speeds up lookups from **O(n) full scan** to **O(log n)**.

| Index Type | Best For |
|-----------|----------|
| **B-Tree** | Range queries (default in most DBs) |
| **Hash** | Exact equality lookups |
| **Composite** | Multi-column queries |
| **Full-text** | Text search |

**Optimization tips:** Index columns in WHERE/JOIN/ORDER BY. Use `EXPLAIN ANALYZE`. Avoid `SELECT *`. Don't wrap indexed columns in functions.

---

### Q17. What is denormalization?

Adding **redundant data** to tables to **reduce JOINs** and speed up reads.

**Trade-off:** Faster reads, but slower writes + harder to maintain consistency + more storage.

**When:** Read-heavy systems where query speed matters more than write complexity.

---

### Q18. What is polyglot persistence?

Using **different databases for different use cases** in the same system.

**Example (e-commerce):** Sessions -> Redis, Products -> MongoDB, Orders -> PostgreSQL, Search -> Elasticsearch, Recommendations -> Neo4j.

---

## 5. Caching

> Deep dive: [05-caching.md](./05-caching.md)

### Q19. What are the caching strategies? Explain cache-aside.

| Strategy | How It Works | Trade-off |
|----------|-------------|-----------|
| **Cache-Aside** | App checks cache; on miss, reads DB, then fills cache | Most common. Stale data possible until TTL expires |
| **Write-Through** | Writes go to cache AND DB simultaneously | Always consistent, but slower writes |
| **Write-Behind** | Writes go to cache, DB updated async later | Fastest writes, but risk of data loss if cache crashes |

**Cache-Aside flow:** `App -> Cache.GET(key) -> MISS -> DB.query() -> Cache.SET(key, value) -> return`

---

### Q20. What are cache eviction policies?

| Policy | Evicts | Best For |
|--------|--------|----------|
| **LRU** | Least Recently Used | General purpose (most common) |
| **LFU** | Least Frequently Used | When frequency matters |
| **FIFO** | Oldest entry | Simple, predictable |
| **TTL** | Expired entries | Time-sensitive data |

**Interview answer:** "I'd use LRU for most cases. LFU if access frequency matters. Always set a TTL as a safety net."

---

### Q21. What is the difference between CDN and application-level caching?

| | CDN | Application Cache |
|---|---|---|
| **Where** | Edge servers globally | In-memory on app server |
| **Caches** | Static assets (JS, CSS, images) | Dynamic data, DB query results |
| **Reduces** | Geographic latency | DB/computation load |
| **Examples** | CloudFront, Cloudflare | Redis, Memcached |

---

## 6. Communication & Messaging

> Deep dive: [06-communication-patterns.md](./06-communication-patterns.md)

### Q22. What is the difference between synchronous and asynchronous communication?

| | Synchronous | Asynchronous |
|---|---|---|
| **Blocking** | Yes (caller waits) | No (fire and forget) |
| **Coupling** | Tight | Loose |
| **Example** | REST API call | Message queue, WebSocket |
| **When** | Need immediate response | Work can be deferred, need resilience |

**Analogy:** Sync = phone call (wait for answer). Async = text message (send and move on).

---

### Q23. What is a message queue? When would you use one?

A **message broker** (Kafka, RabbitMQ, SQS) sits between producers and consumers, decoupling them.

**Patterns:**
- **Point-to-Point:** One consumer per message (task queue)
- **Pub/Sub:** Many subscribers per message (event broadcast)

**Use when:** Downstream service is slow/unreliable, work can be deferred, need to smooth traffic spikes, need retry/dead-letter handling.

---

### Q24. What are message delivery guarantees?

| Semantic | How | Risk |
|----------|-----|------|
| **At-most-once** | Ack before processing | Message may be lost |
| **At-least-once** | Ack after processing | Duplicates possible |
| **Exactly-once** | Idempotent producer + transactional consumer | Complex, some perf cost |

**Interview tip:** "At-least-once with idempotent consumers is the most practical approach for most systems."

---

## 7. Security & Authentication

> Deep dive: [07-security-and-auth.md](./07-security-and-auth.md)

### Q25. What is the difference between authentication and authorization?

| | Authentication (AuthN) | Authorization (AuthZ) |
|---|---|---|
| **Question** | "Who are you?" | "What can you do?" |
| **Verifies** | Identity | Permissions |
| **When** | First (login) | After authentication |
| **Example** | Username/password, JWT, biometrics | Roles, ACL, policies |

**Analogy:** AuthN = passport check at airport. AuthZ = boarding pass check at gate.

---

### Q26. How does JWT authentication work? Why is it stateless?

**Flow:** User logs in -> server creates JWT (Header.Payload.Signature) -> client stores it -> sends with every request in `Authorization: Bearer <token>` -> server verifies signature.

**Stateless because:** The token contains all needed info (user ID, roles, expiry) and is self-verifying via the signature. No server-side session lookup needed.

**Trade-off:** Can't revoke a JWT before expiry without a blacklist (which adds state). Use short-lived access tokens + refresh tokens.

---

### Q27. Explain OAuth 2.0 in simple terms.

OAuth lets users **grant limited access** to their data on one service to another service, **without sharing their password**.

**Flow ("Login with Google"):**
1. User clicks "Login with Google" on your app
2. Your app redirects to Google's auth page
3. User approves the permissions
4. Google sends an **authorization code** back to your app
5. Your app exchanges the code for an **access token**
6. Your app uses the token to fetch user's profile from Google

**Key insight:** Your app never sees the user's Google password. The access token has limited scope and expires.

---

### Q28. What is SSO (Single Sign-On)?

**SSO** lets a user log in **once** and access **multiple applications** without re-authenticating.

**Flow:** User -> App A -> redirects to Identity Provider (IdP) -> user authenticates once -> gets token (SAML/JWT) -> presents token to App A, App B, App C -> all grant access.

**Examples:** Google Workspace (one login for Gmail, Drive, Calendar), corporate Okta/Azure AD.

---

### Q29. What are rate limiting algorithms?

| Algorithm | How It Works | Pros | Cons |
|-----------|-------------|------|------|
| **Token Bucket** | Tokens added at fixed rate; request consumes one | Handles bursts | Per-user state |
| **Leaky Bucket** | Requests queue, drain at constant rate | Smooth output | Adds latency |
| **Fixed Window** | Count per time window | Simple | Burst at window boundary |
| **Sliding Window** | Weighted count across two windows | Accurate + efficient | Slightly complex |

**Interview answer:** "Token bucket for APIs that need to allow bursts. Sliding window counter for distributed rate limiting with Redis."

---

## 8. Design Patterns & SOLID

> Deep dive: [08-design-patterns.md](./08-design-patterns.md)

### Q30. What are the SOLID principles?

| Principle | Meaning | Example |
|-----------|---------|---------|
| **S** - Single Responsibility | A class should have one reason to change | `UserService` handles users, not emails |
| **O** - Open/Closed | Open for extension, closed for modification | Add new payment methods without changing existing code |
| **L** - Liskov Substitution | Subtypes must be usable via base type | A `Square` should work wherever `Rectangle` is expected |
| **I** - Interface Segregation | Many small interfaces > one fat interface | `Printable` and `Scannable` instead of `Machine` |
| **D** - Dependency Inversion | Depend on abstractions, not concretions | Inject `Logger` interface, not `ConsoleLogger` directly |

**Also know:** DRY (don't repeat), KISS (keep simple), YAGNI (you ain't gonna need it).

---

### Q31. What is the difference between Factory and Builder patterns?

| | Factory | Builder |
|---|---|---|
| **Purpose** | Choose WHICH object to create | Build a COMPLEX object step by step |
| **Returns** | One of several concrete types | One fully-configured object |
| **When** | `createLogger('prod')` -> FileLogger or ConsoleLogger | `new QueryBuilder().select(...).from(...).where(...).build()` |

---

### Q32. Explain the Observer pattern. Where is it used?

**Observer** = one-to-many notification. When the subject's state changes, all registered observers are notified.

**Real-world uses:** EventEmitter in Node.js, RxJS Observables in Angular, React useState/useEffect, DOM event listeners, Kafka consumers.

**Pub/Sub vs Observer:** Observer = subject knows its subscribers directly. Pub/Sub = a broker mediates, publishers and subscribers are fully decoupled.

---

### Q33. What is the Strategy pattern?

Defines a **family of algorithms**, encapsulates each one, and makes them **interchangeable at runtime**.

```ts
const pricing = {
  standard: (cart) => cart.total,
  discount: (cart) => cart.total * 0.9,
  vip:      (cart) => cart.total * 0.8,
};
function checkout(cart, strategy = 'standard') {
  return pricing[strategy](cart);
}
```

**Use when:** You have multiple algorithms for the same task and want to swap them without changing the calling code. Eliminates long if/else chains.

---

### Q34. What is the Decorator pattern?

**Attaches additional responsibilities** to an object dynamically, without modifying its class.

**Real-world:** Express middleware (logging, auth, compression wrapping the handler), React HOCs, Python `@decorator` syntax.

**Key:** Each decorator wraps the original and adds behavior before/after delegating to it.

---

### Q35. Name 3 common anti-patterns to avoid.

| Anti-pattern | Problem | Fix |
|-------------|---------|-----|
| **God Object** | One class does everything | Split into focused classes (SRP) |
| **Singleton Abuse** | Hidden global state, hard to test | Use dependency injection |
| **Excessive Inheritance** | Deep class hierarchies, fragile | Prefer composition over inheritance |

---

## 9. System Design Scenarios

> Deep dive: [09-case-studies.md](./09-case-studies.md)

### Q36. Design a URL shortener — key decisions?

1. **ID generation:** Base62 encoding (a-z, A-Z, 0-9). 7 chars = 62^7 = 3.5 trillion URLs
2. **Storage:** Key-value store (Redis) for O(1) lookups + relational DB for analytics
3. **Redirect:** 302 (temporary) for analytics tracking, 301 (permanent) if you don't need analytics
4. **Caching:** Cache top 20% most-accessed URLs (Pareto principle), LRU eviction, 24h TTL

---

### Q37. How does Twitter's news feed work? What is the fan-out problem?

**Fan-out problem:** When a celebrity with 50M followers posts, writing to all 50M feed caches is extremely expensive.

**Solution — Hybrid approach:**
- **Normal users (< 10K followers):** Fan-out on WRITE (push to all follower caches) -> fast reads
- **Celebrities (> 10K followers):** Fan-out on READ (merge their posts at read time) -> avoids write storms
- **Feed ranking:** Score = relevance x recency x engagement (ML model)

---

### Q38. How would you design a ride-sharing service (Uber)?

**Key components:**
1. **Location Service:** Ingest driver pings every 4-5s -> store in Redis GEO with geohash indexing
2. **Matching Service:** Get rider's geohash -> query nearby drivers -> filter available -> score by distance + rating -> lock driver
3. **Surge Pricing:** Supply/demand ratio per zone. Low supply = higher multiplier
4. **Reliability:** WebSocket for real-time updates, Kafka for event processing, PostgreSQL for ride records

---

### Q39. How would you design Netflix's video streaming?

**Pipeline:** Upload -> Raw Storage (S3) -> Transcoding Queue (Kafka) -> FFmpeg Workers (360p/720p/1080p/4K) -> CDN Storage -> CDN Edge Servers -> User

**Key decisions:**
- **Adaptive bitrate streaming** (HLS/DASH) — adjusts quality to network conditions
- **CDN** for global low-latency delivery
- **Pre-warm CDN cache** for trending/newly released content
- **Cassandra** for metadata (write-heavy, time-series)

---

## 10. Distributed Systems

### Q40. What is consistent hashing? Why is it used?

**Problem:** Simple `hash(key) % N` breaks when you add/remove servers — almost all keys get reassigned.

**Solution:** Consistent hashing uses a hash **ring**. Each server owns a range on the ring. Adding/removing a server only reassigns keys near that position (~1/N of keys move instead of all).

**Virtual nodes (vnodes):** Each physical server gets ~150 positions on the ring to ensure even distribution.

**Used in:** DynamoDB, Cassandra, load balancers, distributed caches.

---

### Q41. What is a consensus algorithm? Name two.

**Consensus** = getting distributed nodes to agree on a value despite failures.

- **Raft:** Leader-based. Leader replicates log to followers. On leader failure, followers elect a new leader. Easier to understand. Used by etcd, CockroachDB.
- **Paxos:** Multi-proposer. More complex, more theoretical. Used by Google Chubby, original Zookeeper.

**Use case:** Leader election, distributed config, replicated state machines.

---

### Q42. What is the difference between 2-Phase Commit and Saga pattern?

| | 2-Phase Commit (2PC) | Saga Pattern |
|---|---|---|
| **How** | Coordinator asks all to prepare, then commit | Chain of local transactions with compensating actions |
| **Consistency** | Strong (all-or-nothing) | Eventual |
| **Availability** | Blocks if coordinator fails | No blocking |
| **Use case** | Small number of participants | Microservices, long-running workflows |

---

### Q43. What is a circuit breaker pattern?

When a downstream service is failing, the **circuit breaker** stops sending requests to it (instead of overwhelming it with retries).

**States:** Closed (normal) -> Open (failing, reject immediately) -> Half-Open (test with limited requests) -> back to Closed if recovered.

**Use with:** Retry with exponential backoff + jitter, timeout, bulkhead (isolate failures).

---

## 11. DevOps & Reliability

### Q44. What is the difference between horizontal and vertical scaling of a database?

- **Vertical:** Upgrade CPU/RAM of the DB server. Simple but has limits.
- **Horizontal reads:** Add read replicas (master-slave). Scales reads, not writes.
- **Horizontal writes:** Shard the database. Scales writes but adds complexity (cross-shard joins, distributed transactions).

**Typical path:** Optimize queries -> add indexes -> vertical scale -> read replicas -> caching layer -> sharding (last resort).

---

### Q45. How do you eliminate single points of failure?

1. **Load balancer** in front of app servers (use multiple LBs too)
2. **Database replicas** with automatic failover
3. **Multi-AZ / multi-region** deployment
4. **Redundant components** (backup DNS, multiple ISPs)
5. **Health checks** + auto-restart + auto-scaling

---

### Q46. What is the difference between blue-green and canary deployments?

| | Blue-Green | Canary |
|---|---|---|
| **How** | Two identical environments. Switch traffic from blue to green | Roll out to small % of users first |
| **Rollback** | Instant (switch back to blue) | Remove canary instances |
| **Cost** | 2x infrastructure during deploy | Minimal extra infra |
| **Risk** | All-or-nothing switch | Gradual, lower risk |

---

## 12. Behavioral / Trade-off Questions

### Q47. How do you approach a system design problem you've never seen?

Use **RADIO:**
1. **Requirements:** Ask clarifying questions. Define functional + non-functional reqs. Estimate scale (DAU, RPS, storage).
2. **Architecture:** Draw high-level boxes (client, LB, services, DB, cache, CDN).
3. **Deep Dive:** Pick the most interesting/challenging component and detail it.
4. **Issues:** Identify bottlenecks, SPOFs, failure modes.
5. **Optimize:** Add caching, sharding, CDN, async processing, replicas.

**Key:** Narrate your thought process. Interviewers evaluate HOW you think, not just the final answer.

---

### Q48. When would you choose consistency over availability (and vice versa)?

**Choose consistency (CP):**
- Banking (can't show wrong balance)
- Inventory (can't oversell)
- Booking systems (can't double-book)

**Choose availability (AP):**
- Social media (stale post counts are OK)
- DNS (eventual propagation is fine)
- Shopping carts (user can retry)

**Interview tip:** "It depends on the business impact of stale data vs. downtime. I'd ask: what happens if a user sees outdated data for 5 seconds? If the answer is 'people lose money' -> CP. If 'nobody notices' -> AP."

---

### Q49. How would you reduce infrastructure costs by 30%?

**Systematic approach:**
1. **Measure first:** AWS Cost Explorer, Datadog, query profiler
2. **Quick wins:** Right-size instances (20-40% saving), reserved instances (40-70%), S3 lifecycle policies
3. **Strategic:** Serverless for bursty workloads, caching to reduce DB load, auto-scaling instead of over-provisioning
4. **Governance:** Tag resources, budget alerts at 80%, monthly FinOps reviews

---

### Q50. What is your process for making technology decisions?

1. **Define requirements** (functional, non-functional, constraints)
2. **Identify options** (at least 2-3 alternatives)
3. **Evaluate trade-offs** (performance, cost, complexity, team expertise, community support)
4. **Prototype if uncertain** (spike / proof of concept)
5. **Document the decision** (Architecture Decision Record — ADR)
6. **Review and iterate** (decisions aren't permanent, plan for change)

---

## Quick Self-Test Checklist

Before your interview, make sure you can explain these in under 30 seconds each:

| # | Can you explain...? | File |
|---|---|---|
| 1 | Vertical vs horizontal scaling | 01 |
| 2 | CAP theorem and when to pick CP vs AP | 01 |
| 3 | Strong vs eventual consistency | 01 |
| 4 | Monolith vs microservices trade-offs | 02 |
| 5 | Load balancer vs API gateway | 03 |
| 6 | Forward vs reverse proxy | 03 |
| 7 | SQL vs NoSQL — when to pick each | 04 |
| 8 | Database sharding and why it's hard | 04 |
| 9 | Cache-aside vs write-through | 05 |
| 10 | Sync vs async communication | 06 |
| 11 | Message queue use cases | 06 |
| 12 | JWT — how it works, why stateless | 07 |
| 13 | OAuth 2.0 flow | 07 |
| 14 | Rate limiting algorithms | 07 |
| 15 | SOLID principles | 08 |
| 16 | Factory vs Builder vs Strategy | 08 |
| 17 | Observer vs Pub/Sub | 08 |
| 18 | URL shortener key decisions | 09 |
| 19 | Fan-out problem (Twitter feed) | 09 |
| 20 | Consistent hashing | 10 |

> **If you can confidently explain all 20 in a mock interview, you're ready.**

---

*Cross-references: Each answer links to the deep-dive file for full diagrams, code examples, and mermaid visuals. Use those files to fill gaps, use this file to test recall.*
