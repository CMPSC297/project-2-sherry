import os
import psycopg2
from sampleAPI import retrieveBook
from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgresql://localhost/sherryzhang")
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Register Button
@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # User did not provide a username and/or password
        if username == "" or password == "":
            return render_template("index.html", message="* Please enter required fields.")
        
        # Username already exists in database
        userDB = db.execute(text("SELECT * FROM users WHERE username = :username"), 
            {"username": username}).fetchone()
        if userDB:
            return render_template("index.html", message="* Username is already taken. Please select a different one.")
        
        # Creating new account
        db.execute(text("INSERT INTO users (username, password) VALUES (:username, :password)"), 
            {"username": username, "password": password})   
        db.commit()

        return render_template("login.html")

# LOGIN on Home Page that routes to Login Page
@app.route("/login", methods=["POST"])
def signin():
    if request.method == "POST":
        return render_template("login.html")

# Login Button
@app.route("/signin", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        userInfo = db.execute(text("SELECT * FROM users WHERE username = :username AND password = :password"), 
            {"username": username, "password": password}).fetchone()

        if userInfo:
            return render_template("search.html")
        
    return render_template("login.html", message = "* Username and/or password is incorrect")

# Logout
@app.route("/logout", methods=["POST"])
def logout():
    if request.method == "POST":
        return render_template("index.html")

# Search Button
@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        isbn = request.form["isbn"]
        title= request.form["title"]
        author = request.form["author"]
        if isbn == "" and title == "" and author == "":
            return render_template("search.html", message="* Please enter an ISBN number, book title, or author.")
        
        # Searching by ISBN
        elif isbn and title == "" and author == "":
            books = db.execute(text("SELECT * FROM books WHERE isbn = :isbn"), 
                {"isbn": isbn}).fetchall()
            if books: 
                return render_template("search.html", books=books)
            else:
                return render_template("search.html", message="No matches.")
        
        # Searching by Book Title
        elif title and isbn == "" and author == "":
            books = db.execute(text("SELECT * FROM books WHERE title = :title"), 
                {"title": title}).fetchall()
            if books: 
                return render_template("search.html", books=books)
            else:
                return render_template("search.html", message="No matches.")
        
        # Searching by Author
        elif author and isbn == "" and title == "":
            books = db.execute(text("SELECT * FROM books WHERE author = :author"), 
                {"author": author}).fetchall()
            if books: 
                return render_template("search.html", books=books)
            else:
                return render_template("search.html", message="No matches.")
        
        else:
            return render_template("search.html", message="* Please only fill out one field above")

# View Book Button
@app.route("/view", methods=["POST"])
def view():
    if request.method == "POST":
        isbn = request.form["book"] # Gives ISBN
        bookDetailDB = retrieveBook(isbn)     
        return render_template("book.html", message=bookDetailDB)

# @app.route("/review", methods=["POST"])
# def review():
#     if request.method == "POST":
#         isbn = request.form["reviewISBN"]
#         review = request.form["review"]
#         db.execute(text("INSERT INTO reviews (isbn, review) VALUES (:isbn, :review)"),
#             {"isbn": isbn, "review": review}) 
#         db.commit()
#         return render_template("index.html")

# # Writing Review
# @app.route("/review", methods=["POST"])
# def review():
#     if request.method == "POST":
#         user_id = session["user_id"]
#         book_id = request.form["book_id"]
#         rating = request.form["rating"]
#         text = request.form["text"]
        
#         # Check if the user has already submitted a review for this book
#         existing_review = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id", 
#                                      {"user_id": user_id, "book_id": book_id}).fetchone()
#         if existing_review:
#             return render_template("error.html", message="You have already submitted a review for this book.")
        
#         # Insert the new review into the database
#         db.execute("INSERT INTO reviews (user_id, book_id, rating, text) VALUES (:user_id, :book_id, :rating, :text)",
#                     {"user_id": user_id, "book_id": book_id, "rating": rating, "text": text})
#         db.commit()
        
#         #Dont know if review page exisits already

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8080)