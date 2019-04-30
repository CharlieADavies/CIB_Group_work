from flask import Flask, request, redirect, url_for, render_template, session
from utils.passwords import check_user

app = Flask(__name__)
app.secret_key = "secret-key"


@app.route("/login_action", methods=['POST'])
def login():
    print("Logging user in")
    username = request.form['username']
    password = request.form['password']
    print(username,password)
    if not check_user(username, password):
        print("Invalid login")
        return redirect(url_for("login_page"))
    session['username'] = username
    return redirect(url_for('dashboard'))


@app.route('/')
def dashboard():
    if "username" in session.keys():
        print(session)
        render_template("main.html")


@app.route('/login')
def login_page():
    return render_template("login.html")


if __name__ == '__main__':
    app.run()
