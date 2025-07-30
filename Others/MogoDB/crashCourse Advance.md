# MongoDB Advanced Concepts

## Aggregation Pipeline

### Basic Pipeline Operations
```javascript
db.orders.aggregate([
    // Match stage - like find
    { $match: { status: "completed" } },
    
    // Group stage
    { $group: {
        _id: "$customerId",
        totalSpent: { $sum: "$total" },
        orderCount: { $sum: 1 }
    }},
    
    // Sort stage
    { $sort: { totalSpent: -1 } }
]);
```

### Complex Aggregations
```javascript
db.sales.aggregate([
    // Unwind arrays
    { $unwind: "$items" },
    
    // Project new fields
    { $project: {
        item: "$items.name",
        amount: { $multiply: ["$items.price", "$items.quantity"] }
    }},
    
    // Group with multiple operations
    { $group: {
        _id: "$item",
        totalSold: { $sum: "$amount" },
        averagePrice: { $avg: "$items.price" },
        count: { $sum: 1 }
    }},
    
    // Having clause equivalent
    { $match: {
        totalSold: { $gt: 1000 }
    }}
]);
```

## Indexes

### Single Field Index
```javascript
// Create index
db.users.createIndex({ email: 1 });

// Unique index
db.users.createIndex(
    { username: 1 },
    { unique: true }
);

// Sparse index
db.products.createIndex(
    { category: 1 },
    { sparse: true }
);
```

### Compound Indexes
```javascript
// Multiple fields
db.orders.createIndex(
    { userId: 1, orderDate: -1 }
);

// Text and regular fields
db.products.createIndex({
    name: "text",
    category: 1
});
```

### Geospatial Indexes
```javascript
// 2dsphere index
db.places.createIndex(
    { location: "2dsphere" }
);

// Query with geospatial operators
db.places.find({
    location: {
        $near: {
            $geometry: {
                type: "Point",
                coordinates: [-73.9667, 40.78]
            },
            $maxDistance: 5000
        }
    }
});
```

## Schema Design

### One-to-Many Relationships
```javascript
// Embedded Documents
{
    _id: ObjectId("..."),
    name: "John Doe",
    orders: [
        {
            orderId: ObjectId("..."),
            date: ISODate("2025-07-11"),
            items: [...]
        }
    ]
}

// References
{
    _id: ObjectId("..."),
    name: "John Doe",
    orderIds: [ObjectId("..."), ObjectId("...")]
}
```

### Many-to-Many Relationships
```javascript
// Intermediate Collection
{
    _id: ObjectId("..."),
    userId: ObjectId("..."),
    productId: ObjectId("..."),
    dateAdded: ISODate("2025-07-11")
}

// Array of References
{
    _id: ObjectId("..."),
    name: "Programming Course",
    students: [ObjectId("..."), ObjectId("...")]
}
```

## Performance Optimization

### Index Optimization
```javascript
// Covered Queries
db.users.find(
    { age: { $gt: 21 } },
    { _id: 0, name: 1, age: 1 }
).hint({ age: 1 });

// Compound Index Strategy
db.orders.createIndex({
    userId: 1,
    status: 1,
    orderDate: -1
});
```

### Query Optimization
```javascript
// Projection
db.products.find(
    { category: "electronics" },
    { name: 1, price: 1 }
);

// Limit and Skip
db.orders.find()
    .sort({ orderDate: -1 })
    .skip(20)
    .limit(10);

// Explain Plan
db.users.find({ age: { $gt: 21 } })
    .explain("executionStats");
```

## Transactions

### Multi-Document Transactions
```javascript
// Start transaction
const session = db.getMongo().startSession();
session.startTransaction();

try {
    // Multiple operations
    const orders = session.getDatabase("mydb").orders;
    const inventory = session.getDatabase("mydb").inventory;
    
    orders.insertOne({
        _id: ObjectId(),
        items: ["item1", "item2"]
    });
    
    inventory.updateMany(
        { _id: { $in: ["item1", "item2"] } },
        { $inc: { quantity: -1 } }
    );
    
    // Commit
    session.commitTransaction();
} catch (error) {
    // Rollback
    session.abortTransaction();
} finally {
    session.endSession();
}
```

## Security

### Authentication
```javascript
// Create user
db.createUser({
    user: "appUser",
    pwd: "securePassword",
    roles: [
        { role: "readWrite", db: "myapp" },
        { role: "read", db: "reporting" }
    ]
});

// Custom role
db.createRole({
    role: "orderProcessor",
    privileges: [
        {
            resource: { db: "myapp", collection: "orders" },
            actions: ["find", "update"]
        }
    ],
    roles: []
});
```

### Authorization
```javascript
// Collection-level access control
db.runCommand({
    createRole: "orderViewer",
    privileges: [
        {
            resource: { db: "myapp", collection: "orders" },
            actions: ["find"]
        }
    ],
    roles: []
});

// Grant role to user
db.grantRolesToUser(
    "appUser",
    ["orderViewer"]
);
```

## Monitoring and Maintenance

### Database Stats
```javascript
// Collection stats
db.orders.stats();

// Database stats
db.stats();

// Server status
db.serverStatus();
```

### Backup and Restore
```bash
# Full backup
mongodump --uri="mongodb://localhost:27017" --out=/backup

# Collection backup
mongodump --uri="mongodb://localhost:27017" \
    --collection=orders --db=myapp

# Restore
mongorestore --uri="mongodb://localhost:27017" \
    --dir=/backup
```

## Best Practices

1. Schema Design
   - Design for common queries
   - Balance between normalization and denormalization
   - Use embedding for "contains" relationships
   - Use references for large or frequently changing data

2. Indexing
   - Create indexes for frequently queried fields
   - Use compound indexes for multiple field queries
   - Avoid over-indexing
   - Monitor index usage

3. Query Optimization
   - Use appropriate projections
   - Limit results when possible
   - Use covered queries when possible
   - Avoid large skip values

4. Performance
   - Use appropriate write concern
   - Batch operations when possible
   - Monitor and analyze slow queries
   - Use appropriate connection pooling

