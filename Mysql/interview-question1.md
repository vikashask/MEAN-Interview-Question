Top Answers to MySQL Interview Questions

## 1. Compare MySQL Vs. SQL Server
Criteria	MySQL	SQL Server
Targeted towards -Internet servers & Open Source software -	Corporate & Enterprise market
Functionality	-Speed -	Administration, Graphical data modelling
Works with	- Assumes internet access	-Administration, Graphical data modelling

## 4. What are the features of MySQL?
MySQL provides cross-platform support, wide range of interfaces for application programming and has many stored procedures like triggers and cursors that helps in managing the database.
## 6. What is the default port for MySQL Server?
The default port for MySQL Server is 3306. Another standard default is port 1433 in TCP/IP for SQL Server.
## 7. What do DDL, DML, and DCL stand for?
DDL is the abbreviation for Data Definition Language dealing with database schemas as well as the description of how data resides in the database. An example is CREATE TABLE command. DML denotes Data Manipulation Language such as SELECT, INSERT etc. DCL stands for Data Control Language and includes commands like GRANT, REVOKE etc.
## 8. What are meant by Joins in MySQL?
In MySQL the Joins are used to query data from two or more tables. The query is made using relationship between certain columns existing in the table. There are four types of Joins in MySQL. Inner Join returns the rows if there is at least one match in both the tables. Left Join returns all the rows form the left table even if there is no match in the right table. Right Join returns all the rows from the right table even if no matches exist in left table. Full Join would return rows when there is at least one match in the tables.
## 9. What are the common MySQL functions?
Common MySQL functions are as follows: 
• NOWO – function for returning current date and time as single value.
• CURRDATEO – function for returning the current date or time. 
• CONCAT (X, Y) – function to concatenates two string values creating single string output. 
• DATEDIFF (X, Y) – function to determine difference two dates.

Become Master of MySQL by going through this MySQL training course.

## 10. What is the difference between CHAR and VARCHAR?
When the table is created, CHAR is used to define the fixed length of the table and columns. The length value could be in the range of 1-255. VARCHAR command is given to adjust the column and table length as required.

## 11. What are HEAP Tables?
Basically HEAP tables are in-memory and used for high speed temporary storages. But TEXT or BLOB fields are not allowed within them. They also do not support AUTO INCREMENT.

## 12. What is the syntax for concatenating tables in MySQL?
The syntax for concatenating tables is MySQL is CONCAT (string 1, string 2, string 3)

Download MySQL Interview Questions asked by top MNCs in 2018
GET PDF
## 13. What are the limits for using columns to create the Index?
The maximum limits of indexed columns that could be created for any table is 16.

## 14. What are the different types of strings in Database columns in MySQL?
Different types of strings that can be used for database columns are SET, BLOB, VARCHAR, TEX, ENUM, and CHAR.

## 16. Is there an object oriented version of MySQL library functions?
MySQLi is the object oriented version of MySQL and it interfaces in PHP.

## 17. What is the storage engine for MySQL?
Storage tables are named as table types. The data is stored in the files using multiple techniques such as indexing, locking levels, capabilities and functions.

## 18. What is the difference between primary key and candidate key?
Primary key in MySQL is use to identify every row of a table in unique manner. For one table there is only one primary key. One of the candidate keys is the primary key and the candidate keys can be used to reference the foreign keys.

## 19. What are the different types of tables in MySQL?
MyISAM is the default table that is based on the sequential access method.

HEAP is the table that is used for fast data access but data will be lost if the table or system crashes. 
InoDB is the table that supports transactions using the COMMIT and ROLL BACK commands.
BDB can support transactions similar to InoDB but the execution is slower.

## 20. Can you use MySQL with LINUX operating system?
Yes, the syntax for using MySQL with LINUX operating system is /etc/init.d/mysqlstart

## 21. What is the use of ENUM in MySQL?
Use of ENUM will limit the values that can go into a table. For instance; the user can create a table giving specific month values and other month values would not enter into the table.

## 22. What are the TRIGGERS that can be used in MySQL tables?
The following TRIGGERS are allowed in MySQL:• BEFORE INSERT

 AFTER INSERT
 BEFORE UPDATE
 AFTER UPDATE
 BEFORE DELETE
 AFTER DELETE

## 23. What is the difference between LIKE and REGEXP operators in MySQL?
 LIKE is denoted using the % sign. 
 For example:
 SELECT * FROM user WHERE user name LIKE “%NAME”.
 • On the other hand the use of REGEXP is as follows:
 SELECT * FROM user WHERE username REGEXP “^NAME”;

## 24. How to use the MySQL slow query log?
Information that is provided on the slow query log could be huge in size. The query could also be listed over thousand times. In order to summarize the slow query log in an informative manner one can use the third party tool “pt-qury-digest”.

## 25. How can one take incremental backup in MySQL?
User can take incremental backup in MySQL using percona xtrabackup.

## 26. How can you change the root password if the root password is lost?
In such cases when the password is lost the user should start the DB with – skip-grants-table and then change the password. Thereafter with the new password the user should restart the DB in normal mode.

## 27. How to resolve the problem of data disk that is full?
When the data disk is full and overloaded the way out is to create and soft link and move the .frm as well as the .idb files into that link location.

## 28. What is the difference between DELETE TABLE and TRUNCATE TABLE commands in MySQL?
Basically DELETE TABLE is logged operation and every row deleted is logged. Therefore the process is usually slow. TRUNCATE TABLE also deletes rows in a table but it will not log any of the rows deleted.  The process is faster in comparison. TRUNCATE TABLE can be rolled back and is functionally similar to the DELETE statement using no WHERE clause.

## 29. What are types of joins in MySQL?
There are four types of Joins in MySQL. 
    Inner Join returns the rows if there is at least one match in both the tables.
    Left Join returns all the rows form the left table even if there is no match in the right table. 
    Right Join returns all the rows from the right table even if no matches exist in left table. 
    Full Join would return rows when there is at least one match in the tables.

## 30.What are the storage models of OLAP?
The storage models in OLA are MOLAP, ROLAP, and HOLAP.

## 31. How to define testing of network layers in MySQL?
For this it is necessary reviewing the layered architecture and determining hardware and software configuration dependencies in respect of the application put to test.

## 32. What is the difference between primary key and unique key?
While both are used to enforce uniqueness of the column defined but primary key would create a clustered index whereas unique key would create non-clustered index on the column. Primary key does not allow ‘NULL’ but unique key allows it. 

## 33. What is meant by transaction and ACID properties?
Transaction is logical unit of work where either all or none of the steps should be performed. ACID is the abbreviation for Atomicity, Consistency, Isolation, and Durability that are properties of any transaction.

## 34. How can one restart SQL Server in single user or minimal configuration modes?
The command line SQLSERVER.EXE used with –m will restart SQL Server in single user mode and with –f will start it in minimal configuration mode.

## 35. What is the difference between BLOB and TEXT?
BLOBs are binary large object holding huge data. 4 types of BLOB are TINYBLOB, BLOB, MEDIBLOB, and LONGBLOB. TEXT is case-sensitive BLOB. 4 types of TEXT are TINY TEXT, TEXT, MEDIUMTEXT, and LONG TEXT.

## 36. What is the basic MySQL architecture?
The logical architecture of MySQL is made of ‘connection manager’, ‘query optimizer’, and ‘pluggable engines’.