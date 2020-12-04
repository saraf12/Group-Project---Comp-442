import sqlite3
import os
import base64
import time
from datetime import datetime, timedelta
from traceback import print_exc
from cryptography.fernet import Fernet
from passlib.hash import bcrypt_sha256
from flask import Flask, render_template, request, redirect, url_for, abort, session, flash, g, jsonify, make_response, json
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["SECRET_KEY"] = "correcthorsebatterystaple"

scriptdir = os.path.dirname(__file__)

dbpath = os.path.join(scriptdir, "matchingsite.sqlite3")

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
            CREATE TABLE IF NOT EXISTS Admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userName TEXT,
                password TEXT
            );
            ''')

c.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                name TEXT,
                email TEXT,
                passwordhash TEXT,
                icon TEXT
            );
            ''')

c.execute('''
            CREATE TABLE IF NOT EXISTS Games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            );
            ''')

c.execute('''
            CREATE TABLE IF NOT EXISTS Stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT,
                game INTEGER,
                performanceRating INTEGER DEFAULT 1200,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                totGamesPlayed INTEGER DEFAULT 0,
                FOREIGN KEY (user) REFERENCES Users(id),
                FOREIGN KEY (game) REFERENCES Games(id)
            );
            ''')

conn.commit()

serverdir = os.path.dirname(__file__)
pepfile = os.path.join(serverdir, "pepper.bin")
with open(pepfile, 'rb') as fin:
    key = fin.read()
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

@app.route("/")
@app.route("/signin/", methods=["GET"])
def get_signin():
    #session['uid'] = ""
    return render_template("signInPage.html")

@app.route("/signin/", methods=["POST"])
def post_signin():
    signindb = get_db()
    c = get_db().cursor()

    data = dict()
    fields = ['username', 'password']
 
    for field in fields:
        data[field] = request.form.get(field)

    if data['username'] == "admin":
        return redirect(url_for("get_admin"))
    return redirect(url_for("get_admin_dashboard"))

@app.route("/register/", methods=["GET"])
def get_register():
    return render_template("register.html")

@app.route("/register/", methods=["POST"])
def post_register():
    regdb = get_db()
    c = get_db().cursor()
    data = dict()
    fields = ['username', 'name', 'email', 'password', 'confirm-password', 'Iprofile']
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

        uid = c.execute('SELECT id FROM Users WHERE email=?;',(data['email'],)).fetchone()

        # if a user is found, then this email address is taken
        if uid is not None:
            flash("An account with this email already exists")
            return redirect(url_for("get_register"))
        uid = c.execute('SELECT id FROM Users WHERE username=?;',(data['username'],)).fetchone()

        # if a user is found, then this email address is taken
        if uid is not None:
            flash("An account with this username already exists")
            return redirect(url_for("get_register"))
        # otherwise add them to the database and redirect to login
        passtohash = data['password']

        h = hash_password(data['password'], pep)

        c.execute('INSERT INTO Users (username, name, email, passwordhash, icon) VALUES (?,?,?,?,?);', 
            (data['username'], data['name'], data['email'], h, "you"))
        regdb.commit()

        return redirect(url_for("get_signin"))
    else:
        return redirect(url_for("get_register"))

#22222~~~~~
@app.route("/admin/", methods = ["GET"])
def get_admin():
    return render_template("admin.html")

#33333~~~~~
@app.route("/admin/", methods = ["POST"])
def post_admin():

    fields = ['username', 'password']

    data = dict()

    for field in fields:
        data[field] = request.form.get(field)
    
    print(f"{data}")
    valid = True
    
    if data['username'] is None or data['username'] == "" and data['password'] is None or data['password'] == "":
        valid = False
        flash("Username & Password cannot be blank")
        return redirect(url_for("get_admin"))

    if data['username'] is None or data['username'] == "":
        valid = False
        flash("Username cannot be blank")
        return redirect(url_for("get_admin"))

    if data['password'] is None or data['password'] == "":
        valid = False
        flash("Password cannot be blank")
        return redirect(url_for("get_admin"))

    if data['password'] != "":
        if len(data['password']) < 8:
            valid = False
            flash("password must be at least 8 characters")
            return redirect(url_for("get_admin"))

    return redirect(url_for('get_admin_dashboard'))
    
@app.route("/admin_dashboard/", methods = ["GET"])
def get_admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/create_game/", methods = ["GET"])
def get_create_game():
    return render_template("admin_dash_games.html")


@app.route("/create_game/", methods = ["POST"])
def post_create_game():
    admindb = get_db()
    c = get_db().cursor()

    gameToAdd = request.form.get('gamename')

    alreadyExists = c.execute('SELECT id, name FROM Games WHERE name=?',(gameToAdd,)).fetchone()
    if alreadyExists:
        flash(f"Game category entered already exists")
        return redirect(url_for("get_admin_dashboard"))
    
    c.execute('''
            CREATE TABLE IF NOT EXISTS {} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username1 TEXT,
                username2 TEXT,
                winnerAccordingToU1 TEXT,
                winnerAccordingToU2 TEXT,
                status TEXT,
                dateCreated DATETIME NOT NULL DEFAULT(DATETIME('now')),
                FOREIGN KEY (username1) REFERENCES Users(id),
                FOREIGN KEY (username2) REFERENCES Users(id)
            );
            ''').format(gameToAdd)
    
    admindb.commit()
    return redirect(url_for("get_admin_dashboard"))

@app.route("/delete_game/", methods = ["GET"])
def get_delete_game():
    return render_template("admin_dash_games.html")
    
@app.route("/delete_game/", methods = ["POST"])
def post_delete_game():
    admindb = get_db()
    c = get_db().cursor()

    gameToDelete = request.form.get('gamename')

    c.execute(''' 
                DROP TABLE {};    
                 ''').format(gameToDelete)

    admindb.commit()
    return redirect(url_for("get_admin_dashboard"))

@app.route("/win_loss/", methods = ["GET"])
def get_win_loss():
    changedb = get_db()
    c = get_db().cursor()

    x = 1
    data = dict()

    c.execute('''
            SELECT id FROM Users;
                ''')
    for r in c:
        data[f"{x}"] = r
        x = x + 1
        
    print(f"{data}")
    
    changedb.commit()
    return render_template("win_loss.html", data = data)

@app.route("/win_loss/", methods = ["POST"])
def change_win_loss():
    changedb = get_db()
    c = get_db().cursor()

    data = dict()
    copy = dict()

    fields = ['id', 'win', 'loss'];

    for field in fields:
        data[field] = request.form.get(field)
        print(f"{data}")

    print(f"{data}")

    c.execute(''' Update Stats
                SET wins = ?, losses = ?
                WHERE id = ?;
             ''',(data['win'], data['loss'], data['id'],))

    data.clear()
    changedb.commit()
    return redirect(url_for("change_win_loss"))

@app.route("/ban_user/", methods = ["GET"])
def get_ban_user():
    changedb = get_db()
    c = get_db().cursor()

    x = 1
    data = dict()
    copy = dict()

    fields = ['id'];

    c.execute('''
            SELECT id FROM Users;
            ''')

    for r in c:
        data[f"{x}"] = r
        x = x + 1

    print(f"{data}")
    changedb.commit()
    return render_template("ban_user.html", data = data)

@app.route("/ban_user/", methods = ["POST"])
def post_ban_user():
    changedb = get_db()
    c = get_db().cursor()

    fields = ['id'];
    data = dict()

    for field in fields:
        data[field] = request.form.get(field)

    print(f"{data}")
    c.execute(''' Delete FROM Users where id = ?;''', (data['id'],))

    changedb.commit()
    return redirect(url_for("post_ban_user"))

@app.route("/admin_dashboard_users/", methods = ["GET"])
def get_admin_user():
    return render_template("admin_dash_user.html")

@app.route("/admin_dashboard_games/", methods = ["GET"])
def get_admin_games():
    return render_template("admin_dash_games.html")

@app.route("/admin_dashboard_matches/", methods = ["GET"])
def get_admin_matches():
    return render_template("admin_dash_matches.html")

if __name__ == '__main__':
    app.run(debug=True)

conn.close()