CREATE TABLE BOOKS (
    isbn VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year VARCHAR NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE,
    password VARCHAR NOT NULL
);

CREATE TABLE reviews (
    reviewID SERIAL PRIMARY KEY,
    username VARCHAR,
    isbn VARCHAR,
    rating INTEGER NOT NULL,
    review VARCHAR UNIQUE,
    FOREIGN KEY (username) REFERENCES users(username),
    FOREIGN KEY (isbn) REFERENCES books(isbn)
);
