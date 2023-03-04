import os
import psycopg2
from sampleAPI import retrieveBook, retrieveAverageRating, retrieveNumberOfRating
from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = '_23hd9udhf*HUHDF'
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# app.config['SECRET_KEY'] = 'hfouuwu9e8r9ui23jrojrlefl'
# Session(app)

# Set up database
engine = create_engine("postgresql://localhost/sherryzhang")
db = scoped_session(sessionmaker(bind=engine))

@app.route('/set_session')
def set_session(id):
    session['id'] = id

@app.route("/get_session")
def get_session():
    return session.get('id')

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
        # session['sessionUsername'] = username
        password = request.form["password"]
        
        userInfo = db.execute(text("SELECT * FROM users WHERE username = :username AND password = :password"), 
            {"username": username, "password": password}).fetchone()
        
        id = db.execute(text("SELECT id FROM users WHERE username = :username"), {"username": username}).fetchone()[0]
        print(id)
        set_session(id)

        if userInfo:
            return render_template("search.html")
        
    return render_template("login.html", message = "* Username and/or password is incorrect")

# Logout
@app.route("/logout", methods=["POST"])
def logout():
    if request.method == "POST":
        session.pop("id", None)
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
        title = db.execute(text("SELECT title FROM books WHERE isbn = :isbn"),
            {"isbn": isbn}).fetchone()[0]
        author = db.execute(text("SELECT author FROM books WHERE isbn = :isbn"),
            {"isbn": isbn}).fetchone()[0]
        year = db.execute(text("SELECT year FROM books WHERE isbn = :isbn"),
            {"isbn": isbn}).fetchone()[0]
        reviews = db.execute(text("SELECT review FROM reviews WHERE isbn = :isbn"),
            {"isbn": isbn}).fetchall()
        averageRating = retrieveAverageRating(isbn)
        numberOfRating = retrieveNumberOfRating(isbn)
        titleDisplay = f"Title: {title}"
        authorDisplay = f"Author: {author}"
        yearDisplay = f"Year: {year}" 
        return render_template("book.html", isbn=isbn, title=titleDisplay, author=authorDisplay, year=yearDisplay, averageRating=averageRating, numberOfRating=numberOfRating, reviews=reviews)

@app.route("/review", methods=["POST"])
def review():
    if request.method == "POST":
        id = get_session()
        # print(userid)
        isbn = request.form["isbn"]     
        # print(isbn)  
        review = request.form["review"]
        rating = request.form["rating"]

        # Check if user already has existing review for the book
        # print(rating)
        # print(isbn)

        existingReviewCheck = db.execute(text("SELECT review FROM reviews WHERE id = :id AND isbn = :isbn"),
            {"id": id, "isbn": isbn}).fetchone()
        if existingReviewCheck:
            error = "Unable to submit review as you have already reviewed this book"
            return render_template("error.html", error=error)

        else:

            # db.execute(text("INSERT INTO users (username, password) VALUES (:username, :password)"), 
            # {"username": username, "password": password})   
            # db.commit()

            db.execute(text("INSERT INTO reviews (id, isbn, rating, review) VALUES (:id, :isbn, :rating, :review)"),
            {"id": id, "isbn": isbn, "rating": rating, "review": review}) 
            db.commit()
            complete = "Your review has been submitted"
        return render_template("success.html", complete=complete)

# @app.route("/api/flights/<int:flight_id>")
@app.route("/api/<int:isbn>")
def apiInfo(isbn):
    check = db.execute(text("SELECT * FROM books WHERE isbn = :isbn"),
        {"isbn": str(isbn)}).fetchone()
    if check:
        info = retrieveBook(isbn)
        return render_template("api.html", info=info)
    else:
        error = "404 Error"
        return render_template("api.html", error=error)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8080)