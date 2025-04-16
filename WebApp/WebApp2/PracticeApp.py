from flask import Flask, redirect, url_for,render_template, request, session
from flask import flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
app = Flask(__name__)
app.secret_key = "QETYUIPKHGDAVXBM10928374"
app.permanent_session_lifetime = timedelta(minutes = 13)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


class users(db.Model):
    #Each row will be given a unique id, this is how we store data in the database view rows and columns
    _id = db.Column("id", db.Integer, primary_key=True)
    #These are the type of data that we are storing, but we give a limit of 100 to the amount columns that can be stored
    uname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    age = db.Column(db.Integer)
    pswd = db.Column(db.String(100))
    image_file = db.Column(db.String(200), default="default.jpg")
    #Used to define each person or ID within our database
    def __init__(self, uname, email, age, pswd, image):
        self.uname = uname
        self.email = email
        self.age = age
        self.pswd = pswd
        self.image = image


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods = ["POST", "GET"])
def login():
    valid = False
    text = "This account does not exist, please enter a valid account or create and account"
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        word = request.form["ps"]
        #session["user"] = user
        found_user = users.query.filter_by(uname = user).first()
        found_pswd = users.query.filter_by(pswd = word).first()
        if found_user and found_pswd:
            valid = False
            session["user"] = found_user.uname
            session["password"] = found_user.pswd
            return redirect(url_for("user"))
        else:
            valid = True
            return render_template("login.html", one = valid, two = text)
    else:
        if "user" in session:
            valid = False
            same = session["user"]
            flash(f"Hey {same}, You are already logged in", "info")
            return redirect(url_for("user"))

        return render_template("login.html", one = valid, two = text)


@app.route("/user", methods=["POST", "GET"])
def user():
    if "user" in session:
        user = session["user"]
        flash("Login successful", "info")
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!")
            flash(f"Email: {email}")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", text = user,)
    else:
        flash("You are not logged in", "info")
        return redirect(url_for("login"))
@app.route("/details")
def details():
    if "user" in session:
        hold = session["image"]
    return render_template("details.html", )
@app.route("/create",methods = ["POST", "GET"])
def create():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        word = request.form["ps"]
        email = request.form["em"]
        age = request.form["ag"]
        image = request.form["png"]
        usr = users(user, email,age,word)
        session["user"] = user
        session["word"] = word
        session["email"] = email
        session["age"] = age
        session["image"] = image
        db.session.add(usr)
        db.session.commit()
        return redirect(url_for("user"))
    return render_template("create.html")
    # found_user = users.query.filter_by(name = user).first()
@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been successfully logged out {user}!", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))
if __name__ == "__main__":
    with app.app_context():
        # Creates the database when the python file is run
        db.create_all()
    app.run(debug = True)