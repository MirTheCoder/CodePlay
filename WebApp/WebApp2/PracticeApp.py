from flask import Flask, redirect, url_for,render_template, request, session
from flask import flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
app = Flask(__name__)
app.secret_key = "QETYUIPKHGDAVXBM10928374"
app.permanent_session_lifetime = timedelta(minutes = 13)
app.config['SQLALCHEMY_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class users(db.Model):
    #Each row will be given a unique id, this is how we store data in the database view rows and columns
    _id = db.Column("id", db.Integer, primary_key=True)
    #These are the type of data that we are storing, but we give a limit of 100 to the amount columns that can be stored
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    #Used to define each person or ID within our database
    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        found_user = user.query.filter_by(name = user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.commit()
        return redirect(url_for("user"))
    else:
        if "user" in session:
            same = session["user"]
            flash(f"Hey {same}, You are already logged in", "info")
            return redirect(url_for("user"))
        return render_template("login.html")
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
            db.commit()
            flash("Email was saved!")
            flash(f"Email: {email}")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", text = user,)
    else:
        flash("You are not logged in", "info")
        return redirect(url_for("login"))
#@app.route("/details")
#def details():
    #if "user" in session:

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been successfully logged out {user}!", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))
if __name__ == "__main__":
    #Creates the database when the python file is run
    db.create_all()
    app.run(debug = True)