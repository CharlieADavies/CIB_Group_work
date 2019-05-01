import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk, PhotoImage
import utils.passwords
import utils.account_details
import tkinter_code.calander_

from PIL import ImageTk, Image
import os
from tkcalendar import Calendar

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
        for pages in (LoginScreen, RegistrationForm, BookingScreen, SubmissionPage, Dashboard):
            page_name = pages.__name__
            frame = pages(parent=window_manager, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.switch_frame("LoginScreen")
        self.title("B&Q Parking")
        self.geometry("900x500")

    def switch_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class LoginScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self, text="Please Login", font=controller.title_font).grid(column=2, row=1)

        username_label = tk.Label(self, text="Username: ", font=controller.label_font).grid(column=1, row=2)
        self.username_text = tk.StringVar()
        username_entry = tk.Entry(self, textvariable=self.username_text).grid(column=2, row=2)

        password_label = tk.Label(self, text="Password: ", font=controller.label_font).grid(column=1, row=3)
        self.password_text = tk.StringVar()
        password_entry = tk.Entry(self, show="*", textvariable=self.password_text).grid(column=2, row=3)

        login_button = tk.Button(self, text="Login", command=lambda: controller.switch_frame("Dashboard"), font=controller.label_font).grid(column=2, row=4)

        register_button = tk.Button(self, text="Registration", command=lambda: controller.switch_frame("RegistrationForm"), font=controller.title_font, pady=15).grid(column=2, row=5)

    def login_click(self):
        # in empty "" enter your secretes.json file path.
        # eg. ardra.denford@yahoo.co.uk, VYq0X718mm for username and password
        can_login = utils.passwords.check_user(
            self.username_text.get(), self.password_text.get(), "H:\Applications of programming\CIB\secrets.json")
        if can_login is True:
            self.controller.switch_frame("Dashboard")
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
        username_label = tk.Label(self, textvariable=self.username_text, font=controller.label_font).grid(column=1, row=2)

        self.first_name_text = tk.StringVar()
        self.first_name_text.set("First name: ")
        first_name_Label = tk.Label(self, textvariable=self.first_name_text, font=controller.label_font).grid(column=1, row=3)

        self.last_name_text = tk.StringVar()
        self.last_name_text.set("Last Name: ")
        last_name_Label = tk.Label(self, textvariable=self.last_name_text, font=controller.label_font).grid(column=1, row=4)

        self.phone_number_text = tk.StringVar()
        self.phone_number_text.set("Phone Number: ")
        Phone_number = tk.Label(self, textvariable=self.phone_number_text, font=controller.label_font).grid(column=1, row=5)

        self.address_text = tk.StringVar()
        self.address_text.set("Address: ")
        Address_Label = tk.Label(self, textvariable=self.address_text, font=controller.label_font).grid(column=1, row=6)

        self.postcode_text = tk.StringVar()
        self.postcode_text.set("Post code: ")
        postcode_Label = tk.Label(self, textvariable=self.postcode_text, font=controller.label_font).grid(column=1, row=7)

        self.role_text = tk.StringVar()
        self.role_text.set("Role: ")
        role_Label = tk.Label(self, textvariable=self.role_text, font=controller.label_font).grid(column=1, row=8)

        self.employee_number_text = tk.StringVar()
        self.employee_number_text.set("Employee number: ")
        employee_number_Label = tk.Label(self, textvariable=self.employee_number_text, font=controller.label_font).grid(column=1, row=9)

        self.badge_text = tk.StringVar()
        self.badge_text .set("badge: ")
        badge_Label = tk.Label(self, textvariable=self.badge_text, font=controller.label_font).grid(column=1, row=10)

        self.has_blue_badge_text = tk.StringVar()
        self.has_blue_badge_text.set("Blue Badge: ")
        has_blue_badge_Label = tk.Label(self, textvariable=self.has_blue_badge_text, font=controller.label_font).grid(column=1, row=11)
        self.account_logic()

    
    def account_logic(self):
        account_details = utils.account_details.AccountDetails("jacob.smith@gmail.com", "H:\\Applications of programming\CIB\\secrets.json")
        details = account_details.get_user_details()
        self.username_text.set("Username: " + str(details[0]))
        self.first_name_text.set("First name: " + str(details[2]))
        self.last_name_text.set("Last name: " + str(details[3]))
        self.phone_number_text.set("Phone Number: " + str(details[4]))
        self.address_text.set("Address: " + str(details[5]))
        self.postcode_text.set("Post Code: " + str(details[6]))
        self.role_text.set("Role: " + str(details[7]))
        self.employee_number_text.set("Employee Number: " + str(details[8]))
        self.badge_text.set("Badge: " + str(details[9]))
        self.has_blue_badge_text.set("Blue Badge: " + str(details[10]))


class BookingScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        photo = tk.PhotoImage(file="Logo.png")
        title = tk.Label(self, text="Bookings", font=controller.title_font).grid(column=2, row=1)
        # YYYY-MM-DD
        control = tkinter_code.calander_.Control(self)

        self.username_text = tk.StringVar()
        self.username_text.set("Username")
        username_label = tk.Label(self, textvariable=self.username_text, font=controller.label_font).grid(column=1, row=4, pady=(100, 10))

        self.park_date_text = tk.StringVar()
        self.park_date_text.set("16-09-2000 10am-3pm")
        park_date_label = tk.Label(self, textvariable=self.park_date_text, font=controller.label_font).grid(column=1,
                                                                                                          row=5)

class RegistrationForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self, text="Registration Form", font=controller.title_font).grid(column=2, row=1)

        username_label = tk.Label(self, text="Username(Email Address): ", font=controller.label_font).grid(column=1, row=2)
        username_entry = tk.Entry(self).grid(column=2, row=2)

        password_label = tk.Label(self, text="Password: ", font=controller.label_font).grid(column=3, row=2)
        password_entry = tk.Entry(self, show="*").grid(column=4, row=2)

        # TODO add confirm password field

        first_name_label = tk.Label(self, text="First Name: ", font=controller.label_font).grid(column=1, row=3)
        first_name_entry = tk.Entry(self).grid(column=2, row=3)

        last_name_label = tk.Label(self, text="Surname: ", font=controller.label_font).grid(column=3, row=3)
        last_name_entry = tk.Entry(self).grid(column=4, row=3)

        phone_number_label = tk.Label(self, text="Phone Number: ", font=controller.label_font).grid(column=1, row=4)
        phone_number_entry = tk.Entry(self).grid(column=2, row=4)

        address__line1_label = tk.Label(self, text="Address Line 1: ", font=controller.label_font).grid(column=1, row=5)
        address__line1_entry = tk.Entry(self).grid(column=2, row=5)

        address_line2_label = tk.Label(self, text="Address Line 2: ", font=controller.label_font).grid(column=3, row=5)
        address_line2_entry = tk.Entry(self).grid(column=4, row=5)

        city_label = tk.Label(self, text="City: ", font=controller.label_font).grid(column=1, row=6)
        city_entry = tk.Entry(self).grid(column=2, row=6)

        post_code_label = tk.Label(self, text="Postcode: ", font=controller.label_font).grid(column=3, row=6)
        post_code_entry = tk.Entry(self).grid(column=4, row=6)

        # todo discuss whether role is tied to employee number or if it's assigned by admins

        role_label = tk.Label(self, text="Role: ", font=controller.label_font).grid(column=1, row=7)
        role_entry = tk.Entry(self).grid(column=2, row=7)

        employee_number_label = tk.Label(self, text="Employee Number: ", font=controller.label_font).grid(column=3, row=7)
        employee_number_entry = tk.Entry(self).grid(column=4, row=7)

        blue_badge_label = tk.Label(self, text="Blue Badge Holder? ", font=controller.label_font).grid(column=3, row=8)
        blue_button_button = tk.Checkbutton(self).grid(column=4, row=8)

        submit_button = tk.Button(self, text="Submit Form", command=lambda: controller.switch_frame("SubmissionPage"), font=controller.title_font).grid(column=4, row=9)


class SubmissionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self, text="Thank you for registering, \nyour form will be reviewed, \nwe will get back to you shortly", font=controller.title_font, pady=30).pack()
        back_button = tk.Button(self, text="Return to login page", command=lambda: controller.switch_frame("LoginScreen"), font=controller.title_font).pack()


class Dashboard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        """profile_picture = ImageTk.PhotoImage(Image.open("Default_picture.png"))
        picture_label = ttk.Label(self, image=profile_picture).grid(column=1, row=1)"""

        welcome_message = tk.Label(self, text="Welcome back 'User'", font=controller.title_font, pady=15, padx=200).grid(column=3, row=1)

        account_button = tk.Button(self, text="Account", font=controller.label_font, pady=8, padx=10).grid(column=4, row=1)

        bookings_button = tk.Button(self, text="Boookings", command=lambda: controller.switch_frame("BookingScreen"), font=controller.label_font, pady=8, padx=10).grid(column=5, row=1)

        line = tk.Frame(self, height=3, width=720, bg="black").grid(column=1, columnspan=10, row=2)


if __name__ == "__main__":
    app = Application()
    app.mainloop()

