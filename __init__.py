##Flask day udemy program 1
from flask import Flask,render_template,flash,request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/dashboard/')
def dashboard():
    try:
        return render_template("dashboard.html")
    except Exception as e:
        return render_template("500.html")

@app.route('/login/')
def check_login():
    return render_template("login.html")

@app.route('/register/')
def register_users():
    return render_template("signup.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

app.run(debug=True)
