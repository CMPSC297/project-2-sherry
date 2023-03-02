CREATE TABLE BOOKS (
    isbn INTEGER PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE info (
    username VARCHAR PRIMARY KEY,
    password VARCHAR NOT NULL
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    book_isbn VARCHAR(13) REFERENCES books(isbn) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL,
    text VARCHAR(1000),
    UNIQUE (book_isbn, user_id)
);

