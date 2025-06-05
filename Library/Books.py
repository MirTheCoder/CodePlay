
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
    #This will bring us to our starting page or home template
    return render_template("home.html")



@app.route("/read")
#This will bring the user to a place where they can select from the options of books within
#our library
def read():
    #This is used to get all the books within the library so that we can send it over
    #To the read template
    booker = books.query.all()
    return render_template("read.html", cart=booker)


#This will take us to the page that will allow us to rate the books
@app.route("/rate")
def rate():
    #Here is how we will gather all the data from our books database model
    storage = books.query.all()
    #We will then import the books data into our rendering template to use for later
    return render_template("rate.html", cart = storage)


#This will take the user to a page where they can upload a new book to the library and
#add it to the database
@app.route("/upload")
def upload():
    #Collects all the books in our library currently in order to actually read the book
    storage = books.query.all()
    return render_template("upload.html", cart=json.dumps([book.to_dict() for book in storage]))

#This will take the user inputs from upload and use them in order to create an instance
#of the book class in order to add it to the library database
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


#This will take the rating info that user input from the rate page and create an instance of
#rate with it
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


#This method will load the reviews that people have written about different books, dependent on which book the user
@app.route("/loadReviews", methods=["POST", "GET"])
def loadReviews():
    #Here we ask for the user data via json in order to receive the title of the book that they
    #want to see the reviews of
    data = request.json
    #This is where we will store the name of the book that the user wants to review
    name = data.get("title")
    #Use sessions to pass data from one app route to another
    session['review_title'] = name
    #What we return to the HTML template or the fetch command
    return jsonify({"message": "Navigating to review seeing page"})


#This method will be used to send over to the HTML the reviews that people have written on
#book of interest
@app.route("/seeReviews", methods=["POST", "GET"])
def seeReviews():
    #We will retrieve the title of the book from session
    title = session.get('review_title')
    #Check to see if the title has a value in it
    if title:
        #Used to collect all the reviews on the specified title
        storage = reviews.query.filter_by(title=title).all()
        #Return the list of reviews to the template in order to display all the reviews for
        #that book
        return render_template("seeReviews.html", cart=storage)
    else:
        #renders just the template if title has no value in it
        return render_template("seeReviews.html")

#This will take the title of the book the user wants to read and store it in a session
#key value
@app.route("/viewBook", methods=['POST','GET'])
def viewBook():
    #Used to get the title of the book that the user selected and bring it to the backend
    data = request.json
    word = data.get("title")
    #Stores the title in session "book_title"
    session['book_title'] = word
    #What we return back to the fetch command
    return jsonify({"message": "We are now going to navigate to the book for you to read"})


#Used to send the correct path to the pdf or book that the user would like to read in order
#for them to view it
@app.route("/reader", methods=["POST","GET"])
def reader():
    #This will get the title and see if the title actually has a value stored inside it
    title = session.get('book_title')
    if title:
        #If it does, then we will get the first occurrence of the book title
        reading = books.query.filter_by(title=title).first()
        #We will call on the .send_pdf() attribute to get the pdf path of the book and
        #send it to the users end
        return render_template("reader.html", cart = reading.send_pdf() )
#Used to create the database if it is empty and not made yet
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)