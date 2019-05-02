import calendar
import datetime
import sys
import utils.date_select_logic
import utils.date_select_logic

if sys.version[0] == '2':
    import Tkinter as tk
else:
    import tkinter as tk

file_path = "..\secrets.json"


class Calendar:
    def __init__(self, parent, values):
        self.values = values
        self.parent = parent
        self.cal = calendar.TextCalendar(calendar.SUNDAY)
        self.year = datetime.date.today().year
        self.month = datetime.date.today().month
        self.wid = []
        self.day_selected = 1
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = ''

        self.setup(self.year, self.month)

    def clear(self):
        for w in self.wid[:]:
            w.grid_forget()
            # w.destroy()
            self.wid.remove(w)

    def go_prev(self):
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1
        # self.selected = (self.month, self.year)
        self.clear()
        self.setup(self.year, self.month)

    def go_next(self):
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1

        # self.selected = (self.month, self.year)
        self.clear()
        self.setup(self.year, self.month)

    def selection(self, day, name):
        self.day_selected = day
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = name

        # data
        self.values['day_selected'] = day
        self.values['month_selected'] = self.month
        self.values['year_selected'] = self.year
        self.values['day_name'] = name
        self.values['month_name'] = calendar.month_name[self.month_selected]

        self.clear()
        self.setup(self.year, self.month)

    def setup(self, y, m):
        left = tk.Button(self.parent, text='<', command=self.go_prev)
        self.wid.append(left)
        left.grid(row=0, column=1)

        header = tk.Label(self.parent, height=2, text='{}   {}'.format(calendar.month_abbr[m], str(y)))
        self.wid.append(header)
        header.grid(row=0, column=2, columnspan=3)

        right = tk.Button(self.parent, text='>', command=self.go_next)
        self.wid.append(right)
        right.grid(row=0, column=5)

        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for num, name in enumerate(days):
            t = tk.Label(self.parent, text=name[:3])
            self.wid.append(t)
            t.grid(row=1, column=num)

        for w, week in enumerate(self.cal.monthdayscalendar(y, m), 2):
            for d, day in enumerate(week):
                if day:
                    # print(calendar.day_name[day])
                    #change colour based on if the day is booked.
                    # username = self.read_file("../tkinter_code/user.txt")
                    # booked_dates = utils.date_select_logic.check_if_booked(username, "H:\Applications of programming\CIB\secrets.json")
                    # if booked_dates
                    b = tk.Button(self.parent, width=5, text=day,
                                  command=lambda day=day: self.selection(day, calendar.day_name[(day - 1) % 7]))
                    self.wid.append(b)
                    b.grid(row=w, column=d)

        sel = tk.Label(self.parent, height=2, text='{} {} {} {}'.format(
            self.day_name, calendar.month_name[self.month_selected], self.day_selected, self.year_selected))
        self.wid.append(sel)
        sel.grid(row=8, column=0, columnspan=7)

        ok = tk.Button(self.parent, width=5, text='OK', command=self.kill_and_save)
        self.wid.append(ok)
        ok.grid(row=9, column=2, columnspan=3, pady=10)

    def kill_and_save(self):
        date = str(self.values['year_selected']) + "-" + str(self.values['month_selected']) + "-" + str(
            self.values['day_selected'])
        free_date = utils.date_select_logic.check_date(date, file_path)
        if free_date is True:
            username = self.read_file("../tkinter_code/user.txt")

            utils.date_select_logic.insert_into_database(file_path, date, username)
            self.parent.destroy()

    def read_file(self, file):
        with open(file, "r+") as f:
            username = f.read()
        return username

class Control:
    def __init__(self, parent):
        parent = parent
        choose_btn = tk.Button(parent, text='Open Calendar', command=self.popup, width=20, height=5)
        # show_btn = tk.Button(parent, text='Show Selected', command=self.print_selected_date)
        choose_btn.grid(column=1, row=2, pady=50)
        # show_btn.grid(column=1, row=3)
        self.data = {}

    def popup(self):
        child = tk.Toplevel()
        cal = Calendar(child, self.data)

    # def print_selected_date(self):
    #     data_to_send = str(self.data['year_selected']) + "-" + str(self.data['month_selected']) + "-" + str(self.data['day_selected'])
    #     free_date = utils.date_select_logic.check_date(data_to_send, "H:\Applications of programming\CIB\secrets.json")
    #     print(data_to_send)
