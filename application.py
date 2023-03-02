import os
import psycopg2
from flask import Flask, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgresql://localhost/dhitasrikanth")
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
        # Need if statement checking if username already exists in DB
        # check if username already exists
        user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
        if user:
            return render_template("error.html", message="Username already taken, please choose a different one.")

        # if username doesn't exist, add user to database
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": password})
        db.commit()
        if username == "" or password == "":
            return render_template("index.html", message="* Please enter required fields")
        return render_template("login.html")

# Login on Home Page
@app.route("/login", methods=["POST"])
def signin():
    if request.method == "POST":
        return render_template("login.html")

# Login Button
@app.route("/signin", methods=["POST"])
def login():
    if request.method == "POST":
        loginusername = request.form["loginusername"]
        loginpassword = request.form["loginpassword"]
        if loginusername == "" or loginpassword == "":
            return render_template("login.html", message="* Please enter your username and/or password correctly")
        # Need to check if username and password both match
        
        return render_template("search.html")

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
        bookTitle= request.form["bookTitle"]
        author = request.form["author"]
        if isbn == "" and bookTitle == "" and author == "":
            return render_template("search.html", message="* Please enter an ISBN number, book title, or author.")
        # Query the database for books matching the search criteria
        search_query = f"%{isbn}%"
        search_query_title = f"%{bookTitle}%"
        search_query_author = f"%{author}%"
        books = db.execute("SELECT * FROM books WHERE isbn LIKE :search_query OR title LIKE :search_query_title OR author LIKE :search_query_author",
                            {"search_query": search_query, "search_query_title": search_query_title, "search_query_author": search_query_author}).fetchall()

        # If no books are found, return an error message
        if len(books) == 0:
            return render_template("search.html", message="No books found matching that search criteria.")

        # Otherwise, display the list of books
        return render_template("search.html", books=books)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8080)