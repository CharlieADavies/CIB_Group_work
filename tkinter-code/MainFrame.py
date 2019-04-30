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
        password_entry = tk.Entry(self, show="*").grid(column=2, row=3)

        login_button = tk.Button(self, text="Login", font=controller.label_font).grid(column=2, row=4)

        register_button = tk.Button(self, text="Registration", command=lambda: controller.switch_frame("RegistrationForm"), font=controller.title_font).grid(column=2, row=5)


class RegistrationForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = tk.Label(self, text="Registration Form", font=controller.title_font).grid(column=3, row=1)

        username_label = tk.Label(self, text="Username(Email Address): ", font=controller.label_font).grid(column=1, row=2)
        username_entry = tk.Entry(self).grid(column=2, row=2)

        password_label = tk.Label(self, text="Password: ", font=controller.label_font).grid(column=3, row=2)
        password_entry = tk.Entry(self).grid(column=4, row=2)

        first_name_label = tk.Label(self, text="First Name: ", font=controller.label_font).grid(column=1, row=3)
        first_name_entry = tk.Entry(self).grid(column=2, row=3)

        last_name_label = tk.Label(self, text="Last Name: ", font=controller.label_font).grid(column=3, row=3)
        last_name_entry = tk.Entry(self).grid(column=4, row=3)

        phone_number_label = tk.Label(self, text="Phone Number: ", font=controller.label_font).grid(column=1, row=4)

        #address

        #postcode

        #role

        #employee number

        #blue badge






if __name__ == "__main__":
    app = Application()
    app.mainloop()

