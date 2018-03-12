from flask import Flask, render_template, redirect, url_for, request, session, flash, g, make_response, send_file
# from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from wtforms import Form, StringField, BooleanField, TextField, PasswordField, validators
# from passlib.hash import sha256_crypt
from connecting_db import Connection
from os import urandom
from ast import literal_eval
from random import shuffle, randrange

app = Flask(__name__)

solved = []

def tellQues(qNo):
    '''
        takes a question number as parameter
        returns the question as tuple
    '''
    c, conn = Connection()
    x = c.execute("SELECT * from question_answers where id=?",(qNo,))
    for i in x:
        if len(i)>0:
            i = list(i)
            i[3] = literal_eval(i[3])
            ra = i.pop(2)
            i[2].append(ra)
            shuffle(i[2])
            return i
    c.close()
    conn.close()

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
            query = "SELECT password FROM "+l_role+" WHERE email = '"+l_uname+"'"
            c = c.execute(query)
            x = c.fetchone()
            # user exists??
            if type(x) == type(tuple()):
                # match password
                if l_pass == x[0]:
                    # set the session for the user
                    session['user'] = l_uname
                    c.close()
                    conn.close()
                    return redirect('/dashboard')
                c.close()
                conn.close()
                return render_template("logsign.html", error="Wrong Pass")
            c.close()
            conn.close()
            return render_template("logsign.html", error="Wrong Email")
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
    if request.method != "POST":
        if 'user' in session:
            subject = randrange(1,4)
            ques = randrange(((90*(subject-1))+1), ((90*(subject-1))+31))
            return render_template("dashboard.html",question=tellQues(ques))
        else:
            return redirect('/logsign')
    else:
        return render_template("500.html")

'''
@app.route('/signup',methods=["GET","POST"])
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
'''

@app.route('/quesCheck', methods=["POST"])
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
        ques = randrange((30*j)+1,(30*(j+1))+1)
        print(solved)
        print(ques)
        return render_template("dashboard.html",question=tellQues(ques),solved=solved)

'''
@app.route('/login2', methods=["GET","POST"])
def login_page2():
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
        return render_template("logsign.html", error = error)

    except Exception as e:
        #flash(e)
        print(e)
        return render_template("logsign.html", error = e)
'''

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