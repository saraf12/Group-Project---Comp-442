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

# c.execute('''
#             DROP TABLE IF EXISTS Games;
#             ''')



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
            CREATE TABLE IF NOT EXISTS TicTacToe (
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
            ''')

c.execute('''
            CREATE TABLE IF NOT EXISTS MarioKart (
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

# c.execute('''
#             INSERT INTO Games (name) VALUES ("MarioKart");
#             ''')

# c.execute('''
#             DELETE FROM Games where id = 1 or id = 2;
#             ''')

# c.execute('''
#             UPDATE TicTacToe SET status="Requested" WHERE id=1;
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
            (data['username'], data['name'], data['email'], h, data['Iprofile']))
        regdb.commit()

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

        password = hash_password(passwordtxt, pep)

        uid = c.execute('SELECT id FROM Users WHERE username=?;',(username,)).fetchone()
        if uid is None:
            flash("Username is not associated with an account")
            return redirect(url_for("get_signin"))
        savedhash = c.execute('SELECT passwordhash FROM Users WHERE id=?;',(uid[0],)).fetchone()

        if uid is not None and savedhash is not None: 
            if check_password(passwordtxt, savedhash[0], pep):
                expires = datetime.utcnow()+timedelta(minutes=30)
                session['uid'] = uid[0]
                session['expires'] = expires.strftime("%Y-%m-%dT%H:%M:%SZ")
                return redirect(url_for("get_main_page"))
            else:
                flash("Password is incorrect")
                return redirect(url_for("get_signin"))
    except Exception:
        flash("User does not exist")
        print_exc()
        return redirect(url_for("get_signin"))

@app.route("/")
@app.route("/mainpage/", methods=["GET"])
def get_main_page():
    curr_uid = session.get("uid")
    if curr_uid == "":
        flash("Please sign in")
        return redirect(url_for("get_signin"))

    # Code implementing a time frame until user is logged out
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

    #Getting all the possible games
    gameOptions = dict()
    gamesCursor = get_db().cursor()
    gamesinDB = gamesCursor.execute('SELECT id, name FROM Games;').fetchall()
    for game in gamesinDB:
        gameOptions[game[0]] = game
    
    # Getting leaderboard info for each game
    UserLists = dict()
    gmsCursor = get_db().cursor()
    allgms = gmsCursor.execute('SELECT id, name FROM Games;').fetchall()
    for gm in allgms:
        UserLists[gm[0]] = c.execute('''SELECT username, performanceRating FROM Stats JOIN Users ON Users.id=Stats.user WHERE game=? 
                   ORDER BY performanceRating DESC;''', (gm[0],)).fetchall()

    regdb.commit()
    return render_template("mainPage.html", profileData=profileData, UserList=UserLists, gameOptions=gameOptions)


@app.route("/profilepage/", methods=["GET"])
def profile_page():
    curr_uid = session.get("uid")
    if curr_uid == "":
        flash("Please sign in")
        return redirect(url_for("get_signin"))

    regdb = get_db()
    c = get_db().cursor()
    profileData = dict()
    profileData['username'] = c.execute('SELECT username FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    profileData['name'] = c.execute('SELECT name FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    profileData['email'] = c.execute('SELECT email FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    profileData['icon'] = c.execute('SELECT icon FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]

   #Get records
    regdb.row_factory = lambda cursor, row: row[0]
    c = regdb.cursor()
    
    # NOTE: Need to change this get it from all games tables
    gamesRecords = dict()
    gameStats = dict()
    #For each game get Game name 
    gamesName = c.execute('SELECT name FROM Games').fetchall()

    for game in gamesName:

        #for Get records from each match
        matchesId = c.execute('SELECT id FROM {} WHERE username1 =? OR username2=?'.format(game),
                    (profileData['username'],profileData['username'],)).fetchall()
        recordList = []
        for mId in matchesId:
            match = dict()
            #match["game"] = game
            match["id"] = mId
            match['c_username'] = profileData['username']
            resp = ""
            username1 = c.execute('SELECT username1 FROM {} WHERE id = ?'.format(game),(mId,)).fetchone()
            username2 = c.execute('SELECT username2 FROM {} WHERE id = ?'.format(game), (mId,)).fetchone()
            if(username1 == profileData['username']):
                match['user'] = 1
                match['username'] = username2
                match['icon'] = c.execute('SELECT icon FROM Users WHERE username =?', (username2,)).fetchone()
                resp = c.execute('SELECT winnerAccordingToU1 FROM {} WHERE id=?'.format(game),(mId,)).fetchone()
            else:
                match['user'] = 2
                match['username'] = username1
                match['icon'] = c.execute('SELECT icon FROM Users WHERE username =?', (username1,)).fetchone()
                resp = c.execute('SELECT winnerAccordingToU2 FROM {} WHERE id=?'.format(game),(mId,)).fetchone()

            if(resp == None):
                match['response'] = 0
            else:
                match['response'] = 1
            recordList.append(match)
        gamesRecords[game] = recordList
        
        #Get player state per game
        stats = dict()
        gameID = c.execute('SELECT id FROM Games WHERE name=?',(game,)).fetchone()
        stats["performance"] = c.execute('SELECT performanceRating FROM Stats WHERE user=? AND game=?',(curr_uid,gameID,)).fetchone()
        stats["wins"] = c.execute('SELECT wins FROM Stats WHERE user=? AND game=?',(curr_uid,gameID,)).fetchone()
        stats["losses"] = c.execute('SELECT losses FROM Stats WHERE user=? AND game=?',(curr_uid,gameID,)).fetchone()
        gameStats[game] = stats

    return render_template("profile.html", profileData=profileData,gameStats=gameStats, gamesRecords = gamesRecords, gameslst = gamesName)



@app.route("/profilepage/", methods=["POST"])
def updaterecord():
    game = request.form['game']
    matchId = request.form['matchId']
    name = "result" + str(matchId)
    r = request.form.getlist('result')
    user = int(request.form['user'])
    regdb = get_db()
    c = get_db().cursor()
    #c.execute('UPDATE {} SET winnerAccordingToU1 =? WHERE id =?;'.format(game),("Done", 1))
    if len(r) > 0:
        result = r[0]
        if(user == 1):
            c.execute('UPDATE {} SET winnerAccordingToU1 =? WHERE id =?;'.format(game),(result, matchId))
        else:
            c.execute('UPDATE {} SET winnerAccordingToU2 =? WHERE id =?;'.format(game),(result, matchId))

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
    valid = True
    if valid and data['password'] != "":
        if len(data['password']) < 8:
            valid = False
            flash("password must be at least 8 characters")
    if valid and data['password'] != data['confirm-password']:
        valid = False
        flash("password and confirm password must match")
    if valid:
        uid = c.execute('SELECT id FROM Users WHERE email=?;',(data['email'],)).fetchone()
        #if a user is found, then this email address is taken
        # otherwise add them to the database and redirect to login
        if data['password'] != "":
            passtohash = data['password']
            h = hash_password(data['password'], pep)
            c.execute('UPDATE Users SET passwordhash = ? WHERE id = ?;', (h, curr_uid))
        if data['username'] != "":
            c.execute('UPDATE Users SET username = ? WHERE id = ?;', (data['username'], curr_uid))
        if data['name'] != "":
            c.execute('UPDATE Users SET name = ? WHERE id = ?;', (data['name'], curr_uid))
        currColor = c.execute('SELECT icon FROM Users WHERE id=?;',(curr_uid,)).fetchone()
        if data['Iprofile'] != currColor:
            c.execute('UPDATE Users SET icon = ? WHERE id = ?;', (data['Iprofile'], curr_uid))
        regdb.commit()
        return redirect(url_for("profile_page"))
    else:
        return redirect(url_for("get_edit_profile_page"))


@app.route("/matchup/<int:gametype>", methods=["GET"])
def get_matchup_window(gametype):
    curr_uid = session.get("uid")
    if curr_uid == "":
        flash("Please sign in")
        return redirect(url_for("get_signin"))
    regdb = get_db()
    c = get_db().cursor()
    currUserData = dict()

    currUserData['username'] = c.execute('SELECT username FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    currUserData['name'] = c.execute('SELECT name FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    currUserData['email'] = c.execute('SELECT email FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]
    currUserData['icon'] = c.execute('SELECT icon FROM Users WHERE id=?;', (curr_uid,)).fetchone()[0]

    # Code to get the current user's performance rating
    currUserData['performanceRating'] = c.execute('''SELECT performanceRating 
                                                    FROM Stats
                                                    WHERE user=? and game=?;''',
                                                    (curr_uid, gametype,)).fetchone()[0]

    lowerLimit = currUserData['performanceRating'] - 200
    upperLimit = currUserData['performanceRating'] + 200

    opponentData = c.execute('''SELECT username, email, performanceRating 
                                FROM Stats JOIN Users ON Stats.user=Users.id
                                WHERE performanceRating>=? AND performanceRating<=?
                                AND NOT Stats.user=? 
                                ORDER BY RANDOM() LIMIT 1;''',
                                (lowerLimit, upperLimit, curr_uid,)).fetchone()

    return render_template("matchup.html", currUserData=currUserData, opponentData=opponentData, gametype=gametype)

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

    # Code to insert match data into appropriate table
    gametype = request.form.get('gametype')

    gameTableName = c.execute('SELECT name FROM Games where id=?', (gametype,)).fetchone()[0]

    c.execute('INSERT INTO {} (username1, username2, status) VALUES (?,?,?);'.format(gameTableName),
                    (currentUsername, opponentUsername, "Requested",))

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

@app.route("/inbox/", methods=["GET"])
def get_inbox():
    curr_uid = session.get("uid")
    if curr_uid == "":
        flash("Please sign in")
        return redirect(url_for("get_signin"))
    regdb = get_db()
    c = get_db().cursor()

    currUsername = c.execute('SELECT username FROM Users WHERE id=?',(curr_uid,)).fetchone()[0]

    requestedGames = dict()
    requesterOfGames = dict()

    allTypesOfGames = c.execute('SELECT id, name FROM Games;').fetchall()

    for game in allTypesOfGames:
        gamesWithUserAsRequester = c.execute('SELECT id, username2, dateCreated, status FROM {} WHERE username1=?;'.format(game[1]),
                    (currUsername,)).fetchall()
        i = 0
        for gm in gamesWithUserAsRequester:
            requesterOfGames[i] = (game[1], gm)
            i = i+1
        gamesWithUserAsResponder = c.execute('SELECT id, username1, dateCreated FROM {} WHERE username2=? AND status=\"Requested\";'.format(game[1]),
                    (currUsername,)).fetchall()
        for gm in gamesWithUserAsResponder:
            requestedGames[i] = (game[1], gm)
            i = i+1   

    return render_template("inbox.html", requestedGames=requestedGames, requesterOfGames=requesterOfGames)


@app.route("/inbox/", methods=["POST"])
def post_inbox():
    curr_uid = session.get("uid")
    if curr_uid == "":
        flash("Please sign in")
        return redirect(url_for("get_signin"))
    regdb = get_db()
    c = get_db().cursor()

    if request.form.get('submit-btn') == "accept":
        gameId = request.form.get('gameid')
        gameTable = request.form.get('gametable')
        c.execute('UPDATE {} SET status=\"Confirmed\" WHERE id=?'.format(gameTable),(gameId,))
    
    if request.form.get('submit-btn') == "decline":
        gameId = request.form.get('gameid')
        gameTable = request.form.get('gametable')
        # ASK Sydney if she would rather a declined match be removed from the database
        # but it might be good to keep it in as declined, so that you can let the other person know it was declined
        c.execute('UPDATE {} SET status=\"Declined\" WHERE id=?'.format(gameTable),(gameId,))
    
    regdb.commit()

    return redirect(url_for("get_inbox"))



    