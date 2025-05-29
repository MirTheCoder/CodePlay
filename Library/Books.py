from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/read")
def read():
    return render_template("read.html")



if __name__ == '__main__':
    app.run(debug=True)