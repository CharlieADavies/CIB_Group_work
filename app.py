from flask import Flask, request, redirect, url_for, render_template, session
from utils.passwords import check_user
from utils.db_func import *  # add_vehicle

app = Flask(__name__)
app.secret_key = "secret-key"


@app.route("/login_action", methods=['POST'])
def login():
    print("Logging user in")
    username = request.form['username']
    password = request.form['password']
    print(username, password)
    if not check_user(username, password):
        print("Invalid login")
        return redirect(url_for("login_page"))
    session['username'] = username
    return redirect(url_for('dashboard'))


@app.route("/vehicle")
def vehicle_form():
    return render_template("main.html")


@app.route("/vehicle_f", methods=['POST'])
def process_vehicle_form():
    username = session['username']
    is_electric = request.form['electric']
    reg = request.form['reg']
    badge = request.form['blue_badge']


@app.route('/')
def dashboard():
    if "username" in session.keys():
        print(session)
        render_template("main.html")


@app.route('/login')
def login_page():
    return render_template("gate.html", type="login")


@app.route("/register")
def register():
    return render_template("gate.html", type="register")


if __name__ == '__main__':
    app.run()
