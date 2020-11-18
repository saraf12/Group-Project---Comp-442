import sqlite3
import os
import base64
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
            CREATE TABLE Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                fname TEXT,
                lname TEXT,
                email TEXT,
                passwordhash TEXT,
                performanceRating INTEGER,
                wins INTEGER,
                losses INTEGER
            );
            ''')

conn.commit()

@app.route("/register/", methods=['POST'])
def post_register():
    #Get all data from the from
    data = dict()
    fields = ["username", "name","email", "password"]
    for field in fields:
        data[field] = request.form.get(field)
    session["email"] = data["email"]
    return redirect(url_for("get_register"))

@app.route("/register/", methods=["GET"])
def get_register():
    return render_template("signInPage.html")