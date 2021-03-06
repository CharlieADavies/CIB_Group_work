from flask import Flask, request, redirect, url_for, render_template, session
from utils.db_func import *
from utils.general_utils import *
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
    return render_template("vehicle.html", title="Vehicles", v={})


@app.route("/vehicle_f", methods=['POST'])
def process_vehicle_form():
    print("New vehicle registered")
    username = session['username']
    print(request.form)
    is_electric = False
    reg = request.form['reg']
    make = request.form['make']
    if insert_vehicle(username, is_electric, reg, make, credential_file=app.root_path + "\\secrets.json"):
        print("FFF")
        return redirect(url_for("dashboard"))
    else:
        print("AAA")
        return redirect(url_for("vehicle_form"))


@app.route('/')
def dashboard():
    if "username" not in session.keys():
        return redirect(url_for("login_page"))
    user_row = get_user_info(session['username'], app.root_path + "\\secrets.json")[0]
    user = {
        'username': user_row[0],
        'first_name': user_row[1],
        'last_name': user_row[2],
        'phone_on': user_row[3],
        'manager': user_row[4]
    }
    template_vals = {"bookings": [], "user": user, 'park_and_ride_dates': []}
    bookings = get_bookings_for(session['username'], app.root_path + "\\secrets.json")
    if bookings:
        first_row = bookings[0]
        for p_r in first_row[3:7]:
            template_vals['park_and_ride_dates'].append(
                {'start': formate_datetime_to_string_str(p_r),
                 'end': formate_datetime_to_string_str(p_r + timedelta(days=7))}
            )

        template_vals['first_booking'] = {
            "date": format_datetime_to_number_str(first_row[1]),
            "start_time": format_int_to_time(first_row[-2]),
            "end_time": format_int_to_time(first_row[-1])
        }
        template_vals['colour'] = first_row[2]
        if len(bookings) > 1:
            for row in bookings:
                template_vals['bookings'].append({
                    "date": format_datetime_to_number_str(row[1]),
                    "start_time": format_int_to_time(row[-2]),
                    "end_time": format_int_to_time(row[-1])
                })

    return render_template("main.html",
                           title="Dashboard",
                           page="dashboard",
                           v=template_vals)


@app.route("/licenses")
def license_page():
    return render_template("main.html",
                           title="Licenses",
                           page="licenses")


@app.route("/manager_action")
def set_manager_form():
    try:
        manager= request.form['manager']
        set_manager(session['username'], manager)
        return redirect(url_for("dashboard"))
    except:
        return redirect(url_for("dashboard"))


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
