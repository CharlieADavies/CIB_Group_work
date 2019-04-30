import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk


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
        for pages in (LoginScreen, RegistrationForm):
            page_name = pages.__name__
            frame = pages(parent=window_manager, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.switch_frame("LoginScreen")
        self.title("B&Q Parking")
        self.geometry("800x300")

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
        username_entry = tk.Entry(self).grid(column=2, row=2)

        password_label = tk.Label(self, text="Password: ", font=controller.label_font).grid(column=1, row=3)
        password_entry = tk.Entry(self).grid(column=2, row=3)

        login_button = tk.Button(self, text="Login", font=controller.label_font).grid(column=2, row=4)

        register_button = tk.Button(self, text="Registration", command=lambda: controller.switch_frame("RegistrationForm"), font=controller.title_font).grid(column=2, row=5)


class RegistrationForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self, text="Registration Form", font=controller.title_font).grid(column=2, row=1)

        username_label = tk.Label(self, text="Username(Email Address): ", font=controller.label_font).grid(column=1, row=2)
        username_entry = tk.Entry(self).grid(column=2, row=2)

        password_label = tk.Label(self, text="Password: ", font=controller.label_font).grid(column=3, row=2)
        password_entry = tk.Entry(self).grid(column=4, row=2)

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

        #change


if __name__ == "__main__":
    app = Application()
    app.mainloop()

