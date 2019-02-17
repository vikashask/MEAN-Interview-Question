## postgresql terminal common commands

PostgreSQL
    pgAdmin tool to management Tools for PostgreSQL
    
    For window you can press window key then search pgAdmin then enter
    Below are the link for postgreSQL ui 

    http://127.0.0.1:50961/browser/ 

    stop the postgresql service = brew services start postgresql
    start the postgresql service = brew services stop postgresql.

> \q | Exit psql connection

> \c | Connect to a new database

> \dt | List all tables

> \du | List all roles

> \list | List databases> 

> \conninfo connection information

>CREATE ROLE me WITH LOGIN PASSWORD 'password';
    
>CREATE DATABASE api;
    
>\list
    
    switch to new database
>\c api 

    CREATE TABLE users (
    ID SERIAL PRIMARY KEY,
    name VARCHAR(30),
    email VARCHAR(30)
    );

    INSERT INTO users (name, email) VALUES ('vik', 'vik@gmail.com'), ('jay', 'jay@gmail.com');

    SELECT * FROM users;