from flask import Flask, render_template, redirect,url_for, request, session, flash, g, make_response, send_file
##from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from connecting_db import Connection
import gc
import os
import ast
import random

app = Flask(__name__)
app.secret_key = os.urandom(134)

solved = []


@app.route('/')
def index():
    return render_template("index.html")

def tellQues(qNo):
    c, conn = Connection()
    x = c.execute("SELECT * from question_answers where id=?",(qNo,))
    for i in x:
        if len(i)>0:
            i = list(i)
            i[3] = ast.literal_eval(i[3])
            ra = i.pop(2)
            i[2].append(ra)
            random.shuffle(i[2])
            return i
    c.close()
    conn.close()



@app.route('/dashboard/' ,methods=["GET","POST"])
def dashboard():
    try:
        if 'user' in session:
            subject = random.randrange(1,4)
            ques = random.randrange(((90*(subject-1))+1), ((90*(subject-1))+31))
            return render_template("dashboard.html",question=tellQues(ques))
        else:
            return render_template("logsign.html")
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
            x = c.execute("SELECT email from users where email=?",(attempted_email,))
            if x.rowcount > 0:
                error = "User already exists"
                c.close()
                conn.close()
                return render_template("logsign.html",error=error)
            else:
                c, conn = Connection()
                c.execute("INSERT INTO users(first_name,last_name,email, password) VALUES (?,?,?,?)",(attempted_firstname,attempted_lastname,attempted_email,attempted_passwd))
                conn.commit()
                c.close()
                conn.close()
                session['users'] = attempted_email
                session['solvedAns'] = []
                # session['curQuesNo'] = 1
                # session['solvedQues'] = ""

                return redirect('/dashboard/')
        except Exception as e:
            error = "Connection error"
            return render_template("logsign.html",error=e)


@app.route('/quesCheck/', methods=["POST"])
def quesCheck():
    if request.method == "POST":
        quesans = request.form['ans']
        qid = request.form['id']
        c, conn = Connection()
        x = c.execute("SELECT answer FROM question_answers WHERE id = ?",(qid,))
        j = (int(qid)-1)//30;
        if 'solved' not in session:
            session['solved'] = []
        for i in x:
            if i[0] == quesans:
                if j not in [2,5,8]:
                    j+=1
                solved.append(1*((j%3)+1))
            else:
                if j not in [0,3,6]:
                    j-=1
                solved.append(0)
        ques = random.randrange((30*j)+1,(30*(j+1))+1)
        print(solved)
        print(ques)
        return render_template("dashboard.html",question=tellQues(ques),solved=solved)



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
                    session['user'] = attempted_username
                    if 'solved' not in session:
                        session['solved'] = []
                    return redirect("/dashboard/")
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
        

@app.route("/logout/")
def logout():
    solved = []
    session.pop('user', None)
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

app.run(debug=True)
