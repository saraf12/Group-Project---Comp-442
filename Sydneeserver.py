from flask import Flask, render_template, request, session,redirect, url_for, flash

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["SECRET_KEY"] = "correcthorsebatterystaple"


@app.route("/register/", methods=['POST'])
def post_register():
    # first get all the data from the form
    data = dict()
    fields = ["username","name","email", "password","confirm-password"]
    for field in fields:
        data[field] = request.form.get(field)
    # #next make sure the user submitted something for all required fields
    valid = True
    for field in fields:
        if data[field] is None or data[field] == "":
            valid = False
            flash(f"{field} cannot be blank")
    if valid and len(data["password"]) < 8:
        valid = False
        flash("Password must be at least 8 characters")
    if valid and data["password"] != data["confirm-password"]:
        valid = False
        flash("password and confirm password must match")
    #return accordingly
    if valid:
        #report data back to SQL
        session["email"] = data["email"]
        return redirect(url_for("get_register"))
    else:
        return render_template("registerPage.html")

@app.route("/home/", methods=["GET"])
def get_register():
    #email = session.get("email")
    return render_template("mainPage.html")