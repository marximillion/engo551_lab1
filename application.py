# postgresql://postgres:23081201@localhost/engo551_lab1
# import requests
import os
import csv

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
Session(app)



@app.route("/")
def main():
    db.create_all()
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, name, author, year in reader:
        book = Books(isbn=isbn, name=name, author=author,
                        year=year)
    db.session.add(book)
    db.session.commit()
    return render_template("index.html") 

@app.route("/register")
def register():
    return render_template("register.html")

#@app.route("/login")
#def register():
#	if session.get("username") is not None:
#		return render_template("home.html", username = session.get("username"))
#	return render_template("login.html")

@app.route("/success", methods=["POST"])
def success():
    username = request.form.get("username")
    password = request.form.get("password")
    user = Users(username=username, password=password)
    #user_exists = Users.query(username)
    #if user_exists == username:
    #    print(f"username: {username}")
    #    return render_template("error.html")
    db.session.add(user)
    db.session.commit()
    return render_template("success.html", username=user.username)

@app.route("/error", methods=["POST"])
def error():
    return render_template("error.html")

@app.route("/login")
def login():
    return render_template("login.html")

"""
@app.route("/home", methods=["POST"])
def home(user):
    username = request.form.get("username")
    password = request.form.get("password")
    user = Users.query.get(username)
    if user is None:
        return render_template("error.html", user=username, message="does not exist")
    #user_exists = Users.query(username)
    #if user_exists == username:
    #    print(f"username: {username}")
    #    return render_template("error.html")
    db.session.add(user)
    db.session.commit()
    return render_template("home.html")
"""

if __name__ == '__main__':
    with application.app_context():
        main()


































@app.route("/names")
def names():
    names = ["Alice", "Bob", "Combucha", "Donday"]
    return render_template("names.html", names=names)

@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name")
    return render_template("hello.html", name=name)
