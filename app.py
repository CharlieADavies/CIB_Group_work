from flask import Flask, request

app = Flask(__name__)
app.secret_key = "secret-key"

@app.route("/login")
def login():
    username = request.form['username']
    password = request.form['password']
    # TODO add the database function that verifies stuff here


@app.route('/')
def dashboard():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
