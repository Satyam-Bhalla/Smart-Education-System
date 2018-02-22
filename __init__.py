##Flask day udemy program 1
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("main.html")

app.run(debug=True)
