from flask import Flask, request, redirect, url_for, render_template, session

from utils.db_func import *
from utils.passwords import check_user

app = Flask(__name__)
app.secret_key = "secret-key"


@app.route("/login_action", methods=['POST'])
def login():
    print("Logging user in")

    username = request.form['username']
    password = request.form['password']

    print(username, password)
    if not check_user(username, password, credential_file="secrets.json"):
        print("Invalid login")
        return redirect(url_for("login_page"))

    session['username'] = username

    return redirect(url_for('dashboard'))


@app.route("/vehicle")
def vehicle_form():
    # TODO add main content
    return render_template("main.html",
                           title="Vehicles")


@app.route("/vehicle_f", methods=['POST'])
def process_vehicle_form():
    username = session['username']
    is_electric = request.form['electric']
    reg = request.form['reg']
    badge = request.form['blue_badge']
    if insert_vehicle(username, is_electric, reg, badge):
        return redirect(url_for("dashboard_page"))
    else:
        return redirect(url_for("vehicle_form"))


@app.route('/')
def dashboard():
    if "username" in session.keys():
        print(session)
        return render_template("main.html",
                               title="Dashboard",
                               type="dashboard")
    else:
        return redirect(url_for("login_page"))


@app.route("/licenses")
def license_page():
    return render_template("main.html",
                           title="Licenses",
                           type="licenses")


@app.route('/login')
def login_page():
    return render_template("gate.html", type="login")


@app.route("/register")
def register_page():
    return render_template("gate.html", type="register")


@app.route("/plate", methods=['POST'])
def number_plate_recognition():
    pass


if __name__ == '__main__':
    app.run()

