import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text

# Change database engine accordingly
engine = create_engine('postgresql://localhost/postgres')

db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute(text("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :destination, :duration)"),
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"{isbn}, {title}, {author}, {year} has been added")
        db.commit()
        
if __name__ == "__main__":
    main()