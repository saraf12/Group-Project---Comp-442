import sqlite3
import os
import base64
import time
from datetime import datetime, timedelta
from traceback import print_exc
#from cryptography.fernet import Fernet
#from passlib.hash import bcrypt_sha256
from flask import Flask, render_template, request, redirect, url_for, abort, session, flash, g, jsonify, make_response
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["SECRET_KEY"] = "correcthorsebatterystaple"

scriptdir = os.path.dirname(__file__)

dbpath = os.path.join(scriptdir, "Jed.sqlite3")

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
            CREATE TABLE IF NOT EXISTS Games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            );
            ''')

conn.commit()

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

#22222~~~~~
@app.route("/admin/", methods = ["GET"])
def get_admin():
    return render_template("admin.html")

#33333~~~~~
@app.route("/admin/", methods = ["POST"])
def post_admin():
    admindb = get_db()
    c = get_db().cursor()

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
    return render_template("blank_main.html")

def create_games_table(conn):
    c = conn.cursor()

    r = c.execute('''
    
                     ''')

    conn.commit()

if __name__ == '__main__':
    app.run(debug=True)

create_games_table(conn)

conn.close()