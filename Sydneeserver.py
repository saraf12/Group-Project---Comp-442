import sqlite3
import os
import base64
import time
from traceback import print_exc
from cryptography.fernet import Fernet
from passlib.hash import bcrypt_sha256
from flask import Flask, render_template, request, redirect, url_for, abort, session, flash, g
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["SECRET_KEY"] = "correcthorsebatterystaple"

scriptdir = os.path.dirname(__file__)

dbpath = os.path.join(scriptdir, "gamematching.sqlite3")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(dbpath)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

conn = sqlite3.connect(dbpath)

c = conn.cursor()

c.execute('''
            DROP TABLE IF EXISTS Users;
            ''')

c.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                name TEXT,
                email TEXT,
                passwordhash TEXT,
                performanceRating INTEGER,
                wins INTEGER,
                losses INTEGER,
                totGamesPlayed INTEGER,
                iconLink TEXT
            );
            ''')

conn.commit()

#save this key somewhere outside the database!
key = Fernet.generate_key()
pep = Fernet(key)

#hash a password (pwd) and user pepper (pep)
def hash_password(pwd, pep):
    #compute the 14 round bcrypt hash
    # of the sha256 hash of the password
    h = bcrypt_sha256.using(rounds=14).hash(pwd)
    # encrypt with AES (pepper)
    ph = pep.encrypt(h.encode('utf-8'))
    # encode as base64 string and return
    b64ph = base64.b64encode(ph)
    return b64ph

#check password and pwd against b64ph
def check_password(pwd, b64ph, pep):
    # decode the encrypted base64 hash
    ph = base64.b64decode(b64ph)
    # decrypt the hash (remove pepper)
    h = pep.decrypt(ph)
    # let passlib check the hash
    return bcrypt_sha256.verify(pwd, h)

@app.route("/register/", methods=["GET"])
def get_register():
    return render_template("registerPage.html")

@app.route("/signin/", methods=["GET"])
def get_signin():
    return render_template("signInPage.html")

@app.route("/register/", methods=["POST"])
def post_register():
    regdb = get_db()
    c = get_db().cursor()
    data = dict()
    fields = ['Iprofile','username', 'name', 'email', 'password', 'confirm-password']
    for field in fields:
        data[field] = request.form.get(field)
    valid = True
    for field in fields:
        if data[field] is None or data[field] == "":
            valid = False
            flash(f"{field} cannot be blank")
    if valid and len(data['password']) < 8:
        valid = False
        flash("password must be at least 8 characters")
    if valid and data['password'] != data['confirm-password']:
        valid = False
        flash("password and confirm password must match")
    if valid:
        session['email'] = data['email']
        print("This is the email: " + str(data['email']))
        uid = c.execute('SELECT id FROM Users WHERE email=?;',(data['email'],)).fetchone()
        print("This is the uid:" + str(uid))
        #if a user is found, then this email address is taken
        if uid is not None:
            flash("An account with this email already exists")
            return redirect(url_for("get_register"))
        # otherwise add them to the database and redirect to login
        passtohash = data['password']
        print(passtohash)
        h = hash_password(data['password'], pep)
        print("This is val of pep in post_register:" + str(pep))
        c.execute('INSERT INTO Users (username, name, email, passwordhash,iconLink) VALUES (?,?,?,?,?);', 
            (data['username'], data['name'], data['email'], h, data['Iprofile']))
        regdb.commit()
        uid = c.execute('SELECT id FROM Users WHERE email=?;',(data['email'],)).fetchone()
        print("This is the uid after adding entry:" + str(uid))
        savedhash = c.execute('SELECT passwordhash FROM Users WHERE id=?;',(uid[0],)).fetchone()
        print(savedhash)
        return redirect(url_for("get_signin"))
    else:
        return redirect(url_for("get_register"))


@app.route("/signin/", methods=["POST"])
def post_signin():
    signindb = get_db()
    c = get_db().cursor()
    try: 
        username = request.form.get('username')
        passwordtxt = request.form.get('password')
        # print("This is the value of pep in post_signin:" + str(pep))
        print(passwordtxt)
        password = hash_password(passwordtxt, pep)
        # print(password)
        uid = c.execute('SELECT id FROM Users WHERE username=?;',(username,)).fetchone()
        savedhash = c.execute('SELECT passwordhash FROM Users WHERE id=?;',(uid[0],)).fetchone()
        # print(savedhash)
        if uid is not None and savedhash is not None: 
            if check_password(passwordtxt, savedhash[0], pep):
                session['uid'] = uid
                session['expires'] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
                # return f"{uid}"
                return redirect(url_for("main_page"))
            else:
                flash("Password is incorrect")
                return redirect(url_for("get_signin"))
    except Exception:
        flash("User does not exist")
        print_exc()
        return redirect(url_for("get_signin"))

@app.route("/mainpage/", methods=["GET"])
def main_page():
    return render_template("mainPage.html")

@app.route("/profilepage/", methods=["GET"])
def profile_page():
    return render_template("profilePage.html")

@app.route("/editprofile/", methods=["GET"])
def get_edit_profile_page():
    return render_template("editProfile.html")

@app.route("/editprofile/", methods=["POST"])
def post_edit_profile_page():
    regdb = get_db()
    c = get_db().cursor()
    data = dict()
    fields = ['username', 'name', 'email', 'password', 'confirm-password']
    for field in fields:
        data[field] = request.form.get(field)
    valid = True
    if valid and data['password'] is not None and len(data['password']) < 8:
        valid = False
        flash("password must be at least 8 characters")
    if valid and data['password'] != data['confirm-password']:
        valid = False
        flash("password and confirm password must match")
    if valid:
        session['email'] = data['email']
        #print("This is the email: " + str(data['email']))
        uid = c.execute('SELECT id FROM Users WHERE email=?;',(data['email'],)).fetchone()
       # print("This is the uid:" + str(uid))
        #if a user is found, then this email address is taken
        # otherwise add them to the database and redirect to login
        if data['password'] is not None:
            passtohash = data['password']
            print(passtohash)
            h = hash_password(data['password'], pep)
        #print("This is val of pep in post_register:" + str(pep))
        if data['username'] is not None:
            c.execute('INSERT INTO Users (username) VALUES(?);',
            (data['username']))
        if data['name'] is not None:
            c.execute('INSERT INTO Users (name) VALUES(?);',
            (data['name']))
        if h is not None:
            c.execute('INSERT INTO Users (passwordhash) VALUES(?);',
            (h))
        regdb.commit()
        uid = c.execute('SELECT id FROM Users WHERE email=?;',(data['email'],)).fetchone()
        # print("This is the uid after adding entry:" + str(uid))
        # savedhash = c.execute('SELECT passwordhash FROM Users WHERE id=?;',(uid[0],)).fetchone()
        # print(savedhash)
        return redirect(url_for("get_signin"))
    else:
        return redirect(url_for("get_register"))


@app.route("/matchup/", methods=["GET"])
def matchup_window():
    return render_template("matchup.html")
    