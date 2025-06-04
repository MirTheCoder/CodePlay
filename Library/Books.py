
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import json
import os
from flask_migrate import Migrate



from sqlalchemy.testing.util import conforms_partial_ordering

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
    pdf = db.Column(db.String(300))

    def __init__(self, title, author, year, serialNum, pdf):
        self.title = title
        self.author = author
        self.year = year
        self.serialNum = serialNum
        self.pdf = pdf

    def to_dict(self):
        return {
            "title": self.title.lower(),
            "author": self.author.lower(),
            "year": str(self.year),
            "serial": str(self.serialNum)
        }
    def send_pdf(self):
        return self.pdf

# This is database where we will keep the reviews for each book
class reviews(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(100000000000000000000000000000000))
    review = db.Column(db.Integer)
    reason = db.Column(db.String(100000000000000000000000000000000))
    name = db.Column(db.String(100000000000000000000000000000000))

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
    booker = books.query.all()
    return render_template("read.html", cart=booker)



@app.route("/rate")
def rate():
    #Here is how we will gather all the data from our books database model
    storage = books.query.all()
    #We will then import the books data into our rendering template to use for later
    return render_template("rate.html", cart = storage)



@app.route("/upload")
def upload():
    storage = books.query.all()
    return render_template("upload.html", cart=json.dumps([book.to_dict() for book in storage]))


@app.route("/addBook", methods=["POST"])
#This is the function we will use to take the users inputs and create a book
def addBook():
    #Here is where we ask for the data (which will be in the form of a dictionary) and then store the pieces of this data that we need
    #into variables so that we can make the book
    try:
        title = request.form['name']
        author = request.form['writer']
        year = int(request.form['year'])
        serial = int(request.form['serial'])
        pdf = request.files['pdf']
        file_name = pdf.filename
        pdfpath = os.path.join("static/books",file_name)
        pdf.save(pdfpath)
    #This is the book that we will create
        newBook = books(title,author, year, serial, pdfpath)
    #We will first add out new book and then commit it to our database
        db.session.add(newBook)
        db.session.commit()
        print("book has successfully been added")
    #We will return the title and the author back to our fetch method
        return jsonify({"title": title, "Writer": author})
    except Exception as e:
        print("Error in addBook: ", e)
        return jsonify({"title": "ERROR", "Writer": "ERROR"})



@app.route("/addReview", methods=["POST"])
def addReview():
    try:
    #Here is where we ask for the data (which will be in the form of a dictionary) and then store the pieces of this data that we need
    #into variables so that we can make the book
        data = request.json
        name = data.get('name')
        rating = int(data.get('rating'))
        text = data.get('text')
        title = data.get('title')
    #This is the book that we will create
        newReview = reviews(title,rating, text, name)
    #We will first add out new book and then commit it to our database
        db.session.add(newReview)
        db.session.commit()
        print("Review has successfully been added")
    #We will return the title and the author back to our fetch method
        return jsonify({"message": "Review has successfully been added"})
    except Exception as e:
        print("Error: ", e)



@app.route("/loadReviews", methods=["POST", "GET"])
def loadReviews():
    data = request.json
    name = data.get("title")
    #Use sessions to pass data from one app route to another
    session['review_title'] = name
    return jsonify({"message": "Navigating to review seeing page"})



@app.route("/seeReviews", methods=["POST", "GET"])
def seeReviews():
    title = session.get('review_title')
    if title:
        storage = reviews.query.filter_by(title=title).all()
        return render_template("seeReviews.html", cart=storage)
    else:
        return render_template("seeReviews.html")


@app.route("/viewBook", methods=['POST','GET'])
def viewBook():
    data = request.json
    word = data.get("title")
    session['book_title'] = word
    return jsonify({"message": "We are now going to navigate to the book for you to read"})



@app.route("/reader", methods=["POST","GET"])
def reader():
    title = session.get('book_title')
    if title:
        reading = books.query.filter_by(title=title).first()
        return render_template("reader.html", cart = reading.send_pdf() )

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)