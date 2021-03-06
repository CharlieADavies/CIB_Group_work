import tkinter as tk
from datetime import time, datetime
from tkinter import font as tkfont
from tkinter import ttk, PhotoImage
import utils.passwords
import utils.account_details
import tkinter_code.calander_

from PIL import ImageTk, Image
import os
from tkcalendar import Calendar
import utils.register
import utils.db_func
import utils.db_init
import utils.date_select_logic

file_path = "../secrets.json"

class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=20, weight="bold")
        self.label_font = tkfont.Font(family='Helvetica', size=15)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        window_manager = tk.Frame(self)
        window_manager.pack(side="top", fill="both", expand=True)
        window_manager.grid_rowconfigure(0, weight=1)
        window_manager.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for pages in (
        LoginScreen, RegistrationForm, BookingScreen, SubmissionPage, DashboardUser, DashboardManager, AccountDetails):
            page_name = pages.__name__
            frame = pages(parent=window_manager, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.switch_frame("LoginScreen")
        self.title("Herbie")
        self.geometry("1500x500")

    def switch_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        frame.update()
        frame.event_generate("<<ShowFrame>>")


class LoginScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self, text="Please Login", font=controller.title_font).pack()

        username_label = tk.Label(self, text="Username: ", font=controller.label_font).pack()
        self.username_text = tk.StringVar()
        username_entry = tk.Entry(self, textvariable=self.username_text).pack()

        password_label = tk.Label(self, text="Password: ", font=controller.label_font).pack()
        self.password_text = tk.StringVar()
        password_entry = tk.Entry(self, show="*", textvariable=self.password_text).pack()

        login_button = tk.Button(self, text="Login", command=self.login_click, font=controller.label_font).pack()

        register_button = tk.Button(self, text="Registration",
                                    command=lambda: controller.switch_frame("RegistrationForm"),
                                    font=controller.title_font, pady=5).pack()
        self.user = ""

    def write_username(self, f="user.txt", user=None):
        with open(f, "w") as f:
            f.write(user)

    def login_click(self):
        # in empty "" enter your secretes.json file path.
        # eg. ardra.denford@yahoo.co.uk, VYq0X718mm for username and password
        can_login = utils.passwords.check_user(
            self.username_text.get(), self.password_text.get(), file_path)
        if can_login is True:
            self.write_username("user.txt", self.username_text.get())
            self.controller.switch_frame("DashboardManager")
        else:
            # Wrong details entered.
            print("Wrong details entered")


class AccountDetails(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self, text="Account Details", font=controller.title_font).grid(column=2, row=1)
        self.username_text = tk.StringVar()
        self.username_text.set("Username: ")
        username_label = tk.Label(self, textvariable=self.username_text, font=controller.label_font).grid(column=1,
                                                                                                          row=2)

        self.first_name_text = tk.StringVar()
        self.first_name_text.set("First name: ")
        first_name_Label = tk.Label(self, textvariable=self.first_name_text, font=controller.label_font).grid(column=1,
                                                                                                              row=3)

        self.last_name_text = tk.StringVar()
        self.last_name_text.set("Last Name: ")
        last_name_Label = tk.Label(self, textvariable=self.last_name_text, font=controller.label_font).grid(column=1,
                                                                                                            row=4)

        self.phone_number_text = tk.StringVar()
        self.phone_number_text.set("Phone Number: ")
        Phone_number = tk.Label(self, textvariable=self.phone_number_text, font=controller.label_font).grid(column=1,
                                                                                                            row=5)

        self.address_text = tk.StringVar()
        self.address_text.set("Address: ")
        Address_Label = tk.Label(self, textvariable=self.address_text, font=controller.label_font).grid(column=1, row=6)

        self.postcode_text = tk.StringVar()
        self.postcode_text.set("Post code: ")
        postcode_Label = tk.Label(self, textvariable=self.postcode_text, font=controller.label_font).grid(column=1,
                                                                                                          row=7)

        self.role_text = tk.StringVar()
        self.role_text.set("Role: Pending")
        role_Label = tk.Label(self, textvariable=self.role_text, font=controller.label_font).grid(column=1, row=8)

        self.employee_number_text = tk.StringVar()
        self.employee_number_text.set("Employee number: ")
        employee_number_Label = tk.Label(self, textvariable=self.employee_number_text, font=controller.label_font).grid(
            column=1, row=9)

        self.badge_text = tk.StringVar()
        self.badge_text.set("badge: ")
        badge_Label = tk.Label(self, textvariable=self.badge_text, font=controller.label_font).grid(column=1, row=10)

        self.has_blue_badge_text = tk.StringVar()
        self.has_blue_badge_text.set("Blue Badge: ")
        has_blue_badge_Label = tk.Label(self, textvariable=self.has_blue_badge_text, font=controller.label_font).grid(
            column=1, row=11)

        self.vehicle_reg_text = tk.StringVar()
        vehicle_reg = tk.Label(self, textvariable=self.vehicle_reg_text, font=controller.label_font).grid(column=3, row=2)

        self.vehicle_make_text = tk.StringVar()
        vechicle_make = tk.Label(self, textvariable=self.vehicle_make_text, font=controller.label_font).grid(column=3, row=3)

        self.bind("<<ShowFrame>>", self.on_show_frame)

    def on_show_frame(self, event):
        creds = utils.db_init.load_credentials(file_path)
        connect_sql = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
        reg = ""
        sql = "SELECT * FROM " + "vehicles"
        cursor = connect_sql.cursor()
        cursor.execute(sql)
        reg_records = cursor.fetchall()
        reg = []
        car_make = []
        for reg_record in reg_records:
            if reg_record[0] == read_user_file("user.txt"):
                reg.append(reg_record[2])
                car_make.append(reg_record[3])
        self.vehicle_make_text.set("Car make:" + str(car_make))
        self.vehicle_reg_text.set("Car reg:" + str(reg))

        dash_type = role()
        image = Image.open("Logo.png")
        image = image.resize((150, 75), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        artwork = tk.Button(self, command=lambda: self.controller.switch_frame(dash_type), image=image)
        artwork.photo = image
        artwork.grid(column=1, row=1)
        self.account_logic()

    def account_logic(self):
        account_details = utils.account_details.AccountDetails(read_user_file("user.txt"), file_path)

        # jacob.smith@gmail.com, password
        details = account_details.get_user_details()
        self.username_text.set("Username: " + str(details[0]))
        self.first_name_text.set("First name: " + str(details[2]))
        self.last_name_text.set("Last name: " + str(details[3]))
        self.phone_number_text.set("Phone Number: " + str(details[4]))
        self.address_text.set("Address: " + str(details[5]))
        self.postcode_text.set("Post Code: " + str(details[6]))
        self.role_text.set("Roles: " + str(details[7]))
        self.employee_number_text.set("Employee Number: " + str(details[8]))
        self.badge_text.set("Badge: " + str(details[9]))
        self.has_blue_badge_text.set("Blue Badge: " + str(details[10]))


def role():
    username_local = read_user_file("user.txt")
    details = utils.account_details.AccountDetails(username_local, file_path)
    user_details = details.get_user_details()
    role = user_details[7]
    print(role)
    dash = ""
    if role == "Manager":
        dash = "DashboardManager"
    elif role == "Facilities":
        dash = "DashboardFacilities"
    elif role == "Employee":
        dash = "DashboardUser"
    elif role == "System Administrator":
        dash = "DashboardSysAdmin"
    return dash


def read_user_file(file):
    with open(file, "r+") as f:
        username = f.read()
    return username


class BookingScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        image = Image.open("herbie_logo.png")
        image = image.resize((150, 75), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        #command=lambda: controller.switch_frame("Dashboard")
        artwork = tk.Label(self, image=image)
        artwork.photo = image
        artwork.grid(column=1, row=1)

        control = tkinter_code.calander_.Control(self)
        title = tk.Label(self, text="Bookings", font=controller.title_font).place(x="1300", y=350)


        line = tk.Frame(self, height=3, width=1200, bg="black").place(x="0", y="80")
        self.bind("<<ShowFrame>>", self.on_show_frame)

    @staticmethod
    def read_file(file):
        with open(file, "r+") as f:
            username = f.read()
        return username

    def on_show_frame(self, event):

        dash_type = role()
        dashboard_btn = tk.Button(self, text="Click here to go back",
                                  command=lambda: self.controller.switch_frame(dash_type), width=20, height=2).grid(column=3,
                                                                                                               row=1)

        subframe_2 = tk.Frame(self, height="275", width="500", relief="raised", pady=5, borderwidth=2)
        subframe_2.place(x="620", y="160")
        line_2 = tk.Frame(self, height=30, width=500, bg="#16dace").place(x="620", y="160")

        image_2 = Image.open("Default_picture.png")
        image_2 = image_2.resize((150, 150), Image.ANTIALIAS)
        image_2 = ImageTk.PhotoImage(image_2)
        artwork_2 = tk.Label(self, image=image_2)
        artwork_2.photo = image_2
        artwork_2.place(x="940", y="265")
        ad = utils.account_details.AccountDetails(self.read_file("user.txt"),
                                                  file_path)
        user = ad.get_user_details()
        first_name = user[2]
        last_name = user[3]
        full_name = first_name + " " + last_name

        name_label = tk.Label(self, text=(full_name), font=self.controller.title_font).place(x="700",
                                                                                                         y="210")
        role_label = tk.Label(self, text="Role: ", font=self.controller.title_font).place(x="657", y="260")
        role_2 = tk.Label(self, text="Employee", font=self.controller.label_font).place(x="737", y="265")
        date_label = tk.Label(self, text="Date: ", font=self.controller.title_font).place(x="657", y="310")
        date_2 = tk.Label(self, text="10/08/2019", font=self.controller.label_font).place(x="737", y="315")
        time_label = tk.Label(self, text="Time: ", font=self.controller.title_font).place(x="657", y="350")
        time_2 = tk.Label(self, text="10am - 3pm", font=self.controller.label_font).place(x="737", y="355")

        username_label = tk.Label(self, text="Username: ", font=self.controller.label_font).grid(column=2, row=8)
        username_entry = tk.Entry(self).grid(column=3, row=8)

        self.booking_date_text = tk.StringVar()
        self.booking_date_text.set("")
        booking_date = tk.Label(self, text="Booking Date(YYYY/MM/DD): ", font=self.controller.label_font).grid(column=2, row=9)
        booking_entry = tk.Entry(self, textvariable=self.booking_date_text).grid(column=3, row=9)

        vehicle_reg = tk.Label(self, text="Vehicle Reg: ", font=self.controller.label_font).grid(column=2, row=10)
        vehicle_reg_entry = tk.Entry(self).grid(column=3, row=10)

        start_time_label = tk.Label(self, text="Start Time: ", font=self.controller.label_font).grid(column=2, row=11)
        start_time_entry = tk.Entry(self).grid(column=3, row=11)

        end_time_label = tk.Label(self, text="End Time: ", font=self.controller.label_font).grid(column=2, row=12)
        end_time_entry = tk.Entry(self).grid(column=3, row=12)


        submit_button = tk.Button(self, text="Submit", command=self.submit).grid(column=3, row=14)

        self.collision_text = tk.StringVar()
        self.collision_text.set("")
        collision_detection = tk.Label(self, textvariable=self.collision_text, font=self.controller.label_font).grid(column=3, row=13)


    def submit(self):
        booking_date = datetime.strptime(self.booking_date_text.get(), "%Y-%m-%d")
        check = get_date(booking_date, read_user_file("user.txt"))
        if(check is True):
            self.collision_text.set("Success")
            utils.db_func.insert_booking(read_user_file("user.txt"), booking_date, )
        else:
            self.collision_text.set("Failed")

def get_date(date_text, user_local):
    x, y = utils.db_func.validate_booking(user_local, date_text)
    check = False
    if x is True:
        check = True

    return check

class RegistrationForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self, text="Registration Form", font=controller.title_font).grid(column=2, row=1)

        self.username_text = tk.StringVar()
        username_label = tk.Label(self, text="Username(Email Address): ", font=controller.label_font).grid(column=1,
                                                                                                           row=2)
        self.username_entry = tk.Entry(self, textvariable=self.username_text).grid(column=2, row=2)

        self.password_text = tk.StringVar()
        password_label = tk.Label(self, text="Password: ", font=controller.label_font).grid(column=3, row=2)
        password_entry = tk.Entry(self, show="*", textvariable=self.password_text).grid(column=4, row=2)

        # TODO add confirm password field
        self.first_name_text = tk.StringVar()
        first_name_label = tk.Label(self, text="First Name: ", font=controller.label_font).grid(column=1, row=3)
        first_name_entry = tk.Entry(self, textvariable=self.first_name_text).grid(column=2, row=3)

        self.last_name_text = tk.StringVar()
        last_name_label = tk.Label(self, text="Surname: ", font=controller.label_font).grid(column=3, row=3)
        last_name_entry = tk.Entry(self, textvariable=self.last_name_text).grid(column=4, row=3)

        self.phone_number_text = tk.StringVar()
        phone_number_label = tk.Label(self, text="Phone Number: ", font=controller.label_font).grid(column=1, row=4)
        phone_number_entry = tk.Entry(self, textvariable=self.phone_number_text).grid(column=2, row=4)

        self.address_text = tk.StringVar()
        address__line1_label = tk.Label(self, text="Address Line 1: ", font=controller.label_font).grid(column=1, row=5)
        address__line1_entry = tk.Entry(self, textvariable=self.address_text).grid(column=2, row=5)

        self.address_second_line_text = tk.StringVar()
        address_line2_label = tk.Label(self, text="Address Line 2: ", font=controller.label_font).grid(column=3, row=5)
        address_line2_entry = tk.Entry(self, textvariable=self.address_second_line_text).grid(column=4, row=5)

        self.city_text = tk.StringVar()
        city_label = tk.Label(self, text="City: ", font=controller.label_font).grid(column=1, row=6)
        city_entry = tk.Entry(self, textvariable=self.city_text).grid(column=2, row=6)

        self.post_code = tk.StringVar()
        post_code_label = tk.Label(self, text="Postcode: ", font=controller.label_font).grid(column=3, row=6)
        post_code_entry = tk.Entry(self, textvariable=self.post_code).grid(column=4, row=6)

        # todo discuss whether role is tied to employee number or if it's assigned by admins

        self.role_text = tk.StringVar()
        role_label = tk.Label(self, text="Role: ", font=controller.label_font).grid(column=1, row=7)
        role_2_labe = tk.Label(self, text="PENDING", font=controller.label_font).grid(column=2, row=7)

        self.employee_number = tk.StringVar()
        employee_number_label = tk.Label(self, text="Employee Number: ", font=controller.label_font).grid(column=3,
                                                                                                          row=7)
        employee_number_entry = tk.Entry(self, textvariable=self.employee_number).grid(column=4, row=7)

        self.check_badge = tk.IntVar()
        blue_badge_label = tk.Label(self, text="Blue Badge Holder? ", font=controller.label_font).grid(column=3, row=8)
        blue_button_button = tk.Checkbutton(self, variable=self.check_badge).grid(column=4, row=8)

        manager_label = tk.Label(self, text="Current Manager: ", font=controller.label_font).grid(column=1, row=8)
        manager_entry = tk.Entry(self).grid(column=2, row=8)

        submit_button = tk.Button(self, text="Submit Form", command=self.check, font=controller.title_font).grid(
            column=3, row=9)

        back_button = tk.Button(self, text="Return To Login", command=lambda: controller.switch_frame("LoginScreen"), font=controller.title_font). grid(column=4, row=9)

    def check(self):
        username = self.username_text.get()
        check = utils.register.check_all(username, file_path)
        if check is True:
            address = self.address_text.get() + " : " + self.address_second_line_text.get() + " : " + self.city_text.get()
            # username, password, firstname, lastname, phone_no, location, postcode, role, employee_no, badge, is_blue
            values = [self.username_text.get(), self.password_text.get(), self.first_name_text.get(),
                      self.last_name_text.get(), self.phone_number_text.get(), address, self.post_code.get(),
                      "PENDING", self.employee_number.get(), None, self.check_badge.get()
                      ]
            utils.register.insert_into_database("users", file_path, values)
        # lambda: controller.switch_frame("SubmissionPage")


class SubmissionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self,
                         text="Thank you for registering, \nyour form will be reviewed, \nwe will get back to you shortly",
                         font=controller.title_font, pady=30).pack()
        back_button = tk.Button(self, text="Return to login page",
                                command=lambda: controller.switch_frame("LoginScreen"),
                                font=controller.title_font).pack()


def get_name(credential_file=file_path):
    username = read_file("user.txt")
    creds = utils.db_init.load_credentials(credential_file)
    connect_sql = utils.db_init.connect(creds['user'], creds['database'], creds['password'], creds['host'])
    table = "users"
    sql = "SELECT * FROM " + table
    cursor = connect_sql.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()
    first_name = ""
    last_name = ""
    for record in records:
        if record[0] == username:
            first_name = record[2]
            last_name = record[3]
    return first_name, last_name


def read_file(file):
    with open(file, "r+") as f:
        username = f.read()
    return username


class DashboardUser(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # role = ""
        # utils.db_func
        # if role == "Manager":

        image = Image.open("herbie_logo.png")
        image = image.resize((150, 75), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        artwork = tk.Label(self, image=image)
        artwork.photo = image
        artwork.grid(column=1, row=1)

        user = get_name(file_path)
        welcome_message = tk.Label(self, text="Welcome back " + user[0] + " " + user[1], font=controller.title_font,
                                   pady=15, padx=200).grid(column=3, row=1)

        account_button = tk.Button(self, text="Account", command=lambda: controller.switch_frame("AccountDetails"),
                                   font=controller.label_font, pady=5, padx=10).grid(column=4, row=1)

        bookings_button = tk.Button(self, text="Boookings", command=lambda: controller.switch_frame("BookingScreen"),
                                    font=controller.label_font, pady=5, padx=10).grid(column=5, row=1)

        line = tk.Frame(self, height=3, width=1200, bg="black").grid(column=1, columnspan=10, row=2)

        subframe_1 = tk.Frame(self, relief="raised", pady=5, borderwidth=2)
        subframe_1.place(x="75", y="150")

        cal = Calendar(subframe_1, font="Arial 14", selectmode='day', locale='en_UK',
                       cursor="hand2")

        cal.config(background="#292d2f", foreground="#1586da", headersbackground="#292d2f", headersforeground="#1586da",
                   selectbackground="#292d2f", selectforeground="#16dace", normalbackground="#292d2f",
                   normalforeground="#1586da",
                   weekendbackground="#292d2f", weekendforeground="#1586da", othermonthbackground="#292d2f",
                   othermonthwebackground="#292d2f")

        cal.pack(fill="both", expand=True)

        subframe_2 = tk.Frame(self, height="275", width="500", relief="raised", pady=5, padx=5, borderwidth=2)
        subframe_2.place(x="520", y="160")
        line_2 = tk.Frame(self, height=30, width=500, bg="#16dace").place(x="520", y="160")

        image_2 = Image.open("Default_picture.png")
        image_2 = image_2.resize((150, 150), Image.ANTIALIAS)
        image_2 = ImageTk.PhotoImage(image_2)
        artwork_2 = tk.Label(self, image=image_2)
        artwork_2.photo = image_2
        artwork_2.place(x="840", y="265")
        ad = utils.account_details.AccountDetails(self.read_file("user.txt"), file_path)
        user = ad.get_user_details()
        first_name = user[2]
        last_name = user[3]
        full_name = first_name + " " + last_name
        name_label = tk.Label(self, text=(full_name), font=controller.title_font).place(x="600", y="210")
        role_label = tk.Label(self, text="Role: ", font=controller.title_font).place(x="557", y="260")
        role_2 = tk.Label(self, text="Employee", font=controller.label_font).place(x="637", y="265")
        date_label = tk.Label(self, text="Date: ", font=controller.title_font).place(x="557", y="310")
        date_2 = tk.Label(self, text="10/08/2019", font=controller.label_font).place(x="637", y="315")
        time_label = tk.Label(self, text="Time: ", font=controller.title_font).place(x="557", y="350")
        time_2 = tk.Label(self, text="10am - 3pm", font=controller.label_font).place(x="637", y="355")

        subframe_3 = tk.Frame(self, height="275", width="250", relief="raised", pady=5, padx=5, borderwidth=2)
        subframe_3.place(x="1050", y="160")

        p_and_r_label = tk.Label(self, text="Your P&R Dates", font=controller.title_font).place(x="1065", y="175")
        pr_label_text = tk.Label(self, text="As a blue badge holder:", font=controller.label_font).place(x="1060",
                                                                                                         y="220")

    def on_show_frame(self, event):
        subframe_1 = tk.Frame(self, relief="raised", pady=5, borderwidth=2)
        subframe_1.place(x="75", y="150")
        cal = Calendar(subframe_1, font="Arial 14", selectmode='day', locale='en_UK',
                       cursor="hand2")

        cal.config(background="#292d2f", foreground="#1586da", headersbackground="#292d2f",
                   headersforeground="#1586da",
                   selectbackground="#292d2f", selectforeground="#16dace", normalbackground="#292d2f",
                   normalforeground="#1586da",
                   weekendbackground="#292d2f", weekendforeground="#1586da", othermonthbackground="#292d2f",
                   othermonthwebackground="#292d2f")
        cal.pack(fill="both", expand=True)

        username = read_user_file("user.txt")
        account_details = utils.date_select_logic.get_date_time(username, file_path)
        date = account_details[0]
        start_time = account_details[1]
        end_time = account_details[2]
        for index in range(len(account_details[0])):
            booking_date = datetime.strptime(date[index], "%Y-%m-%d")
            cal.calevent_create(booking_date, "booking " + str(start_time[index]) + " - " + str(end_time[index]),
                                "booking")
            cal.tag_config('booking', background='red', foreground='yellow')

        cal.pack(fill="both", expand=True)

        log_out_button = tk.Button(self, text="Log Out",
                                   command=lambda: self.controller.switch_frame("LoginScreen"),
                                   font=self.controller.title_font).place(x=100, y=450)

    def read_file(self, file):
        with open(file, "r+") as f:
            username = f.read()
        return username


class DashboardManager(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        image = Image.open("herbie_logo.png")
        image = image.resize((150, 75), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        artwork = tk.Label(self, image=image)
        artwork.photo = image
        artwork.grid(column=1, row=1)

        user = get_name(file_path)
        welcome_message = tk.Label(self, text="Welcome back " + user[0] + " " + user[1], font=controller.title_font,
                                   pady=15, padx=200).grid(column=2, row=1)

        account_button = tk.Button(self, text="Account", command=lambda: controller.switch_frame("AccountDetails"),
                                   font=controller.label_font, pady=5, padx=10).grid(column=4, row=1)

        bookings_button = tk.Button(self, text="Boookings",
                                    command=lambda: controller.switch_frame("BookingScreen"),
                                    font=controller.label_font, pady=5, padx=10).grid(column=5, row=1)
        view_employee_button = tk.Button(self, text="Employee Bookings",
                                         command=lambda: controller.switch_frame("DashboardUser"),
                                         font=controller.label_font, pady=5, padx=10).grid(column=6, row=1)
        reports_button = tk.Button(self, text="Reports", command=lambda: controller.switch_frame("Reports"), font=controller.label_font, pady=5, padx=10).grid(column=7, row=1)

        line = tk.Frame(self, height=3, width=1200, bg="black").grid(column=1, columnspan=10, row=2)

        subframe_1 = tk.Frame(self, relief="raised", pady=5, borderwidth=2)
        subframe_1.place(x="75", y="150")

        # cal = Calendar(subframe_1, font="Arial 14", selectmode='day', locale='en_UK',
        #                cursor="hand2")
        #
        # cal.config(background="#292d2f", foreground="#1586da", headersbackground="#292d2f",
        #            headersforeground="#1586da",
        #            selectbackground="#292d2f", selectforeground="#16dace", normalbackground="#292d2f",
        #            normalforeground="#1586da",
        #            weekendbackground="#292d2f", weekendforeground="#1586da", othermonthbackground="#292d2f",
        #            othermonthwebackground="#292d2f")



        subframe_2 = tk.Frame(self, height="275", width="500", relief="raised", pady=5, padx=5, borderwidth=2)
        subframe_2.place(x="520", y="160")
        line_2 = tk.Frame(self, height=30, width=500, bg="#16dace").place(x="520", y="160")

        image_2 = Image.open("Default_picture.png")
        image_2 = image_2.resize((150, 150), Image.ANTIALIAS)
        image_2 = ImageTk.PhotoImage(image_2)
        artwork_2 = tk.Label(self, image=image_2)
        artwork_2.photo = image_2
        artwork_2.place(x="840", y="265")

        name_label = tk.Label(self, text=(self.read_file("user.txt")), font=controller.title_font).place(x="600",
                                                                                                         y="210")
        role_label = tk.Label(self, text="Role: ", font=controller.title_font).place(x="557", y="260")
        role_2 = tk.Label(self, text="Employee", font=controller.label_font).place(x="637", y="265")
        date_label = tk.Label(self, text="Date: ", font=controller.title_font).place(x="557", y="310")
        date_2 = tk.Label(self, text="10/08/2019", font=controller.label_font).place(x="637", y="315")
        time_label = tk.Label(self, text="Time: ", font=controller.title_font).place(x="557", y="350")
        time_2 = tk.Label(self, text="10am - 3pm", font=controller.label_font).place(x="637", y="355")

        subframe_3 = tk.Frame(self, height="275", width="250", relief="raised", pady=5, padx=5, borderwidth=2)
        subframe_3.place(x="1050", y="160")

        p_and_r_label = tk.Label(self, text="Your P&R Dates", font=controller.title_font).place(x="1065", y="175")
        pr_label_text = tk.Label(self, text="As a blue badge holder:", font=controller.label_font).place(x="1060",
                                                                                                         y="220")

        self.bind("<<ShowFrame>>", self.on_show_frame)

    def on_show_frame(self, event):
        subframe_1 = tk.Frame(self, relief="raised", pady=5, borderwidth=2)
        subframe_1.place(x="75", y="150")
        cal = Calendar(subframe_1, font="Arial 14", selectmode='day', locale='en_UK',
                           cursor="hand2")

        cal.config(background="#292d2f", foreground="#1586da", headersbackground="#292d2f",
                       headersforeground="#1586da",
                       selectbackground="#292d2f", selectforeground="#16dace", normalbackground="#292d2f",
                       normalforeground="#1586da",
                       weekendbackground="#292d2f", weekendforeground="#1586da", othermonthbackground="#292d2f",
                       othermonthwebackground="#292d2f")
        cal.pack(fill="both", expand=True)

        username = read_user_file("user.txt")
        account_details = utils.date_select_logic.get_date_time(username, file_path)
        date = account_details[0]
        start_time = account_details[1]
        end_time = account_details[2]
        for index in range(len(account_details[0])):
            booking_date = datetime.strptime(date[index], "%Y-%m-%d")
            cal.calevent_create(booking_date, "booking " + str(start_time[index]) + " - " + str(end_time[index]), "booking")
            cal.tag_config('booking', background='red', foreground='yellow')

        cal.pack(fill="both", expand=True)

        log_out_button = tk.Button(self, text="Log Out", command=lambda: self.controller.switch_frame("LoginScreen"), font=self.controller.title_font).place(x=100, y=450)

    def read_file(self, file):
        with open(file, "r+") as f:
            username = f.read()
        return username

class DashboardFacilities(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        image = Image.open("herbie_logo.png")
        image = image.resize((150, 75), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        artwork = tk.Label(self, image=image)
        artwork.photo = image
        artwork.grid(column=1, row=1)

        user = get_name(file_path)
        welcome_message = tk.Label(self, text="Welcome back " + user[0] + " " + user[1], font=controller.title_font,
                                   pady=15, padx=200).grid(column=2, row=1)

        account_button = tk.Button(self, text="Account", command=lambda: controller.switch_frame("AccountDetails"),
                                   font=controller.label_font, pady=5, padx=10).grid(column=4, row=1)

        bookings_button = tk.Button(self, text="Boookings",
                                    command=lambda: controller.switch_frame("BookingScreen"),
                                    font=controller.label_font, pady=5, padx=10).grid(column=5, row=1)

        reports_button = tk.Button(self, text="Reports", command=lambda: controller.switch_frame("Reports"), font=controller.label_font, pady=5, padx=10).grid(column=6, row=1)

        line = tk.Frame(self, height=3, width=1200, bg="black").grid(column=1, columnspan=10, row=2)

        subframe_1 = tk.Frame(self, relief="raised", pady=5, borderwidth=2)
        subframe_1.place(x="75", y="150")

        cal = Calendar(subframe_1, font="Arial 14", selectmode='day', locale='en_UK',
                       cursor="hand2")

        cal.config(background="#292d2f", foreground="#1586da", headersbackground="#292d2f",
                   headersforeground="#1586da",
                   selectbackground="#292d2f", selectforeground="#16dace", normalbackground="#292d2f",
                   normalforeground="#1586da",
                   weekendbackground="#292d2f", weekendforeground="#1586da", othermonthbackground="#292d2f",
                   othermonthwebackground="#292d2f")

        cal.pack(fill="both", expand=True)

        subframe_2 = tk.Frame(self, height="275", width="500", relief="raised", pady=5, padx=5, borderwidth=2)
        subframe_2.place(x="520", y="160")
        line_2 = tk.Frame(self, height=30, width=500, bg="#16dace").place(x="520", y="160")

        image_2 = Image.open("Default_picture.png")
        image_2 = image_2.resize((150, 150), Image.ANTIALIAS)
        image_2 = ImageTk.PhotoImage(image_2)
        artwork_2 = tk.Label(self, image=image_2)
        artwork_2.photo = image_2
        artwork_2.place(x="840", y="265")

        name_label = tk.Label(self, text=(self.read_file("user.txt")), font=controller.title_font).place(x="600",
                                                                                                         y="210")
        role_label = tk.Label(self, text="Role: ", font=controller.title_font).place(x="557", y="260")
        role_2 = tk.Label(self, text="Employee", font=controller.label_font).place(x="637", y="265")
        date_label = tk.Label(self, text="Date: ", font=controller.title_font).place(x="557", y="310")
        date_2 = tk.Label(self, text="10/08/2019", font=controller.label_font).place(x="637", y="315")
        time_label = tk.Label(self, text="Time: ", font=controller.title_font).place(x="557", y="350")
        time_2 = tk.Label(self, text="10am - 3pm", font=controller.label_font).place(x="637", y="355")

        subframe_3 = tk.Frame(self, height="275", width="250", relief="raised", pady=5, padx=5, borderwidth=2)
        subframe_3.place(x="1050", y="160")

        p_and_r_label = tk.Label(self, text="Your P&R Dates", font=controller.title_font).place(x="1065", y="175")
        pr_label_text = tk.Label(self, text="As a blue badge holder:", font=controller.label_font).place(x="1060",
                                                                                                         y="220")

    def on_show_frame(self, event):
        subframe_1 = tk.Frame(self, relief="raised", pady=5, borderwidth=2)
        subframe_1.place(x="75", y="150")
        cal = Calendar(subframe_1, font="Arial 14", selectmode='day', locale='en_UK',
                       cursor="hand2")

        cal.config(background="#292d2f", foreground="#1586da", headersbackground="#292d2f",
                   headersforeground="#1586da",
                   selectbackground="#292d2f", selectforeground="#16dace", normalbackground="#292d2f",
                   normalforeground="#1586da",
                   weekendbackground="#292d2f", weekendforeground="#1586da", othermonthbackground="#292d2f",
                   othermonthwebackground="#292d2f")
        cal.pack(fill="both", expand=True)

        username = read_user_file("user.txt")
        account_details = utils.date_select_logic.get_date_time(username, file_path)
        date = account_details[0]
        start_time = account_details[1]
        end_time = account_details[2]
        for index in range(len(account_details[0])):
            booking_date = datetime.strptime(date[index], "%Y-%m-%d")
            cal.calevent_create(booking_date, "booking " + str(start_time[index]) + " - " + str(end_time[index]),
                                "booking")
            cal.tag_config('booking', background='red', foreground='yellow')

        cal.pack(fill="both", expand=True)

        log_out_button = tk.Button(self, text="Log Out",
                                   command=lambda: self.controller.switch_frame("LoginScreen"),
                                   font=self.controller.title_font).place(x=100, y=450)

    def read_file(self, file):
        with open(file, "r+") as f:
            username = f.read()
        return username


class DashboardSysAdmin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        image = Image.open("herbie_logo.png")
        image = image.resize((150, 75), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        artwork = tk.Label(self, image=image)
        artwork.photo = image
        artwork.grid(column=1, row=1)

        user = get_name("../secrets.json")
        welcome_message = tk.Label(self, text="Welcome back " + user[0] + " " + user[1], font=controller.title_font,
                                   pady=15, padx=200).grid(column=2, row=1)

        account_button = tk.Button(self, text="Account", command=lambda: controller.switch_frame("AccountDetails"),
                                   font=controller.label_font, pady=5, padx=10).grid(column=4, row=1)

        bookings_button = tk.Button(self, text="Boookings",
                                    command=lambda: controller.switch_frame("BookingScreen"),
                                    font=controller.label_font, pady=5, padx=10).grid(column=5, row=1)

        reports_button = tk.Button(self, text="Reports", command=lambda: controller.switch_frame("Reports"), font=controller.label_font, pady=5, padx=10).grid(column=6, row=1)

        parking_dates_button = tk.Button(self, text="Parking Data", command=lambda: controller.switch_Frame("Parking Data"), font=controller.label_font, pady=5, padx=10).grid(column=7, row=1)

        approve_accounts = tk.Button(self, text="Account Approval", command=lambda: controller.switch_Frame("User Accounts"), font=controller.label_font, pady=5, padx=10).grid(column=8, row=1)

        line = tk.Frame(self, height=3, width=1200, bg="black").grid(column=1, columnspan=10, row=2)

        subframe_1 = tk.Frame(self, relief="raised", pady=5, borderwidth=2)
        subframe_1.place(x="75", y="150")

        cal = Calendar(subframe_1, font="Arial 14", selectmode='day', locale='en_UK',
                       cursor="hand2")

        cal.config(background="#292d2f", foreground="#1586da", headersbackground="#292d2f",
                   headersforeground="#1586da",
                   selectbackground="#292d2f", selectforeground="#16dace", normalbackground="#292d2f",
                   normalforeground="#1586da",
                   weekendbackground="#292d2f", weekendforeground="#1586da", othermonthbackground="#292d2f",
                   othermonthwebackground="#292d2f")

        cal.pack(fill="both", expand=True)

        subframe_2 = tk.Frame(self, height="275", width="500", relief="raised", pady=5, padx=5, borderwidth=2)
        subframe_2.place(x="520", y="160")
        line_2 = tk.Frame(self, height=30, width=500, bg="#16dace").place(x="520", y="160")

        image_2 = Image.open("Default_picture.png")
        image_2 = image_2.resize((150, 150), Image.ANTIALIAS)
        image_2 = ImageTk.PhotoImage(image_2)
        artwork_2 = tk.Label(self, image=image_2)
        artwork_2.photo = image_2
        artwork_2.place(x="840", y="265")

        name_label = tk.Label(self, text=(self.read_file("user.txt")), font=controller.title_font).place(x="600",
                                                                                                         y="210")
        role_label = tk.Label(self, text="Role: ", font=controller.title_font).place(x="557", y="260")
        role_2 = tk.Label(self, text="Employee", font=controller.label_font).place(x="637", y="265")
        date_label = tk.Label(self, text="Date: ", font=controller.title_font).place(x="557", y="310")
        date_2 = tk.Label(self, text="10/08/2019", font=controller.label_font).place(x="637", y="315")
        time_label = tk.Label(self, text="Time: ", font=controller.title_font).place(x="557", y="350")
        time_2 = tk.Label(self, text="10am - 3pm", font=controller.label_font).place(x="637", y="355")

        subframe_3 = tk.Frame(self, height="275", width="250", relief="raised", pady=5, padx=5, borderwidth=2)
        subframe_3.place(x="1050", y="160")

        p_and_r_label = tk.Label(self, text="Your P&R Dates", font=controller.title_font).place(x="1065", y="175")
        pr_label_text = tk.Label(self, text="As a blue badge holder:", font=controller.label_font).place(x="1060",
                                                                                                         y="220")

    def on_show_frame(self, event):
        subframe_1 = tk.Frame(self, relief="raised", pady=5, borderwidth=2)
        subframe_1.place(x="75", y="150")
        cal = Calendar(subframe_1, font="Arial 14", selectmode='day', locale='en_UK',
                       cursor="hand2")

        cal.config(background="#292d2f", foreground="#1586da", headersbackground="#292d2f",
                   headersforeground="#1586da",
                   selectbackground="#292d2f", selectforeground="#16dace", normalbackground="#292d2f",
                   normalforeground="#1586da",
                   weekendbackground="#292d2f", weekendforeground="#1586da", othermonthbackground="#292d2f",
                   othermonthwebackground="#292d2f")
        cal.pack(fill="both", expand=True)

        username = read_user_file("user.txt")
        account_details = utils.date_select_logic.get_date_time(username, file_path)
        date = account_details[0]
        start_time = account_details[1]
        end_time = account_details[2]
        for index in range(len(account_details[0])):
            booking_date = datetime.strptime(date[index], "%Y-%m-%d")
            cal.calevent_create(booking_date, "booking " + str(start_time[index]) + " - " + str(end_time[index]),
                                "booking")
            cal.tag_config('booking', background='red', foreground='yellow')

        cal.pack(fill="both", expand=True)

        log_out_button = tk.Button(self, text="Log Out",
                                   command=lambda: self.controller.switch_frame("LoginScreen"),
                                   font=self.controller.title_font).place(x=100, y=450)

    def read_file(self, file):
        with open(file, "r+") as f:
            username = f.read()
        return username



if __name__ == "__main__":
    app = Application()
    app.mainloop()

