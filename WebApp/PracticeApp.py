

from flask import Flask, redirect, url_for,render_template, request, session
from flask import flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os
import sqlalchemy
app = Flask(__name__)
app.secret_key = "QETYUIPKHGDAVXBM10928374"
#We use this in order to have the user once logged in, have their session logged in for 13 minutes, this means that
#for 13 minutes they will be logged in already or auto logged in
app.permanent_session_lifetime = timedelta(minutes = 20)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

#Here is our database where we will store the image of each user
class users(db.Model):
    #Each row will be given a unique id, this is how we store data in the database view rows and columns
    _id = db.Column("id", db.Integer, primary_key=True)
    #These are the type of data that we are storing, but we give a limit of 100 to the amount columns that can be stored
    uname = db.Column(db.String(100), nullable=True, default=None)
    email = db.Column(db.String(100), nullable=True, default=None)
    age = db.Column(db.Integer, nullable=True, default=None)
    pswd = db.Column(db.String(1000), nullable=True, default=None)
    image = db.Column(db.Text, nullable=True, default=None)
    education1 = db.Column(db.String(2000) , nullable=True, default=None)
    education2 = db.Column(db.String(2000), nullable=True, default=None)
    education3 = db.Column(db.String(2000), nullable=True, default=None)
    activity1 = db.Column(db.String(2000), nullable=True, default=None)
    activity2 = db.Column(db.String(2000), nullable=True, default=None)
    activity3 = db.Column(db.String(2000), nullable=True, default=None)
    phone = db.Column(db.Integer, nullable=True, default=None)
    birth = db.Column(db.String(1000), nullable=True, default=None)
    address = db.Column(db.String(1000), nullable=True, default=None)
    bio = db.Column(db.Text, nullable=True, default=None)
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
        #The session timer starts
        session.permanent = True
        #Here we will retrieve the username and password input by the user in the sign-in form if their session has expired,
        #and they have to do a post request or fill out a form to get in
        user = request.form["nm"]
        word = request.form["ps"]
        #session["user"] = user
        found_user = users.query.filter_by(uname=user, pswd=word).first()
        if found_user:
            #If the username and password are found within the user database, then we will give the user access to the user page
            valid = False
            session["user"] = found_user.uname
            session["password"] = found_user.pswd
            return redirect(url_for("user"))
        else:
            #if not true that both the username and password are found in the database, then we will
            #tell the suer to either try again or make an account
            valid = True
            return render_template("login.html", one = valid, two = text)
    else:
        #If the user is already in session, then the application will let them know that they are already logged in
        if "user" in session:
            valid = False
            same = session["user"]
            flash(f"Hey {same}, You are already logged in", "info")
            return redirect(url_for("user"))

        return render_template("login.html", one = valid, two = text)


@app.route("/user", methods=["POST", "GET"])
def user():
    #If the user is able to log in and the session starts, then the user will be notified that it was a success
    if "user" in session:
        user = session["user"]
        flash("Login successful", "info")
        #In the user page, the user can add their email, and it will be saved within the database for their specific user
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            #Message to notify the user that the email was successfully saved
            flash("Email was saved!")
            flash(f"Email: {email}")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", text = user, email = email)
    else:
        #If the user is not in session and has been logged out, then they will be denied the chance to access users and
        #will be returned to the login page to start up their session or create a new account
        flash("You are not logged in", "info")
        return redirect(url_for("login"))
@app.route("/details")
def details():
    #Here we check to see if the user is in session
    if "user" in session:
        username = session["user"]
        found_user = users.query.filter_by(uname = username).first()
        #If the user data is found in the database, then we will collect all teh users information to display
        if found_user:
            age = found_user.age
            picture = found_user.image
            mail = found_user.email
            phone = found_user.phone
            brith = found_user.birth
            address = found_user.address
            bio = found_user.bio
            education1 = found_user.education1
            education2 = found_user.education2
            education3 = found_user.education3
            activity1 = found_user.activity1
            activity2 = found_user.activity2
            activity3 = found_user.activity3
    else:
        #this will only pop up if the user is not logged in and tries to access the details page
        flash("You are not logged in","info")
        #if the user is not logged in, then we will redirect the user to the login page
        return redirect(url_for("login"))
        #We pass the information into the details page to display the users details
    return render_template("details.html", photo = picture, email = mail, num = age, user = username,
                           phone = phone, brith = brith, address = address, bio = bio, education1 = education1
                           , education2 = education2, education3 = education3, activity1 = activity1,
            activity2 = activity2, activity3 = activity3)
@app.route("/create",methods = ["POST", "GET"])
#This is used to help create a new user within the database
def create():
    #This allows the user to create an account and have all their details stored within the session
    #basically, their data will be saved in the session
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        found_user = users.query.filter_by(uname=user).first()
        word = request.form["ps"]
        found_pswd = users.query.filter_by(uname=word).first()
        email = request.form["em"]
        found_email = users.query.filter_by(uname=email).first()

        if found_user:
            flash("Username has already been taken","info")
        elif found_pswd:
            flash("Username has already been taken", "info")
        elif found_email:
            flash("Username has already been taken", "info")
        else:
            age = request.form["ag"]
            pic = request.files["png"]
            session["user"] = user
            session["word"] = word
            session["email"] = email
            session["age"] = age
            picture = os.path.join("static", "profilePic")
            pic.save(picture)
            session["image"] = picture
            usr = users(user, email, age, word, picture)
            #add the new account to the database
            db.session.add(usr)
            db.session.commit()
            #Sends the new user to the user page
            return redirect(url_for("user"))
    #Will return the user to the create template if they do not submit a post request
    return render_template("create.html")
    # found_user = users.query.filter_by(name = user).first()
@app.route("/logout")
def logout():
    #Will only execute if the user is already in session
    if "user" in session:
        user = session["user"]
        flash(f"You have been successfully logged out {user}!", "info")
    #This will cancel the session of the user and also remove any saved information under the user in that session as
    #well
    session.pop("user", None)
    session.pop("email", None)
    #Returns the user back to the login page
    return redirect(url_for("login"))
@app.route("/edit", methods = ["POST", "GET"])
#This method allows the user to edit their information that shows up on their details page or profile page
def edit():
    #Checks to see if the user is in session or logged in
    if "user" in session:
        #Checks to see if the method or the route is receiving a post request
        if request.method == "POST":
            #This is where we locate the user in our database and update all the attributes of the users profile
            #they have edited so that we can then save them as their new information
            #We will also just use the user database info if the user does not edit their information with the edit page
            username = session["user"]
            found_user = users.query.filter_by(uname=username).first()
            image = request.files["image"]
            if image:
                path = found_user.image
                image.save("path")
            else:
                image = found_user.image
            email = request.form["email"]
            if email:
                session["email"] = email
                found_user.email = email
            else:
                email = found_user.email
            phone = request.form["phone"]
            if phone:
                session["phone"] = phone
                found_user.phone = phone
            else:
                phone = found_user.phone
            education1 = request.form["active1"]
            education2 = request.form["active2"]
            education3 = request.form["active3"]
            if education1:
                session["edu1"] = education1
                found_user.education1 = education1
            else:
                education1 = found_user.education1
            if education2:
                session["edu2"] = education2
                found_user.education2 = education2
            else:
                education2 = found_user.education2
            if education3:
                session["edu3"] = education3
                found_user.education3 = education3
            else:
                education3 = found_user.education3
            bio = request.form["bio"]
            if bio:
                session["bio"] = bio
                found_user.bio = bio
            else:
                bio = found_user.bio

            activity1 = request.form["hobby1"]
            activity2 = request.form["hobby2"]
            activity3 = request.form["hobby3"]
            if activity1:
                session["activity1"] = activity1
                found_user.activity1 = activity1
            else:
                activity1 = found_user.activity1
            if activity2:
                session["activity2"] = activity2
                found_user.activity2 = activity2
            else:
                activity2 = found_user.activity2
            if activity3:
                session["activity3"] = activity3
                found_user.activity3 = activity3
            else:
                activity3 = found_user.activity3
            age = request.form["age"]
            if age:
                session["age"] = age
                found_user.age = age
            else:
                age = found_user.age
            address = request.form["address"]
            if address:
                session["address"] = address
                found_user.address = address
            else:
                address = found_user.address
            birth = request.form["birth"]
            if birth:
                session["birth"] = birth
                found_user.birth = birth
            else:
                birth = found_user.birth

            #We commit the changes once we have finished editing the users databse
            db.session.commit()

            # In the render template we will pass all the data of the user into the edit template as context so that it
            # can show on the edit page
            return render_template("edit.html", pic=image, email=email, phone=phone, bio=bio,
            education1=education1, education2=education2, education3=education3, activity1=activity1,
            activity2=activity2, activity3=activity3, age=age, address=address, birth=birth)
        else:
            #If it is not a post request, then we will just upload current data of the user into the edit page
            #So that the user can see what their data currently is
            username = session["user"]
            #We first have to locate the specific users database
            found_user = users.query.filter_by(uname=username).first()
            image = found_user.image
            email = found_user.email
            phone = found_user.phone
            bio = found_user.bio
            education1 = found_user.education1
            education2 = found_user.education2
            education3 = found_user.education3
            activity1 = found_user.activity1
            activity2 = found_user.activity2
            activity3 = found_user.activity3
            age = found_user.age
            address = found_user.address
            birth = found_user.birth
            #In the render template we will pass all the data of the user into the edit template as context so that it
            #can show on the edit page
            return render_template("edit.html", pic = image, email = email, phone = phone, bio = bio,
            education1 = education1, education2 = education2, education3 = education3, activity1 = activity1,
            activity2 = activity2, activity3 = activity3, age = age, address = address, birth = birth)
    else:
        log = True
        #This will show if the user is not logged in
        return render_template("edit.html", log = log)



if __name__ == "__main__":
    with app.app_context():
        # Creates the database when the python file is run
        db.create_all()
    app.run(debug = True)