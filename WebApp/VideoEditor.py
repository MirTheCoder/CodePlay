from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('video.html')

@app.route('/editor',methods=['POST'])
def editor():
    return render_template('editor.html')

if __name__ == '__main__':
    app.run(debug=True)