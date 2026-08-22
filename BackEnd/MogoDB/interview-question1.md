# MongoDB Interview Questions — Quick Revision Guide

> Organized by topic for fast revision. Each answer is interview-ready with extra context where it helps recall.

---

## Table of Contents
1. [Fundamentals & NoSQL Basics](#1-fundamentals--nosql-basics)
2. [MongoDB vs SQL vs Other NoSQL DBs](#2-mongodb-vs-sql-vs-other-nosql-dbs)
3. [Data Modeling & Relationships](#3-data-modeling--relationships)
4. [ObjectID, Namespace & Documents](#4-objectid-namespace--documents)
5. [Indexes](#5-indexes)
6. [Aggregation Framework](#6-aggregation-framework)
7. [Replication](#7-replication)
8. [Sharding](#8-sharding)
9. [Transactions & Locking](#9-transactions--locking)
10. [Storage Engine & Disk Behavior](#10-storage-engine--disk-behavior)
11. [Performance & Operational Notes](#11-performance--operational-notes)
12. [One-Line Cheat Sheet](#12-one-line-cheat-sheet)

---

## 1. Fundamentals & NoSQL Basics

**Q: What are the best features of MongoDB?**
- Document-oriented (stores data as BSON documents, not rows/tables)
- High performance (in-memory-friendly, efficient indexing)
- High availability (via replica sets)
- Easy horizontal scalability (via sharding)
- Rich, expressive query language (supports joins-like `$lookup`, aggregation, geospatial, text search)

**Q: What are NoSQL databases? What types exist?**
NoSQL databases store and retrieve data using models other than the tabular relations of RDBMS (SQL/Oracle). They're built for scale, flexible schemas, and specific access patterns.

Types of NoSQL databases:
| Type | Example | Best For |
|---|---|---|
| Document Oriented | MongoDB, CouchDB | Semi-structured, nested data |
| Key-Value | Redis, DynamoDB | Caching, simple lookups |
| Column Oriented | Cassandra, HBase | Wide-column, analytics |
| Graph | Neo4j | Relationship-heavy data (social graphs) |

**Q: What kind of NoSQL database is MongoDB?**
A **document-oriented** database. It stores data as **BSON** (Binary JSON) documents, grouped into **collections** (analogous to tables).

**Q: Most important features of MongoDB?**
- Flexible schema (documents in the same collection can differ in structure)
- Agile and highly scalable
- Faster than traditional RDBMS for many workloads (denormalized reads)
- Expressive query language + aggregation pipeline

---

## 2. MongoDB vs SQL vs Other NoSQL DBs

**Q: Compare SQL databases and MongoDB at a high level.**
| | SQL (RDBMS) | MongoDB |
|---|---|---|
| Structure | Tables, rows, columns | Collections, documents (BSON) |
| Schema | Fixed/predefined | Flexible/dynamic |
| Relationships | Foreign keys, JOINs | Embedding or manual references (`$lookup`) |
| Scaling | Vertical (mostly) | Horizontal (sharding) |
| Best for | Highly relational, transactional data | Rapidly evolving, hierarchical/nested data |

**Q: How is MongoDB better than other SQL databases?**
- Flexible document structure — one document can have 5 fields, another in the same collection can have 10, no migration needed.
- Efficient indexing and storage layout often gives faster reads/writes for document-shaped data.
- Horizontal scaling out of the box via sharding.

**Q: Compare MongoDB and CouchDB at a high level.**
Both are document-oriented, but:
- **MongoDB** — better for **dynamic queries** and **high performance on very large datasets**.
- **CouchDB** — better for **predefined/occasionally-changing queries** and offline-first/multi-master replication use cases.

---

## 3. Data Modeling & Relationships

**Q: Does MongoDB support foreign key constraints?**
No. There's no built-in referential integrity — relationships are handled at the application level or via embedding.

**Q: How can you achieve primary key–foreign key style relationships?**
By **embedding** one document inside another (denormalization), e.g., embedding an `address` document inside a `customer` document. For many-to-many or large sub-documents, use **manual references** (store an `_id` and query separately, or use `$lookup` in aggregation).

**Q: When should you embed one document within another?**
Embed when there is:
- A **"contains"** relationship between entities (e.g., order contains line items)
- A **one-to-many** relationship where the "many" side is small/bounded
- A need for **performance** (single read fetches everything, no joins needed)

> Rule of thumb: **Embed for data accessed together; reference for data that's large, frequently updated independently, or shared across many documents.**

**Q: Does MongoDB need a lot of RAM?**
No. MongoDB can run on modest RAM — it dynamically allocates/deallocates memory based on system needs and working-set size. More RAM helps performance (indexes/working set fit in memory) but isn't a hard requirement.

---

## 4. ObjectID, Namespace & Documents

**Q: What is a Namespace in MongoDB?**
The concatenation of **database name + collection name**, e.g., `school.students` (database: `school`, collection: `students`).

**Q: Which languages have official MongoDB driver support?**
C, C++, C#, Java, Node.js, Perl, PHP, Python, Ruby, Scala, Go, Erlang — plus community-supported drivers for other languages.

**Q: Explain the structure of ObjectID in MongoDB.**
`ObjectID` is a **12-byte** BSON type composed of:
| Bytes | Meaning |
|---|---|
| 4 bytes | Timestamp (seconds since epoch) |
| 3 bytes | Machine identifier |
| 2 bytes | Process ID |
| 3 bytes | Incrementing counter |

This makes it unique across machines/processes without needing a central counter, and it's roughly sortable by creation time.

**Q: MongoDB uses BSON to represent document structures. True or False?**
**True.** BSON (Binary JSON) extends JSON with additional types (dates, binary data, ObjectId, etc.) and is more efficient to parse/traverse.

**Q: If you remove a document from the database, is it removed from disk?**
Yes — deleting a document removes it from disk (space may be reused/reclaimed depending on storage engine, but the document itself is gone).

**Q: Command to insert a document into `school.persons`.**
```js
use school
db.persons.insert({ name: "kadhir", dept: "CSE" })
// Modern syntax:
db.persons.insertOne({ name: "kadhir", dept: "CSE" })
```

---

## 5. Indexes

**Q: What are Indexes in MongoDB?**
Indexes support efficient query execution. Without an index, MongoDB performs a **collection scan** — checking every document. With an appropriate index, MongoDB can limit the documents it must inspect, drastically improving query speed.

**Q: How many indexes does MongoDB create by default for a new collection?**
**One** — the default index on `_id` for every collection.

**Q: Can you create an index on an array field? What happens?**
Yes. MongoDB creates a **multikey index**, indexing **each element of the array** individually.

**Q: What is a covered query?**
A query where:
1. All fields used in the query are part of an index, **and**
2. All fields returned in the results are also in that same index.

Because everything needed is in the index, MongoDB never has to load the full document — it answers entirely from the index (which lives in RAM or is stored sequentially on disk), making it **significantly faster**.

**Q: Does MongoDB support text search?**
Yes — via **text indexes**, which support search inside string content. Introduced in v2.6.

**Q: What happens if an index doesn't fit into RAM?**
MongoDB has to read index pages from disk, which is much slower than RAM access — query performance degrades.

**Q: Command to list all indexes on a collection.**
```js
db.collection.getIndexes()
```

---

## 6. Aggregation Framework

**Q: What is Aggregation in MongoDB?**
A framework for processing data records and returning **computed results** — grouping values across documents and applying operations (sum, avg, group, filter, reshape, join) to produce a single/summarized result.

Three ways to aggregate in MongoDB:
1. **Aggregation pipeline** (`db.collection.aggregate([...])`) — most common, stage-based (`$match`, `$group`, `$project`, `$lookup`, etc.)
2. **Map-reduce** — legacy, JavaScript-based, largely superseded by the pipeline
3. **Single-purpose aggregation methods** — e.g., `count()`, `distinct()`

---

## 7. Replication

**Q: What is Replication in MongoDB?**
The process of **synchronizing data across multiple servers** (a **replica set**). It provides:
- Redundancy and increased data availability
- Protection against loss of a single server
- Automatic failover / recovery from hardware failure

**Q: What are Primary and Secondary replica sets?**
- **Primary** — the only node that accepts **writes**. MongoDB replication is **single-master**.
- **Secondary** — read-only nodes that replicate data from the primary (can serve reads if configured, e.g., with read preferences).

**Q: By default, does MongoDB write/read from both primary and secondary?**
**False.** By default, all writes and reads go to the **primary** only. Reading from secondaries requires explicit read preference configuration (e.g., `secondaryPreferred`), and returns eventually-consistent data.

---

## 8. Sharding

**Q: What is Sharding in MongoDB?**
A method of **horizontally distributing data across multiple machines (shards)**. Used to support very large datasets and high-throughput operations that a single server can't handle.

Key components:
- **Shard** — holds a subset of the data
- **mongos** — query router that directs operations to the right shard(s)
- **Config servers** — store cluster metadata and chunk distribution
- **Shard key** — determines how data is distributed across shards (choosing a good shard key is critical for even distribution)

---

## 9. Transactions & Locking

**Q: Does MongoDB support ACID transactions and locking?**
Historically: No multi-document ACID transactions, only **atomic operations on a single document**.
> Note: Since MongoDB 4.0+, **multi-document ACID transactions** are supported (especially within replica sets, and across shards since 4.2). Still, for performance, favor schema designs that minimize the need for multi-document transactions.

**Q: How can you achieve transaction-like behavior/locking without multi-doc transactions?**
Use **nesting/embedded documents** so related data updates happen within a **single document**, which is always atomic in MongoDB.

---

## 10. Storage Engine & Disk Behavior

**Q: What is a Storage Engine in MongoDB?**
The component responsible for **how data is managed/stored on disk**. Different engines trade off differently for read-heavy vs. write-heavy workloads.

**Q: Which storage engines does MongoDB use?**
- **MMAPv1** — legacy, memory-mapped files (deprecated in newer versions)
- **WiredTiger** — default since MongoDB 3.2; supports document-level concurrency control and compression

**Q: Does MongoDB write to disk immediately or lazily?**
**Lazily.** Writes are first recorded in the **journal** (write-ahead log) immediately for durability, but the actual data files on disk are updated lazily/periodically.

**Q: At what interval does MongoDB write updates to disk?**
By default, roughly every **60 seconds** (configurable via `commitIntervalMs` / `syncPeriodSecs`, exact defaults vary by version — WiredTiger checkpoints default to 60s).

**Q: Why are MongoDB data files large in size?**
MongoDB (particularly with MMAPv1) **preallocates** data files in advance to reserve disk space and avoid filesystem fragmentation.

---

## 11. Performance & Operational Notes

**Q: Why is MongoDB not preferred on a 32-bit system?**
A 32-bit build limits total storage (data + indexes) to about **2 GB**. This is a hard address-space limitation — never deploy MongoDB in production on 32-bit machines. On **64-bit** builds, there's effectively no such storage ceiling.

---

## 12. One-Line Cheat Sheet

| Topic | One-liner |
|---|---|
| Data model | Document (BSON) inside collections, no fixed schema |
| Default index | `_id` on every collection |
| Relationship style | Embed for "contains"/1-to-many/perf; reference otherwise |
| Transactions | Atomic per document; multi-doc ACID since v4.0+ |
| Write durability | Journal immediately, data files lazily (~60s) |
| Scale up | Sharding (horizontal) |
| Scale availability | Replication (replica sets, primary + secondaries) |
| Default storage engine | WiredTiger |
| Text search | Text indexes (since v2.6) |
| Covered query | Query fully answered by index, no document fetch |
