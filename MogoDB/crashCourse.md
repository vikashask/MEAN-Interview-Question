
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
