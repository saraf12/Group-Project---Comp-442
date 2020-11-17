from flask import Flask, render_template, request, session,redirect, url_for, flash

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["SECRET_KEY"] = "correcthorsebatterystaple"

@app.route("/register/")
def post_register():
    return 0