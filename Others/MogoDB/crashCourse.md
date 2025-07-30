# MongoDB Crash Course

## Basic Concepts

### Documents
MongoDB stores data in flexible, JSON-like documents. Example:
```json
{
    "name": "John Doe",
    "age": 30,
    "email": "john@example.com",
    "address": {
        "street": "123 Main St",
        "city": "Boston",
        "state": "MA"
    }
}
```

### Collections
Collections are groups of documents. Similar to tables in relational databases.

## Basic Operations (CRUD)

### Create Operations

#### Insert One Document
```javascript
db.users.insertOne({
    name: "John Doe",
    age: 30,
    email: "john@example.com"
})
```

#### Insert Multiple Documents
```javascript
db.users.insertMany([
    { name: "Jane Smith", age: 25 },
    { name: "Bob Wilson", age: 35 }
])
```

### Read Operations

#### Find Documents
```javascript
// Find all documents
db.users.find()

// Find with conditions
db.users.find({ age: { $gt: 25 } })

// Find one document
db.users.findOne({ name: "John Doe" })
```

#### Query Operators
```javascript
// Greater than
db.users.find({ age: { $gt: 25 } })

// Less than
db.users.find({ age: { $lt: 30 } })

// In array
db.users.find({ status: { $in: ["active", "pending"] } })

// And condition
db.users.find({
    $and: [
        { age: { $gt: 25 } },
        { status: "active" }
    ]
})
```

### Update Operations

#### Update One Document
```javascript
db.users.updateOne(
    { name: "John Doe" },
    { $set: { age: 31 } }
)
```

#### Update Multiple Documents
```javascript
db.users.updateMany(
    { status: "inactive" },
    { $set: { status: "active" } }
)
```

#### Update Operators
```javascript
// Increment value
db.users.updateOne(
    { name: "John Doe" },
    { $inc: { age: 1 } }
)

// Add to array
db.users.updateOne(
    { name: "John Doe" },
    { $push: { hobbies: "reading" } }
)
```

### Delete Operations

#### Delete One Document
```javascript
db.users.deleteOne({ name: "John Doe" })
```

#### Delete Multiple Documents
```javascript
db.users.deleteMany({ status: "inactive" })
```

## Indexing

### Create Index
```javascript
// Single field index
db.users.createIndex({ email: 1 })

// Compound index
db.users.createIndex({ 
    email: 1, 
    name: 1 
})

// Unique index
db.users.createIndex(
    { email: 1 },
    { unique: true }
)
```

### List Indexes
```javascript
db.users.getIndexes()
```

### Drop Index
```javascript
db.users.dropIndex("index_name")
```

## Aggregation Pipeline

### Basic Aggregation
```javascript
db.orders.aggregate([
    // Match stage
    { $match: { status: "completed" } },
    
    // Group stage
    { $group: {
        _id: "$customerId",
        totalAmount: { $sum: "$amount" }
    }},
    
    // Sort stage
    { $sort: { totalAmount: -1 } }
])
```

### Common Aggregation Operators

#### $match
```javascript
{ $match: { status: "active" } }
```

#### $group
```javascript
{ $group: {
    _id: "$category",
    count: { $sum: 1 },
    avgPrice: { $avg: "$price" }
}}
```

#### $sort
```javascript
{ $sort: { name: 1 } }
```

#### $project
```javascript
{ $project: {
    name: 1,
    email: 1,
    _id: 0
}}
```

## Data Modeling

### One-to-One Relationship
```javascript
// User document
{
    _id: ObjectId("..."),
    name: "John Doe",
    profile: {
        age: 30,
        address: "123 Main St"
    }
}
```

### One-to-Many Relationship
```javascript
// User document
{
    _id: ObjectId("..."),
    name: "John Doe",
    orders: [
        { orderId: "001", amount: 100 },
        { orderId: "002", amount: 200 }
    ]
}
```

### Many-to-Many Relationship
```javascript
// Users collection
{
    _id: ObjectId("..."),
    name: "John Doe"
}

// Groups collection
{
    _id: ObjectId("..."),
    name: "Admins"
}

// UserGroups collection
{
    userId: ObjectId("..."),
    groupId: ObjectId("...")
}
```

## Best Practices

1. Schema Design
   - Design for how data is accessed
   - Consider embedding vs referencing
   - Plan for data growth

2. Indexing
   - Create indexes for frequent queries
   - Avoid over-indexing
   - Use compound indexes effectively

3. Performance
   - Use proper query operators
   - Limit result sets
   - Use projection to return only needed fields

4. Security
   - Use authentication
   - Implement role-based access control
   - Encrypt sensitive data

## Common Commands

### Database Commands
```javascript
// Show databases
show dbs

// Switch database
use dbname

// Show collections
show collections

// Drop database
db.dropDatabase()
```

### Collection Commands
```javascript
// Create collection
db.createCollection("users")

// Drop collection
db.users.drop()

// Rename collection
db.users.renameCollection("newUsers")
```

### Administrative Commands
```javascript
// Get server status
db.serverStatus()

// Current operations
db.currentOp()

// Kill operation
db.killOp(opId)
```
