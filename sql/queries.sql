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
    user VARCHAR,
    isbn VARCHAR,
    rating INTEGER NOT NULL,
    review VARCHAR UNIQUE
);

-- CREATE TABLE reviews (
--     id SERIAL PRIMARY KEY,
--     book_isbn VARCHAR(13) REFERENCES books(isbn) ON DELETE CASCADE,
--     user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
--     rating INTEGER NOT NULL,
--     text VARCHAR(1000),
--     UNIQUE (book_isbn, user_id)
-- );

