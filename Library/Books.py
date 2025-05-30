from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy


app = Flask(__name__)
app.secret_key = "HASGGTYEIFGEG21356253725"
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

class books(db.Model):
    #Each row will be given a unique id, this is how we store data in the database view rows and columns
    _id = db.Column("id", db.Integer, primary_key=True)
    #These are the type of data that we are storing, but we give a limit of 100 to the amount columns that can be stored
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year = db.Column(db.Integer)
    serialNum = db.Column(db.Integer)
    #Used to define each person or ID within our database
    def __init__(self, title, author, year, serialNum):
        self.title = title
        self.author = author
        self.year = year
        self.serialNum = serialNum

class reviews(db.Model):
    #Each row will be given a unique id, this is how we store data in the database view rows and columns
    _id = db.Column("id", db.Integer, primary_key=True)
    #These are the type of data that we are storing, but we give a limit of 100 to the amount columns that can be stored
    title = db.Column(db.String(1000))
    review = db.Column(db.Integer)
    reason = db.Column(db.String(1000))
    name = db.Column(db.String(1000))
    #Used to define each person or ID within our database
    def __init__(self, title, review, reason, name):
        self.title = title
        self.review = review
        self.reason = reason
        self.name = name


@app.route("/")
def home():
    return render_template("home.html")
@app.route("/read")
def read():
    return render_template("read.html")
@app.route("/rate")
def rate():
    #We use this in order to gather all the data from the books database
    storage = books.query.all()
    #We pass all the values in the book database into the rendering
    return render_template("rate.html", cart = storage)



if __name__ == '__main__':
    #with app.app_context():
        #This will allow us to create our database template despite us not having any data within it
        #db.create_all()
    app.run(debug=True)