from flask import Flask, render_template, redirect,url_for, request, session, flash, g, make_response, send_file
##from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from connecting_db import Connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard/')
def dashboard():
    try:
        return render_template("dashboard.html")
    except Exception as e:
        return render_template("500.html")

@app.route('/login/', methods=["GET","POST"])
def login_page():

    error = ''
    try:
	
        if request.method == "POST":
		
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            #flash(attempted_username)
            #flash(attempted_password)

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('dashboard'))
				
            else:
                error = "Invalid credentials. Try Again."

        return render_template("logsign.html", error = error)

    except Exception as e:
        #flash(e)
        return render_template("logsign.html", error = error)  

@app.route('/signupp/', methods=["GET","POST"])
def register_user():
    try:
        c, conn = Connection()
        return("okay")
    except Exception as e:
        return(str(e))
        


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

app.run(debug=True)
