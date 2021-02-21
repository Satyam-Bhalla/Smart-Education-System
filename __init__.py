from flask import Flask, render_template, redirect, url_for, request, session, flash, g, make_response, send_file
# from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from wtforms import Form, StringField, BooleanField, TextField, PasswordField, validators
# from passlib.hash import sha256_crypt
# from html.parser import HTMLParser
import html
from connecting_db import Connection
from os import urandom
from ast import literal_eval
from random import shuffle, randrange

app = Flask(__name__)

def tellQues(subject,diff=1):
    '''
        takes a subject, and diff as parameter for new question
        returns the question as tuple
    '''
    qNo = randrange(((90*(subject-1))+(30*(diff-1))+1), ((90*(subject-1))+(30*diff)+1))
    c, conn = Connection()
    query = "SELECT * from question_answers where id = "+str(qNo)
    x = c.execute(query)
    for i in x:
        if len(i)>0:
            i = list(i)
            i[3] = literal_eval(i[3])
            ra = i.pop(2)
            print(ra)
            i[2].append(ra)
            shuffle(i[2])
            print(i)
            i[1] = html.unescape(i[1])
            print(i)
            return i
    c.close()
    conn.close()

def setSession(user):
    session['user'] = user
    session['solved'] = []
    session['solvedQues'] = []
    # session['solvedResp'] = dict()

def updateScore(qdiff, right):
    '''
        take the difficulty of the question that is solved
        and a bool value if it is correct or not
        and updates the solved of session
    '''
    if right:
        # if correct then, add this qdiff to previous score
        if len(session['solved']) != 0: 
            session['solved'].append(session['solved'][-1]+qdiff)
        else:
            session['solved'].append(0)
            session['solved'].append(qdiff)    
    else:
        # if incorrect then, subtract qdiff to previous score 
        if len(session['solved']) != 0:    
            session['solved'].append(session['solved'][-1]-qdiff)
        else:
            session['solved'].append(0)
            session['solved'].append(-qdiff)

class SignUpForm(Form):
    '''
    class for signup form
    as we are going to same page for login and signup
    we handle that by own
    '''
    fname = StringField('First Name',[
        validators.DataRequired()
    ])
    lname = StringField('Last Name',[
        validators.DataRequired()
    ])
    email = StringField('Email',[
        validators.DataRequired()
    ])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password Not Matched')
    ])
    confirm = PasswordField('Confirm Password')

class LoginForm(Form):
    #as the sign up for it is class for login form
    uname = StringField('Email',[
        validators.DataRequired()
    ])
    lpassword = PasswordField('Password',[
        validators.DataRequired()
    ])

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/logsign', methods=["GET","POST"])
def logsign_page():
    error = ''
    if request.method == "POST":
        if 'username' in request.form:
            l_uname = request.form['username']
            l_pass = request.form['password']
            # we should ask for the role to as login as it can be a parent and a student at same time
            l_role = request.form['role']
            #create connection with database
            c, conn = Connection()
            query = " SELECT '"+l_pass+"' = (SELECT password FROM "+l_role+" WHERE email = '"+l_uname+"')"
            c = c.execute(query)
            x = c.fetchone()
            # user not exists = (None,)
            # pass not match = (0,)
            # pass match = (1,0)
            # user exists??
            if x[0] == None:
                c.close()
                conn.close()
                return render_template("logsign.html", error="Wrong Email")
            elif x[0] == 0:
                c.close()
                conn.close()
                return render_template("logsign.html", error="Wrong Password")
            else:
                setSession(user = l_uname)
                c.close()
                conn.close()
                return redirect('/dashboard')    
        else:
            s_fname = request.form['firstname']
            s_mname = request.form['midname']
            s_lname = request.form['lastname']
            s_email = request.form['email']
            s_pass = request.form['password']
            s_roll = request.form['role']
            if s_mname == "":
                s_name = s_fname + " " + s_lname
            else:
                s_name = s_fname +" "+ s_mname + " "+ s_lname
            # to free up the space a little bit as we will be using s_name
            del s_fname
            del s_mname
            del s_lname
            query = "SELECT name FROM "+s_roll+" WHERE email = '"+s_email+"'"
            c, conn = Connection()
            c = c.execute(query)
            x = c.fetchone()
            if type(x) == type(tuple()):
                c.close()
                conn.close()
                return render_template("logsign.html",error="User already exists")
            else:
                query = "INSERT INTO "+s_roll+"(name, email, password) VALUES ('"+s_name+"','"+s_email+"','"+s_pass+"')"
                c.execute(query)
                conn.commit()
                c.close()
                conn.close()
                return render_template("logsign.html", msg="You Can Login Now")
    return render_template("logsign.html")

@app.route('/fgtPass')
def fgtpass():
    return render_template("fgtpass.html")

@app.route('/dashboard' ,methods=["GET","POST"])
def dashboard():
    if 'user' in session:
        if request.method == "POST":
            quesans = request.form['ans']
            qid = request.form['id']
            qdiff = int(request.form['difficulty'])
            session['solvedQues'].append(int(qid)) 
            c, conn = Connection()
            query = "SELECT '"+quesans+"' = (SELECT answer FROM question_answers WHERE id = "+qid+")"
            c = c.execute(query)
            x = c.fetchone()
            if x[0] == 1:
                updateScore(qdiff = qdiff, right = True)
                # and raise a level
                # we can check for times the answer was correct too
                # and cal increase or decrease the level on that 
                if qdiff != 3:
                    qdiff += 1
            else:
                updateScore(qdiff = qdiff, right = False)
                # and drop a level
                if qdiff != 1:
                    qdiff -= 1
            # send the question of new difficulty to dashboard
            session.modified = True
            subject = randrange(1,4)
            return render_template("dashboard.html",question=tellQues(subject = subject, diff = qdiff))
        subject = randrange(1,4)
        return render_template("dashboard.html",question=tellQues(subject = subject))
    return redirect('/logsign')

@app.route("/logout")
def logout():
    solved = []
    session.pop('user', None)
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
    secret_key = urandom(134)
    print("\n Secret_key = ", secret_key, " \n")
    app.secret_key = secret_key
    app.run(debug=True)