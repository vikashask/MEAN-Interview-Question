
##
use DATABASE_NAME

## selected database, use the command db

db

show dbs

## drop database
db.dropDatabase()

## create collection
db.createCollection(name, options)
db.createCollection(‘tutorialspoint’)

## collection
show collections

## Insert
db.movie.insert({"name":"tutorials point"})

db.tutorialspoint.insert({"name" : "tutorialspoint"})
>db.COLLECTION_NAME.insert(document)


db.post.insert([
   {
      title: 'MongoDB Overview', 
      description: 'MongoDB is no sql database',
      by: 'tutorials point',
      url: 'http://www.tutorialspoint.com',
      tags: ['mongodb', 'database', 'NoSQL'],
      likes: 100
   },
   {
      title: 'NoSQL Database', 
      description: "NoSQL database doesn't have tables",
      by: 'tutorials point',
      url: 'http://www.tutorialspoint.com',
      tags: ['mongodb', 'database', 'NoSQL'],
      likes: 20, 
      comments: [	
         {
            user:'user1',
            message: 'My first comment',
            dateCreated: new Date(2013,11,10,2,35),
            like: 0 
         }
      ]
   }
])

## drop collection
db.COLLECTION_NAME.drop()

db.COLLECTION_NAME.find()

db.mycol.find().pretty()

=====================
## Equality
db.mycol.find({"by":"tutorials point"}).pretty()

## Less Than
 db.mycol.find({"likes":{$lt:50}}).pretty()

## Greater Than
db.mycol.find({"likes":{$gt:50}}).pretty()

## Greater Than Equals
db.mycol.find({"likes":{$gte:50}}).pretty()

## Not Equals 
db.mycol.find({"likes":{$ne:50}}).pretty()

## AND in MongoDB
db.mycol.find(
   {
      $and: [
         {key1: value1}, {key2:value2}
      ]
   }
).pretty()

## Find
db.mycol.find({$and:[{"by":"tutorials point"},{"title": "MongoDB Overview"}]}).pretty() {

db.COLLECTION_NAME.remove(DELLETION_CRITTERIA)

## remove only one
>db.COLLECTION_NAME.remove(DELETION_CRITERIA,1)
## remove all documents
>db.mycol.remove()

## MongoDB - Projection

## The find() Method

db.COLLECTION_NAME.find({},{KEY:1})

db.mycol.find({},{"title":1,_id:0})



