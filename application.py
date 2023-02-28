from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ENV = "dev"

# if ENV == "dev":
#     app.debug = True
#     app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456@localhost/postgres"
# else:
#     app.debug = False
#     app.config["SQLALCHEMY_DATABASE_URI"] = ""

# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)

# class Feedback(db.Model):
#     __tablename__ = "feedback"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(200), unique=True)
#     password = db.Column(db.String(200))

#     def __init__(self, username, password):
#         self.username = username
#         self.password = password


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


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8080)

# import os

# from flask import Flask, session
# from flask_session import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

# app = Flask(__name__)

# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# # Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# # Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))


# @app.route("/")
# def index():
#     return "Project 2: TODO"

# if __name__ == "__main__":
#     app.run(debug=True)