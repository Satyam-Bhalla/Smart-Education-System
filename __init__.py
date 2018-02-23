from flask import Flask, render_template, redirect,url_for, request, session, flash, g, make_response, send_file
##from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from connecting_db import Connection
import gc

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
        c, conn = Connection()
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            attempted_firstname = request.form['firstname']
            attempted_lastname = request.form['lastname']
            attempted_email = request.form['email']
            attempted_passwd = request.form['passwd']
            if not attempted_firstname:
                if attempted_username == "admin" and attempted_password == "password":
                    return redirect(url_for('dashboard'))
                    
                else:
                    error = "Invalid credentials. Try Again."
            else:
                x = c.execute("SELECT * from users where email=(?)",attempted_email)
                if int(len(x))>0:
                    error = "User already exist"
                    return render_template("logsign.html",error=error)
                else:
                    c.execute("INSERT INTO users(first_name,last_name,email, password) VALUES (?,?,?,?)",(attempted_firstname,attempted_lastname,attempted_email,attempted_passwd))
                    c.commit()
                    return render_template(url_for('dashboard'))
        c.close()
        conn.close()
        # gc.close()
        return render_template("logsign.html", error = error)

    except Exception as e:
        #flash(e)
        print(e)
        return render_template("logsign.html", error = e)  



@app.route('/signup/', methods=["GET","POST"])
def register_user():
    try:
        c, conn = Connection()
        
        gc.collect()
    except Exception as e:
        return(str(e))
        


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

app.run(debug=True)
