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
app.secret_key = '_23hd9udhf*HUHDF'
# app.config['SECRET_KEY'] = 'hfouuwu9e8r9ui23jrojrlefl'
# Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# app.config['SECRET_KEY'] = 'hfouuwu9e8r9ui23jrojrlefl'
# Session(app)

# Set up database
engine = create_engine("postgresql://localhost/sherryzhang")
db = scoped_session(sessionmaker(bind=engine))

# app = Flask(__name__)

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
        session['sessionUsername'] = username
        password = request.form["password"]
        
        userInfo = db.execute(text("SELECT * FROM users WHERE username = :username AND password = :password"), 
            {"username": username, "password": password}).fetchone()
        
        # id = db.execute(text("SELECT id FROM users WHERE username = :username"), {"username": username}).fetchone()
        # session['userSessionID'] = id

        if userInfo:
            return render_template("search.html")
        
    return render_template("login.html", message = "* Username and/or password is incorrect")

# Logout
@app.route("/logout", methods=["POST"])
def logout():
    if request.method == "POST":
        session.pop("sessionUsername", None)
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
            books = db.execute(text("SELECT * FROM books WHERE isbn LIKE :isbn"), 
                {"isbn": isbn+"%"}).fetchall()
            if books: 
                return render_template("search.html", books=books)
            else:
                return render_template("search.html", message="No matches.")
        
        # Searching by Book Title
        elif title and isbn == "" and author == "":
            books = db.execute(text("SELECT * FROM books WHERE title LIKE :title"), 
                {"title": title+"%"}).fetchall()
            if books: 
                return render_template("search.html", books=books)
            else:
                return render_template("search.html", message="No matches.")
        
        # Searching by Author
        elif author and isbn == "" and title == "":
            books = db.execute(text("SELECT * FROM books WHERE author LIKE :author"), 
                {"author": author+"%"}).fetchall()
            if books: 
                return render_template("search.html", books=books)
            else:
                return render_template("search.html", message="No matches.")
        
        else:
            return render_template("search.html", message="* Please only fill out one field above")

# Return to Search
@app.route("/returnToSearch", methods=["POST"])
def returntoSearch():
    if request.method == "POST":
        return render_template("search.html")

# View Book Button
@app.route("/view", methods=["POST"])
def view():
    if request.method == "POST":
        isbn = request.form["book"] # Gives ISBN
        session["isbn"] = isbn
        title = db.execute(text("SELECT title FROM books WHERE isbn = :isbn"),
            {"isbn": isbn}).fetchone()
        author = db.execute(text("SELECT author FROM books WHERE isbn = :isbn"),
            {"isbn": isbn}).fetchone()
        year = db.execute(text("SELECT year FROM books WHERE isbn = :isbn"),
            {"isbn": isbn}).fetchone()
        reviews = db.execute(text("SELECT review FROM reviews WHERE isbn = :isbn"),
            {"isbn": isbn}).fetchall()
        message = f"ISBN: {isbn}, \nTitle: {title} \nAuthor: {author} \nYear: {year}"
        # bookDetailDB = retrieveBook(isbn)     
        return render_template("book.html", message=message, reviews=reviews)

@app.route("/review", methods=["POST"])
def review():
    if request.method == "POST":
        if "sessionUsername" and "isbn" in session:
            username = session["sessionUsername"]
            isbn = session["isbn"]       
            review = request.form["review"]
            rating = request.form["rating"]

            # Check if user already has existing review for the book
            existingReviewCheck = db.execute(text("SELECT review FROM reviews WHERE isbn = :isbn AND username = :username"),
                {"isbn": isbn, "username": username})
            if existingReviewCheck:
                error = "Unable to submit review as you have already reviewed this book"
                return render_template("error.html", error=error)

            else:
                db.execute(text("INSERT INTO reviews (username, isbn, rating, review) VALUES (:username, :isbn, :rating, :review)"),
                {"username": username, "isbn": isbn, "rating": rating, "review": review}) 
                db.commit()
                complete = "Your review has been submitted"
                return render_template("success.html", complete=complete)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8080)