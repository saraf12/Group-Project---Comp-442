import sqlite3
import os
import base64
import time
from datetime import datetime, timedelta
from traceback import print_exc
from cryptography.fernet import Fernet
from passlib.hash import bcrypt_sha256
from flask import Flask, render_template, request, redirect, url_for, abort, session, flash, g, jsonify, make_response
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

# c.execute('''
#             DROP TABLE IF EXISTS Stats;
#             ''')



c.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                name TEXT,
                email TEXT,
                passwordhash TEXT,
                performanceRating INTEGER DEFAULT 400,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                totGamesPlayed INTEGER DEFAULT 0,
                icon TEXT
            );
            ''')

c.execute('''
            CREATE TABLE IF NOT EXISTS UserTable (
                username TEXT PRIMARY KEY UNIQUE,
                name TEXT,
                email TEXT,
                passwordhash TEXT,
                performanceRating INTEGER DEFAULT 400,
                icon TEXT
            );
            ''')

c.execute('''
            CREATE TABLE IF NOT EXISTS Matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username1 TEXT PRIMARY KEY UNIQUE,
                username2 TEXT,
                response1 TEXT,
                response2 TEXT,
                status TEXT,
                dateCreated DATETIME NOT NULL DEFAULT(DATETIME('now')),
                FOREIGN KEY (username1) REFERENCES Users(username),
                FOREIGN KEY (username2) REFERENCES Users(username),
                FOREIGN KEY (winner) REFERENCES Users(username),
                FOREIGN KEY (loser) REFERENCES Users(username)
            );
            ''')

c.execute('''
            CREATE TABLE IF NOT EXISTS Games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            );
            ''')

c.execute('''
            CREATE TABLE IF NOT EXISTS Stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user INTEGER,
                game INTEGER,
                performanceRating INTEGER DEFAULT 400,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                totGamesPlayed INTEGER DEFAULT 0,
                FOREIGN KEY (user) REFERENCES Users(id),
                FOREIGN KEY (game) REFERENCES Games(id)
            );
            ''')
conn.commit()


# c.execute('''
#             DELETE FROM Users where id = 7;
#             ''')

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

@app.route("/register/", methods=["GET"])
def get_register():
    return render_template("registerPage.html")

@app.route("/")
@app.route("/signin/", methods=["GET"])
def get_signin():
    session['uid'] = ""
    return render_template("signInPage.html")

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
        # print("This is the email: " + str(data['email']))
        uid = c.execute('SELECT id FROM Users WHERE email=?;',(data['email'],)).fetchone()
        # print("This is the uid:" + str(uid))
        # if a user is found, then this email address is taken
        if uid is not None:
            flash("An account with this email already exists")
            return redirect(url_for("get_register"))
        uid = c.execute('SELECT id FROM Users WHERE username=?;',(data['username'],)).fetchone()
        # print("This is the uid:" + str(uid))
        # if a user is found, then this email address is taken
        if uid is not None:
            flash("An account with this username already exists")
            return redirect(url_for("get_register"))
        # otherwise add them to the database and redirect to login
        passtohash = data['password']
        # print(passtohash)
        h = hash_password(data['password'], pep)
        # print("This is val of pep in post_register:" + str(pep))
        c.execute('INSERT INTO Users (username, name, email, passwordhash, icon) VALUES (?,?,?,?,?);', 
            (data['username'], data['name'], data['email'], h, data['Iprofile']))
        regdb.commit()
        # uid = c.execute('SELECT id FROM Users WHERE email=?;',(data['email'],)).fetchone()
        # print("This is the uid after adding entry:" + str(uid))
        # savedhash = c.execute('SELECT passwordhash FROM Users WHERE id=?;',(uid[0],)).fetchone()
        # print(savedhash)
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
        # print(passwordtxt)
        password = hash_password(passwordtxt, pep)
        # print(password)
        uid = c.execute('SELECT id FROM Users WHERE username=?;',(username,)).fetchone()
        if uid is None:
            flash("Username is not associated with an account")
            return redirect(url_for("get_signin"))
        savedhash = c.execute('SELECT passwordhash FROM Users WHERE id=?;',(uid[0],)).fetchone()
        # print(savedhash)
        if uid is not None and savedhash is not None: 
            if check_password(passwordtxt, savedhash[0], pep):
                expires = datetime.utcnow()+timedelta(minutes=30)
                session['uid'] = uid[0]
                session['expires'] = expires.strftime("%Y-%m-%dT%H:%M:%SZ")
                # return f"{uid}"
                return redirect(url_for("get_main_page"))
            else:
                flash("Password is incorrect")
                return redirect(url_for("get_signin"))
    except Exception:
        flash("User does not exist")
        print_exc()
        return redirect(url_for("get_signin"))


@app.route("/mainpage/", methods=["GET"])
def get_main_page():
    curr_uid = session.get("uid")
    if curr_uid == "":
        flash("Please sign in")
        return redirect(url_for("get_signin"))
    # print(curr_uid)

    # Code attempting to implement a time frame until user is logged out
    try:
        exp = datetime.strptime(session.get("expires"), "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        exp = None
    if curr_uid is None or exp is None or exp < datetime.utcnow():
        flash("Session has expired. Please sign in again.")
        return redirect(url_for("get_signin"))

    regdb = get_db()
    c = get_db().cursor()
    profileData = dict()
    profileData['username'] = c.execute('SELECT username FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    profileData['name'] = c.execute('SELECT name FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    profileData['email'] = c.execute('SELECT email FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    profileData['icon'] = c.execute('SELECT icon FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]

    #Getting leaderboard stuff
    # UserList = "null"
    # UserList = c.execute('SELECT username, performanceRating FROM Users ORDER BY performanceRating DESC;').fetchall()
    # print(UserList[0][0])
    # print(profileData['username'])
    # print(profileData['name'])
    # print(profileData['email'])
    # print(profileData['icon'])
    # THIS icon code  WORKS!!
    # icon = c.execute('SELECT icon FROM Users WHERE id=?;', (curr_uid,)).fetchone()
    # icon = icon[0]

    # profileData = dict()
    # profilePieces = ['username', 'name', 'email', 'icon']       #need to add record stuff to this
    # temp = c.execute('SELECT ? FROM Users WHERE id=?;',(profilePieces[0], curr_uid,)).fetchone()
    # print(temp[0])
    # for field in profilePieces:
    #     holder = c.execute('SELECT ? FROM Users WHERE id=?;',(field, curr_uid,)).fetchone()
    #     print(holder)

    # print(profileData['icon'])

    #Trying to get current game value
    # print(request.form.get("game-menu"))

    #Getting all the possible games
    gameOptions = dict()
    gamesCursor = get_db().cursor()
    gamesCursor.execute('SELECT id, name FROM Games;')
    for game in gamesCursor:
        gameOptions[game[0]] = game

    #Getting leaderboard info for each game
    UserLists = dict()
    gmsCursor = get_db().cursor()
    gmsCursor.execute('SELECT id, name FROM Games;')
    for gm in gmsCursor:
        print(gm)
        UserLists[gm[0]] = c.execute('SELECT user, performanceRating FROM Stats WHERE game=? ORDER BY performanceRating DESC;', (gm[0],)).fetchall()

    print(UserLists)

    #Trying to get just the leaderboard info for one game (Snake)
    snakeLeaders = []
    snakeLeaders = c.execute('SELECT user, performanceRating FROM Stats WHERE game=1 ORDER BY performanceRating DESC;').fetchall()
    print(snakeLeaders)

    # print(gameOptions)
    return render_template("mainPage.html", profileData=profileData, UserList=UserLists, gameOptions=gameOptions)

# @app.route("/ajaxtest/", methods=["POST"])
# def post_main_page():

#     curr_uid = session.get("uid")
#     if curr_uid == "":
#         flash("Please sign in")
#         return redirect(url_for("get_signin"))
#     # print(curr_uid)

#     # Code attempting to implement a time frame until user is logged out
#     try:
#         exp = datetime.strptime(session.get("expires"), "%Y-%m-%dT%H:%M:%SZ")
#     except ValueError:
#         exp = None
#     if curr_uid is None or exp is None or exp < datetime.utcnow():
#         flash("Session has expired. Please sign in again.")
#         return redirect(url_for("get_signin"))

#     regdb = get_db()
#     c = get_db().cursor()
#     profileData = dict()
#     profileData['username'] = c.execute('SELECT username FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
#     profileData['name'] = c.execute('SELECT name FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
#     profileData['email'] = c.execute('SELECT email FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
#     profileData['icon'] = c.execute('SELECT icon FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]

#     #Getting leaderboard stuff
#     UserList = c.execute('SELECT username, performanceRating FROM Users ORDER BY performanceRating DESC;').fetchall()

#     print(UserList)
#     #Getting all the possible games
#     gameOptions = dict()
#     gamesCursor = get_db().cursor()
#     gamesCursor.execute('SELECT id, name FROM Games;')
#     for game in gamesCursor:
#         gameOptions[game[0]] = game
#     # print(gameOptions)
    

#     req = request.get_json()

#     session['currgameid'] = req.get('gameid')
#     print("This is the session variable:")
#     print(session['currgameid']) 

#     print("trying to print current game id:")
#     print(session['currgameid'])

#     # res = make_response(jsonify({"message": "JSON recieved"}), 200)

#     return render_template("declinePage.html")


@app.route("/profilepage/", methods=["GET"])
def profile_page():
    curr_uid = session.get("uid")
    if curr_uid == "":
        flash("Please sign in")
        return redirect(url_for("get_signin"))
    # print(curr_uid)
    regdb = get_db()
    c = get_db().cursor()
    profileData = dict()
    profileData['username'] = c.execute('SELECT username FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    profileData['name'] = c.execute('SELECT name FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    profileData['email'] = c.execute('SELECT email FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    profileData['performanceRating'] = c.execute('SELECT performanceRating FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    profileData['wins'] = c.execute('SELECT wins FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    profileData['losses'] = c.execute('SELECT losses FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    profileData['totGamesPlayed'] = c.execute('SELECT totGamesPlayed FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    profileData['icon'] = c.execute('SELECT icon FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]

   #Get records
    regdb.row_factory = lambda cursor, row: row[0]
    c = regdb.cursor()
    recordList = []
    matchesId = c.execute('SELECT id FROM Matches WHERE username1 =? OR username2=? ',(profileData['username'],profileData['username'],)).fetchall()
    
    for mId in matchesId:
        match = dict()
        match["id"] = mId
        match['c_username'] = profileData['username']
        resp = ""
        username1 = c.execute('SELECT username1 FROM Matches WHERE id = ?',(mId,)).fetchone()
        username2 = c.execute('SELECT username2 FROM Matches WHERE id = ?', (mId,)).fetchone()
        if(username1 == profileData['username']):
            match['user'] = 1
            match['username'] = username2
            match['icon'] = c.execute('SELECT icon FROM Users WHERE username =?', (username2,)).fetchone()
            resp = c.execute('SELECT response1 FROM Matches WHERE id=?',(mId,)).fetchone()
        else:
            match['user'] = 2
            match['username'] = username1
            match['icon'] = c.execute('SELECT icon FROM Users WHERE username =?', (username1,)).fetchone()
            resp = c.execute('SELECT response2 FROM Matches WHERE id=?',(mId,)).fetchone()

        if(resp == None):
            match['response'] = 0
        else:
            match['response'] = 1
        recordList.append(match)


    return render_template("profilePage.html", profileData=profileData, records = recordList)



@app.route("/profilepage/", methods=["POST"])
def updaterecord():
    matchId = request.form['matchId']
    name = "result" + str(matchId)
    r = request.form.getlist('result')
    user = int(request.form['user'])
    regdb = get_db()
    c = get_db().cursor()
    c.execute('UPDATE Matches SET response1 =? WHERE id =?;',("Done", 1))
    if len(r) > 0:
        result = r[0]
        if(user == 1):
            c.execute('UPDATE Matches SET response1 =? WHERE id =?;',(result, matchId))
        else:
            c.execute('UPDATE Matches SET response2 =? WHERE id =?;',(result, matchId))
    #print(len(r))
    regdb.commit()
    return redirect(url_for("profile_page"))


@app.route("/editprofile/", methods=["GET"])
def get_edit_profile_page():
     # get info to prefill fields
    curr_uid = session.get("uid")
    if curr_uid == "":
        flash("Please sign in")
        return redirect(url_for("get_signin"))
    regdb = get_db()
    c = get_db().cursor()
    profileData = dict()
    profileData['username'] = c.execute('SELECT username FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    profileData['name'] = c.execute('SELECT name FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    # print(profileData['name'])
    profileData['email'] = c.execute('SELECT email FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    profileData['icon'] = c.execute('SELECT icon FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    return render_template("editProfile.html", profileData=profileData)


@app.route("/editprofile/", methods=["POST"])
def post_edit_profile_page():
    curr_uid = session.get("uid")
    regdb = get_db()
    c = get_db().cursor()
    data = dict()
    fields = ['username', 'name', 'email', 'password', 'confirm-password', 'Iprofile']
    for field in fields:
        data[field] = request.form.get(field)
    # print(data['password'])
    valid = True
    if valid and data['password'] != "":
        if len(data['password']) < 8:
            valid = False
            flash("password must be at least 8 characters")
    if valid and data['password'] != data['confirm-password']:
        valid = False
        flash("password and confirm password must match")
    if valid:
        # session['email'] = data['email']
        #print("This is the email: " + str(data['email']))
        uid = c.execute('SELECT id FROM Users WHERE email=?;',(data['email'],)).fetchone()
       # print("This is the uid:" + str(uid))
        #if a user is found, then this email address is taken
        # otherwise add them to the database and redirect to login
        if data['password'] != "":
            passtohash = data['password']
            # print(passtohash)
            h = hash_password(data['password'], pep)
            c.execute('UPDATE Users SET passwordhash = ? WHERE id = ?;', (h, curr_uid))
            # c.execute('INSERT INTO Users (passwordhash) VALUES(?) WHERE id=?;',
            # (h, curr_uid))
        #print("This is val of pep in post_register:" + str(pep))
        if data['username'] != "":
            c.execute('UPDATE Users SET username = ? WHERE id = ?;', (data['username'], curr_uid))
            # c.execute('INSERT INTO Users (username) VALUES(?) WHERE id=?;',
            # (data['username'], curr_uid))
        if data['name'] != "":
            c.execute('UPDATE Users SET name = ? WHERE id = ?;', (data['name'], curr_uid))
            # c.execute('INSERT INTO Users (name) VALUES(?) WHERE id=?;',
            # (data['name'], curr_uid))
        currColor = c.execute('SELECT icon FROM Users WHERE id=?;',(curr_uid,)).fetchone()
        if data['Iprofile'] != currColor:
            c.execute('UPDATE Users SET icon = ? WHERE id = ?;', (data['Iprofile'], curr_uid))
        regdb.commit()
        # uid = c.execute('SELECT id FROM Users WHERE email=?;',(data['email'],)).fetchone()
        # print("This is the uid after adding entry:" + str(uid))
        # savedhash = c.execute('SELECT passwordhash FROM Users WHERE id=?;',(uid[0],)).fetchone()
        # print(savedhash)
        return redirect(url_for("profile_page"))
    else:
        return redirect(url_for("get_edit_profile_page"))


@app.route("/matchup/", methods=["GET"])
def get_matchup_window():
    curr_uid = session.get("uid")
    if curr_uid == "":
        flash("Please sign in")
        return redirect(url_for("get_signin"))
    regdb = get_db()
    c = get_db().cursor()
    currUserData = dict()

    currUserData['username'] = c.execute('SELECT username FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    currUserData['name'] = c.execute('SELECT name FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    currUserData['performanceRating'] = c.execute('SELECT performanceRating FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    currUserData['email'] = c.execute('SELECT email FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    currUserData['icon'] = c.execute('SELECT icon FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]

    lowerLimit = currUserData['performanceRating'] - 200
    upperLimit = currUserData['performanceRating'] + 200

    opponentData = c.execute('SELECT username, email, performanceRating FROM Users WHERE performanceRating >= ? AND performanceRating <= ? AND NOT id=? ORDER BY RANDOM() LIMIT 1;', 
        (lowerLimit, upperLimit, curr_uid,)).fetchone()
    # print(opponentData[0])
    

    return render_template("matchup.html", currUserData=currUserData, opponentData=opponentData)

@app.route("/matchaccepted/", methods=["POST"])
def post_matchup_window_accept():
    curr_uid = session.get("uid")
    if curr_uid == "":
        flash("Please sign in")
        return redirect(url_for("get_signin"))
    regdb = get_db()
    c = get_db().cursor()
    currentUsername = request.form.get('current-username')
    opponentUsername = request.form.get('opponent-username')
    c.execute('INSERT INTO Matches (username1, username2) VALUES (?,?);', 
            (currentUsername, opponentUsername,))
    regdb.commit()
    return redirect(url_for("match_accepted"))

@app.route("/matchdeclined/", methods=["POST"])
def post_matchup_window_decline():
    return redirect(url_for("match_declined"))

@app.route("/acceptconfirmation/", methods=["GET"])
def match_accepted():
    return render_template("acceptPage.html")

@app.route("/declineconfirmation/", methods=["GET"])
def match_declined():
    return render_template("declinePage.html")



    