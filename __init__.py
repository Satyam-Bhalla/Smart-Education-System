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


@app.route('/signup/',methods=["GET","POST"])
def signup_page():
    error = ''
    if request.method == "POST":
        attempted_firstname = request.form['firstname']
        attempted_lastname = request.form['lastname']
        attempted_email = request.form['email']
        attempted_passwd = request.form['passwd']
        try:
            c, conn = Connection()
            print(1)
            x = c.execute("SELECT email from users where email=?",(attempted_email,))
            print(2)
            print(x.rowcount)
            print(dir(x))
            if x.rowcount > 0:
                error = "User already exists"
                c.close()
                conn.close()
                print(11)
                return render_template("logsign.html",error=error)
            else:
                c, conn = Connection()
                c.execute("INSERT INTO users(first_name,last_name,email, password) VALUES (?,?,?,?)",(attempted_firstname,attempted_lastname,attempted_email,attempted_passwd))
                print(3)
                conn.commit()
                c.close()
                conn.close()
                return redirect('/dashboard/')
        except Exception as e:
            error = "Connection error"
            return render_template("logsign.html",error=e)


@app.route('/login/', methods=["GET","POST"])
def login_page():
    error = ''
    try:
        c, conn = Connection()
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            print(attempted_username)
            x = c.execute("SELECT * FROM users WHERE email=? AND password=?",(attempted_username,attempted_password,))
            for i in x:
                if len(i)>0:
                    c.close()
                    conn.close()
                    return render_template("dashboard.html")
                else:
                    error = "User doesn't exist"
                    c.close()
                    conn.close()
                    return render_template("logsign.html",error=error)
        # else:
        c.close()
        conn.close()
        # gc.close()
        return render_template("logsign.html", error = error)

    except Exception as e:
        #flash(e)
        print(e)
        return render_template("logsign.html", error = e)
        


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

app.run(debug=True)
