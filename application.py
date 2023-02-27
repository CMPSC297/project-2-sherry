from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = "dev"

if ENV == "def":
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456@localhost/registration"
else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = ""

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "" or password == "":
            return render_template("index.html", message="* Please enter required fields")
        return render_template("registration.html")


if __name__ == "__main__":
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