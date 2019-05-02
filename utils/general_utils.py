import calendar
import datetime
from datetime import timedelta


def format_datetime_to_number_str(date : datetime.date):
    #TODO logic to ad th or 1st to day
    return "{}/{}/{}".format(date.day, date.month, date.year)


def format_int_to_time(time_int):
    #TODO write this properly
    return str(time_int)+":00"
