import calendar
import datetime
from datetime import timedelta


def format_datetime_to_number_str(date : datetime.datetime):
    #TODO logic to ad th or 1st to day
    return "{}/{}/{}".format(date.day, date.month, date.year)

