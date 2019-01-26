
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
