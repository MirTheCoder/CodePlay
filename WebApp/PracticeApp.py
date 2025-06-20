
from flask import Flask, redirect, url_for,render_template, request, session, jsonify
from flask import flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os
import json
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

#Here is our database where we will store the data for each user
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

#This database is used to store the friendships between people
class friends(db.Model):
    # Each row will be given a unique id, this is how we store data in the database view rows and columns
    _id = db.Column("id", db.Integer, primary_key=True)
    friend1 = db.Column(db.String(2000))
    friend2 = db.Column(db.String(2000))

    # Used to define each friendship or ID within our database
    def __init__(self, friend1, friend2):
        self.friend1 = friend1
        self.friend2 = friend2

#This database will handle all friend requests that get sent to users
class requests(db.Model):
    # Each row will be given a unique id, this is how we store data in the database view rows and columns
    _id = db.Column("id", db.Integer, primary_key=True)
    toFriend = db.Column(db.String(2000))
    fromFriend = db.Column(db.String(2000))

    # Used to define each friendship or ID within our database
    def __init__(self, toFriend, fromFriend):
        self.toFriend = toFriend
        self.fromFriend = fromFriend
#This database will store every sent message from one user to another
class talk(db.Model):
    # Each row will be given a unique id, this is how we store data in the database view rows and columns
    _id = db.Column("id", db.Integer, primary_key=True)
    speaker = db.Column(db.String(2000))
    hearer = db.Column(db.String(2000))
    text = db.Column(db.String(2000))

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
        found_user = users.query.filter_by(uname=user).first()
        flash("Login successful", "info")
        #In the user page, the user can add their email, and it will be saved within the database for their specific user
        if request.method == "POST":
            email = request.form["email"]
            if email:
                session["email"] = email
                found_user.email = email
                db.session.commit()
                #Message to notify the user that the email was successfully saved
                flash("Email was saved!")
                flash(f"Email: {email}")
            else:
                email = found_user.email
        else:
            if "email" in session:
                email = session["email"]
                return render_template("user.html", text = user, email = email)
        return render_template("user.html", text=user)
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
        #Checks to make sure that the username, password, or email is not matching any of the users within
        #our database
        if found_user:
            flash("Username has already been taken","info")
        elif found_pswd:
            flash("Username has already been taken", "info")
        elif found_email:
            flash("Username has already been taken", "info")
        else:
            age = request.form["ag"]
            #Since we made age optional, we have to check for age and see if a value ha been inputted for
            #age, else we just assign its value to None
            if not age:
                age = None
            else:
                session["age"] = age
            pic = request.files["png"]
            # Since we made profile pic optional, we have to check for profile pic and see if a value ha been inputted
            # for profile pic, else we just assign its value to None
            if not pic:
                picture = "static/profile_icon.png"
            else:
                filespace = pic.filename
                picture = os.path.join("static", filespace)
                pic.save(picture)
            session["user"] = user
            session["word"] = word
            session["email"] = email
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
                image.save(path)
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
            return render_template("edit.html", pic=found_user.image, email=email, phone=phone, bio=bio,
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

@app.route("/seeUsers", methods = ["POST", "GET"])
def seeUsers():
    #First we check and see if the user is logged in already
   if "user" in session:
       valid = False
       if request.method == "POST":
           #If the user submits the name of the user they would like to see, we will get the input
           #To see if it is a user in our database.
            name = request.form["person"]
            session["chat1"] = name
           #To ensure that the user can not accidentally pull up their own profile
            if name == session["user"]:
                return render_template("seeUsers.html")
            found_user = found_user = users.query.filter_by(uname=name).first()
            if found_user:
                #We will send these values of the user to the template, but we will first check that the values
                #are not empty, because if the are then we will just put in a substitute or placeholder value
                valid = True
                name = found_user.uname
                session["person"] = name
                img = found_user.image
                if not img:
                    img = "static/profile_icon.png"
                age = found_user.age
                if not age:
                    age = "N/A"
                email = found_user.email
                if not email:
                    email = "N/A"
                return render_template("seeUsers.html", text = valid, name = name, img = img,
                                       age = age, email = email)
            else:
                #If the user is not found, then we will let the user know via an alert
                alert = "User does not exist"
                return render_template("seeUsers.html", alert = alert)
       #Runs if the user is not searching up a user
       return render_template("seeUsers.html")
   else:
       #This text will display on the seeUsers page and direct the user to the login page if they are not logged in
       speech = "You must log in first to access this page"
       return render_template("seeUsers.html", speech=speech)



@app.route("/displayUser", methods = ["POST", "GET"])
#This handles the displaying of profiles of other users that the user in session would like to view
def displayUser():
    if "user" in session:
        username = session["person"]
        found_user = users.query.filter_by(uname=username).first()
        # If the user data is found in the database, then we will collect all teh users information to display
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
            return render_template("details.html", photo=picture, email=mail, age=age, user=username,
                                   phone=phone, brith=brith, address=address, bio=bio, education1=education1
                                   , education2=education2, education3=education3, activity1=activity1,
                                   activity2=activity2, activity3=activity3)
        else:
            #Displays if the user does not exist within our database
            flash("User not found", "info")
            return redirect(url_for("user"))
    else:
        # this will only pop up if the user is not logged in and tries to access the details page
        flash("You are not logged in", "info")
        # if the user is not logged in, then we will redirect the user to the login page
        return redirect(url_for("login"))
        # We pass the information into the details page to display the users details

@app.route("/addRequest", methods = ["POST","GET"])
#This helps to create the friend requests sent out by users to other users
def addRequest():
    sender = session["user"]
    reciever = request.form["name"]
    found_request = requests.query.filter_by(toFriend=reciever, fromFriend=sender).first()
    #Checks first to see if the user has already sent a friend request that is pending currently
    if found_request:
        return jsonify({"message": f"You have already sent a friend request to {reciever}"})
    friendsFirst = friends.query.filter_by(friend1=sender,friend2=reciever).first()
    friendsSecond = friends.query.filter_by(friend1=reciever, friend2=sender).first()
    #Checks to see if the user is already friends with the person they are trying to send a friend request to
    if friendsFirst or friendsSecond:
        return jsonify({"message": f"{reciever} is already one of your friends"})
    #Where we exactly crate teh friend request and add it to our friend request database
    friending = requests(reciever, sender)
    # add the new account to the database
    db.session.add(friending)
    db.session.commit()
    #Notify the user that the friend request was successful
    return jsonify({"message": f"Your friend request to {reciever} has been successfully sent"})

@app.route("/viewRequests", methods=["POST","GET"])
#Allows the user to view friend request that were sent to them
def viewRequets():
    if "user" in session:
        # we will get all the friend request sent to the user and store it within a list
        void = []
        username = session["user"]
        catalog = requests.query.filter_by(toFriend=username).all()
        for cat in catalog:
            #checks to see if the sender of the request is a user within our database
            found_person = users.query.filter_by(uname=cat.fromFriend).first()
            if found_person:
                void.append(found_person)

        #We will send the list of people who sent a friend request to the user to the front end for the page to display
        return render_template("viewRequests.html", catalog = void)
    else:
        #Activates if the user is not logged in currently
        alert = "You need to log in first to access this page"
        return render_template("viewRequests.html", alert = alert)

@app.route("/addBack", methods=["POST","GET"])
#Used to allow the user to add people back that requested to be friends
def addBack():
    username = session["user"]
    name = request.form["name"]
    #Here we will get the user that the person in session added back as a friend
    #Once the user has been added back as a friend, we will then delete the friend request
    if name:
        found_request = requests.query.filter_by(fromFriend=name).first()
        if found_request:
            match = friends(username,found_request.fromFriend)
            db.session.add(match)
            db.session.delete(found_request)
            db.session.commit()
            #Lets the user in session know that the friend has been added back successfully
            return jsonify({"message": f"{name} is now your friend"})
        else:
            #Will display if the friend request could not be found
            return jsonify({"message": "There was an error with finding the user"})
    else:
        #If the name of the user is not within our database, then we send this message
        return jsonify({"message": "Name not found"})

@app.route("/seeFriends", methods=["POST","GET"])
#Allows the user to see all the friends on their friends list
def seeFriends():
    if "user" in session:
        if request.method == "POST":
            session["chat1"] = request.form["chat"]
            return jsonify({"message": "Navigating to chat room"})
        #We will store all the users friendships within this list
        list = []
        username = session["user"]
        #If the users name is found in a paired friendship within our database, then we will add that user to their
        #friends list
        for partner in friends.query.all():
            if partner.friend1 == username:
                name = partner.friend2
                found_user = users.query.filter_by(uname=name).first()
                list.append(found_user)
            elif partner.friend2 == username:
                name = partner.friend1
                found_user = users.query.filter_by(uname=name).first()
                list.append(found_user)


        return render_template("seeFriends.html",network = list)
    else:
        #Executes only if the user is not logged in
        alert = "You are currently not logged in, please log in first to access this page"
        return render_template("seeFriends.html", alert = alert)

@app.route("/displayPerson", methods = ["POST", "GET"])
def displayPerson():
    #Checks to see if the user is logged in
    if "user" in session:
        session["person"] = request.form["name"]
        #This is where we get the name of the user that the user in session would like to view
        username = session["person"]
        found_user = users.query.filter_by(uname=username).first()
        #Let the user know that we will be successfully navigating to the user of interest profile
        if found_user:
            return jsonify({"message": f"Navigating to {session["person"]}'s profile"})
        else:
            return jsonify({"message": "User not found"})
    else:
        # this will only pop up if the user is not logged in and tries to access the details page
        flash("You are not logged in", "info")
        # if the user is not logged in, then we will redirect the user to the login page
        return redirect(url_for("login"))

@app.route("/removeFriend", methods = ["POST", "GET"])
#This will be in charge of removing friends from a users friend list
def removeFriend():
    if "user" in session:
        remove = request.form["name"]
        username = session["user"]
        #We will look through the friends list to locate the friend of interest that the user wants to remove
        #So that we can remove them
        found_friend1 = friends.query.filter_by(friend1=remove, friend2=username).first()
        found_friend2 = friends.query.filter_by(friend1=username, friend2=remove).first()
        if found_friend1:
            db.session.delete(found_friend1)
            db.session.commit()
            #Notify the user if the removal was successful
            return jsonify({"message": f"{remove} has successfully been removed from your friends list"})
        elif found_friend2:
            db.session.delete(found_friend1)
            db.session.commit()
            # Notify the user if the removal was successful
            return jsonify({"message": f"{remove} has successfully been removed from your friends list"})
        else:
            #Appears if we can not find the user
            return jsonify({"message": "User not found"})
    else:
        # this will only pop up if the user is not logged in and tries to remove a Friend
        return jsonify({"message": False})

@app.route("/chat", methods=["POST","GET"])
#Used to handle chats between all users
def chat():
    if "user" in session:
        #Here we will get the two users that we will be making a chat room between
        speakTo = session["chat1"]
        username = session["user"]
        #We will also find the two people chatting within our user database
        found_hearer = users.query.filter_by(uname=speakTo).first()
        found_speaker = users.query.filter_by(uname=username).first()
        #We will get all the conversations
        found_convo = talk.query.all()
        #Used to update the conversation logs between both users if a message is sent
        if request.method == "POST":
            message = request.form["message"]
            if message:
                converse = talk(speaker=username, hearer=speakTo, text=message)
                db.session.add(converse)
                db.session.commit()
                found_convo = talk.query.all()
        if found_convo:
            return render_template("chat.html", speaking =found_speaker, hearing=found_hearer, convo=found_convo)

        return render_template("chat.html", speaking = found_speaker, hearing = found_hearer)

    else:
        #executes is the user tries to access chat without being logged in
        alert = "you are not logged in, log in first to access this page"
        return render_template("chat.html", alert=alert)


if __name__ == "__main__":
    with app.app_context():
        # Creates the database when the python file is run
        db.create_all()
    app.run(debug = True)