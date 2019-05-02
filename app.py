from flask import Flask, request, redirect, url_for, render_template, session

from utils.db_func import *
from utils.general_utils import format_datetime_to_number_str, format_int_to_time
from utils.passwords import check_user

app = Flask(__name__)
app.secret_key = "secret-key"


@app.route("/login_action", methods=['POST'])
def login():
    print("Logging user in")
    username = request.form['username']
    password = request.form['password']

    print(username, password)
    if not check_user(username, password, credential_file=app.root_path + "\\secrets.json"):
        print("Invalid login")
        return redirect(url_for("login_page"))

    session['username'] = username

    return redirect(url_for('dashboard'))


@app.route("/vehicle")
def vehicle_form():
    return render_template("main.html", title="Vehicles")


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
    if not "username" in session.keys():
        return redirect(url_for("login_page"))
    user_row = get_user_info(session['username'], app.root_path + "\\secrets.json")[0]
    print(user_row)
    user = {
        'username' : user_row[0],
        'first_name' : user_row[1],
        'last_name' : user_row[2],
        'phone_on' : user_row[3],
        'manager' : user_row[4]
    }
    template_vals = {"bookings": [], "user":user}
    bookings = get_bookings_for(session['username'], app.root_path + "\\secrets.json")
    print(bookings)
    if bookings:
        first_row = bookings[0]
        template_vals['first_booking'] = {
            "date": format_datetime_to_number_str(first_row[1]),
            "start_time": format_int_to_time(first_row[-2]),
            "end_time": format_int_to_time(first_row[-1])
        }
        if len(bookings) > 1:
            for row in bookings:
                template_vals['bookings'].append({
                    "date": format_datetime_to_number_str(row[1]),
                    "start_time": format_int_to_time(row[-2]),
                    "end_time": format_int_to_time(row[-1])
                })

    print(template_vals)
    return render_template("main.html",
                           title="Dashboard",
                           page="dashboard",
                           v=template_vals)


@app.route("/licenses")
def license_page():
    return render_template("main.html",
                           title="Licenses",
                           page="licenses")


@app.route('/login')
def login_page():
    if "username" in session.keys():  # if user is logged in, redirect to dashboard
        return redirect(url_for("dashboard"))
    else:
        return render_template("gate.html", page="login")


@app.route("/register")
def register_page():
    if "username" in session.keys():  # if user is logged in, redirect to dashboard
        return redirect(url_for("dashboard"))
    else:
        return render_template("gate.html", page="register")


@app.route("/sign-out")
def sign_out():
    del session['username']  # TODO proven to work, but test session.pop("username", None)
    return redirect(url_for("login_page"))


@app.route("/plate", methods=['POST'])
def number_plate_recognition():
    pass


if __name__ == '__main__':
    app.run()
