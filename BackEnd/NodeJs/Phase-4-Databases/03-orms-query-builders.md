# ORMs & Query Builders

## Sequelize (SQL ORM)

```javascript
const { Sequelize, DataTypes } = require("sequelize");

// Initialize
const sequelize = new Sequelize("database", "user", "password", {
  host: "localhost",
  dialect: "mysql",
});

// Define model
const User = sequelize.define("User", {
  name: DataTypes.STRING,
  email: {
    type: DataTypes.STRING,
    unique: true,
    allowNull: false,
  },
  age: DataTypes.INTEGER,
});

// Sync with database
await sequelize.sync();

// CRUD
const user = await User.create({ name: "John", email: "john@example.com" });
const users = await User.findAll();
const user = await User.findByPk(1);
await user.update({ age: 30 });
await user.destroy();

// Relationships
const Post = sequelize.define("Post", {
  title: DataTypes.STRING,
  content: DataTypes.TEXT,
});

User.hasMany(Post);
Post.belongsTo(User);

// Query with relations
const user = await User.findByPk(1, { include: Post });
```

## Mongoose (MongoDB ODM)

```javascript
const mongoose = require("mongoose");

// Connect
await mongoose.connect("mongodb://localhost:27017/mydb");

// Define schema
const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, unique: true, required: true },
  age: { type: Number, min: 0 },
  tags: [String],
  createdAt: { type: Date, default: Date.now },
});

// Create model
const User = mongoose.model("User", userSchema);

// CRUD
const user = await User.create({ name: "John", email: "john@example.com" });
const users = await User.find();
const user = await User.findById(id);
await User.updateOne({ _id: id }, { age: 30 });
await User.deleteOne({ _id: id });

// Relationships
const postSchema = new mongoose.Schema({
  title: String,
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
});

const Post = mongoose.model("Post", postSchema);

// Populate relations
const user = await User.findById(id).populate("posts");
```

## TypeORM

```javascript
import {
  createConnection,
  Entity,
  PrimaryGeneratedColumn,
  Column,
} from "typeorm";

// Initialize
const connection = await createConnection({
  type: "mysql",
  host: "localhost",
  username: "root",
  password: "password",
  database: "mydb",
  entities: [User, Post],
  synchronize: true,
});

// Define entity
@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column({ unique: true })
  email: string;

  @Column({ nullable: true })
  age: number;
}

// Repository pattern
const userRepository = connection.getRepository(User);

const user = await userRepository.create({ name: "John" });
await userRepository.save(user);

const users = await userRepository.find();
const user = await userRepository.findOne(id);
await userRepository.update(id, { age: 30 });
await userRepository.delete(id);
```

## Query Builders

```javascript
// Sequelize query builder
const users = await User.findAll({
  where: { age: { [Op.gte]: 18 } },
  order: [["createdAt", "DESC"]],
  limit: 10,
  offset: 0,
});

// Mongoose query builder
const users = await User.find({ age: { $gte: 18 } })
  .sort({ createdAt: -1 })
  .limit(10)
  .skip(0);

// TypeORM query builder
const users = await connection
  .createQueryBuilder(User, "user")
  .where("user.age >= :age", { age: 18 })
  .orderBy("user.createdAt", "DESC")
  .limit(10)
  .offset(0)
  .getMany();

// Knex.js (query builder)
const users = await knex("users")
  .where("age", ">=", 18)
  .orderBy("created_at", "desc")
  .limit(10);
```

## Migrations

```javascript
// Sequelize migration
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable("Users", {
      id: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        autoIncrement: true,
      },
      name: Sequelize.STRING,
      email: Sequelize.STRING,
    });
  },
  down: async (queryInterface) => {
    await queryInterface.dropTable("Users");
  },
};

// Run migrations
// npx sequelize-cli db:migrate

// Mongoose doesn't have migrations (schema-less)
// Use version control and manual updates

// TypeORM migrations
import { MigrationInterface, QueryRunner, Table } from "typeorm";

export class CreateUserTable1234567890 implements MigrationInterface {
  async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.createTable(
      new Table({
        name: "users",
        columns: [
          { name: "id", type: "int", isPrimary: true },
          { name: "name", type: "varchar" },
        ],
      })
    );
  }

  async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropTable("users");
  }
}
```

## Performance Tips

```javascript
// Use indexes
userSchema.index({ email: 1 });
userSchema.index({ age: 1, status: 1 });

// Lazy load relations
const user = await User.findById(id);
const posts = await user.getPosts(); // Load on demand

// Batch operations
const users = await User.bulkCreate([user1, user2, user3]);

// Pagination
const page = 1;
const limit = 10;
const users = await User.find()
  .skip((page - 1) * limit)
  .limit(limit);

// Select specific fields
const users = await User.find({}, { name: 1, email: 1 });

// Use aggregation for complex queries
const stats = await User.aggregate([
  { $group: { _id: "$status", count: { $sum: 1 } } },
]);
```
