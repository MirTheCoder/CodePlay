from flask import Flask, render_template

app = Flask(__name__)
#These are all routes to various art templates, wand the first route leads to the home page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/retro')
def retro():
    return render_template('retro.html')

@app.route('/retroBash')
def retroBash():
    return render_template('retroBash.html')

@app.route('/pumpitUp')
def pumpItUp():
    return render_template('pumpitUp.html')
@app.route('/Immanuel')
def immaneul():
    return render_template('Immanuel.html')
@app.route('/villageHero')
def villageHero():
    return render_template('villageHero.html')
@app.route('/EmbraceOfNature')
def embraceOfNature():
    return render_template("EmbraceOfNature.html")
if __name__ == '__main__':
    #Adding the debugger allows you to see the changes you make in real time on the web server while its running
    #Also allows you to see error messages as well
    app.run(debug=True)