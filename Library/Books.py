from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

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
def addBook():
    data = request.json
    title = data.get('name')

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
    return render_template("upload.html")




if __name__ == '__main__':
    app.run(debug=True)