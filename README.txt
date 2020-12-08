~~~ Group-Project---Comp-442 -- User Testing ~~~
Group Member:
    Sydnee Charles
    Tirzah Lloyd 
    Jedidiah Madubuko

Overview:
    Website matches up opponents who want to play a particular game.  
    The actual nature of the game doesn’t matter because the website does not host the game, 
    but only creates the matchups for players who are seeking an opponent.  
    We include functionality that lets users specify which game they would like to play, 
    and they would only be matched up with other players of about the same level. 
    The website will pair up players and let them record the result after the game is played. 
    The players are also free to accept or decline a matchup.

How to run website:
    -set FLASK_APP=integratedServer.py
    -python -m flask run

Software to install to be able to run the program:
        -flask
        -flask_mail
        -passlib
        -cryptography
        -traceback
        -datetime
    

-User signin using http://localhost:5000/signin/ or choose to create an account

Existing users that can be used for testing purposes:
username: gamer2000, password: letsplay
username: highscorer18, password: playagame
username: blade750, password: herewego

To access admin side:
-Type "admin" into username field of regular signin page, leave password blank, and hit submit
-At login page use these credentials:
username: theboss, password: incontrol

Quirk about adding games: the game name must include no spaces!!