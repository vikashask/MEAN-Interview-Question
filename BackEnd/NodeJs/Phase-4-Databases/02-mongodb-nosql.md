# MongoDB & NoSQL

## MongoDB Basics

```javascript
const { MongoClient } = require("mongodb");

const client = new MongoClient("mongodb://localhost:27017");

async function connect() {
  await client.connect();
  const db = client.db("mydb");
  const collection = db.collection("users");

  // CRUD operations
  await collection.insertOne({ name: "John", email: "john@example.com" });
  const user = await collection.findOne({ email: "john@example.com" });
  await collection.updateOne({ _id: user._id }, { $set: { age: 30 } });
  await collection.deleteOne({ _id: user._id });
}
```

## Document Structure

```javascript
// Flexible schema
const user = {
  _id: ObjectId(),
  name: "John",
  email: "john@example.com",
  age: 30,
  tags: ["nodejs", "mongodb"],
  address: {
    street: "123 Main St",
    city: "New York",
    zip: "10001",
  },
  createdAt: new Date(),
};

// Insert document
await collection.insertOne(user);

// Insert multiple
await collection.insertMany([user1, user2, user3]);
```

## Querying

```javascript
// Find all
const users = await collection.find({}).toArray();

// Find with filter
const users = await collection.find({ age: { $gt: 18 } }).toArray();

// Find one
const user = await collection.findOne({ email: "john@example.com" });

// Operators
// $eq, $ne, $gt, $gte, $lt, $lte
// $in, $nin
// $and, $or, $not
// $exists, $type
// $regex

const results = await collection
  .find({
    age: { $gte: 18, $lt: 65 },
    status: { $in: ["active", "pending"] },
  })
  .toArray();
```

## Updates

```javascript
// Update one
await collection.updateOne(
  { _id: userId },
  { $set: { age: 30, status: "active" } }
);

// Update multiple
await collection.updateMany(
  { status: "inactive" },
  { $set: { status: "archived" } }
);

// Operators
// $set - set field value
// $unset - remove field
// $inc - increment value
// $push - add to array
// $pull - remove from array
// $addToSet - add to set (no duplicates)

await collection.updateOne(
  { _id: userId },
  {
    $set: { lastLogin: new Date() },
    $inc: { loginCount: 1 },
    $push: { loginHistory: new Date() },
  }
);
```

## Aggregation

```javascript
// Aggregation pipeline
const results = await collection
  .aggregate([
    { $match: { age: { $gte: 18 } } },
    { $group: { _id: "$status", count: { $sum: 1 } } },
    { $sort: { count: -1 } },
    { $limit: 10 },
  ])
  .toArray();

// Stages
// $match - filter documents
// $project - select fields
// $group - group by field
// $sort - sort results
// $limit - limit results
// $skip - skip results
// $lookup - join collections
// $unwind - flatten arrays

// Join example
const results = await collection
  .aggregate([
    {
      $lookup: {
        from: "posts",
        localField: "_id",
        foreignField: "userId",
        as: "posts",
      },
    },
  ])
  .toArray();
```

## Indexing

```javascript
// Create indexes
await collection.createIndex({ email: 1 });
await collection.createIndex({ age: 1, status: 1 });
await collection.createIndex({ name: "text" }); // Text index

// Index options
await collection.createIndex({ email: 1 }, { unique: true, sparse: true });

// List indexes
const indexes = await collection.listIndexes().toArray();

// Drop index
await collection.dropIndex("email_1");
```

## Transactions

```javascript
const session = client.startSession();

try {
  await session.withTransaction(async () => {
    const usersCollection = db.collection("users");
    const logsCollection = db.collection("logs");

    await usersCollection.insertOne({ name: "John" }, { session });
    await logsCollection.insertOne({ action: "User created" }, { session });
  });
} finally {
  await session.endSession();
}
```

## Schema Validation

```javascript
// Define schema
const schema = {
  $jsonSchema: {
    bsonType: "object",
    required: ["name", "email"],
    properties: {
      _id: { bsonType: "objectId" },
      name: { bsonType: "string" },
      email: { bsonType: "string" },
      age: { bsonType: "int", minimum: 0 },
      tags: {
        bsonType: "array",
        items: { bsonType: "string" },
      },
    },
  },
};

// Create collection with validation
await db.createCollection("users", { validator: schema });
```
