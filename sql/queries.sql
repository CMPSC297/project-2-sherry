CREATE TABLE books (
    isbn INTEGER PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE info (
    username VARCHAR PRIMARY KEY,
    password VARCHAR NOT NULL
);

