from flask import Flask, request, redirect, url_for, render_template
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
        return redirect(url_for('invalid_login'))
    return redirect(url_for('home'))


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login')
def login_page():
    return render_template("login.html")


if __name__ == '__main__':
    app.run()
