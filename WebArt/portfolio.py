from flask import Flask, render_template

app = Flask(__name__)

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
    app.run(debug=True)