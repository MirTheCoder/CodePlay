
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import json

app = Flask(__name__)
app.secret_key = "HASGGTYEIFGEG21356253725"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db.init_app(app)

# This is the database where we will keep all the books we make along with teh fields require for each book
class books(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year = db.Column(db.Integer)
    serialNum = db.Column(db.Integer)

    def __init__(self, title, author, year, serialNum):
        self.title = title
        self.author = author
        self.year = year
        self.serialNum = serialNum

    def to_dict(self):
        return {
            "title": self.title.lower(),
            "author": self.author.lower(),
            "year": str(self.year),
            "serial": str(self.serialNum)
        }

# This is database where we will keep the reviews for each book
class reviews(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    review = db.Column(db.Integer)
    reason = db.Column(db.String(1000))
    name = db.Column(db.String(1000))

    def __init__(self, title, review, reason, name):
        self.title = title
        self.review = review
        self.reason = reason
        self.name = name

#Here we have our various routes that we will call to access the templates that we need
@app.route("/")
def home():
    return render_template("home.html")
@app.route("/read")
def read():
    return render_template("read.html")
@app.route("/rate")
def rate():
    #Here is how we will gather all the data from our books database model
    storage = books.query.all()
    #We will then import the books data into our rendering template to use for later
    return render_template("rate.html", cart = storage)
@app.route("/upload")
def upload():
    storage = books.query.all()
    return render_template("upload.html", ccart=json.dumps([book.to_dict() for book in storage]))


@app.route("/addBook", methods=["POST"])
#This is the function we will use to take the users inputs and create a book
def addBook():
    #Here is where we ask for the data (which will be in the form of a dictionary) and then store the pieces of this data that we need
    #into variables so that we can make the book
        data = request.json
        title = data.get('name')
        author = data.get('writer')
        year = data.get('year')
        serial = data.get('serial')
    #This is the book that we will create
        newBook = books(title,author, year, serial)
    #We will first add out new book and then commit it to our database
        db.session.add(newBook)
        db.session.commit()
        print("book has successfully be added")
    #We will return the title and the author back to our fetch method
        return jsonify({"name": title, "writer": author})




if __name__ == '__main__':
    app.run(debug=True)