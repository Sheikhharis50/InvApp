from django.forms import DateInput
from datetime import datetime

class DatePickerInput(DateInput):
    input_type = 'date'

def getCurrentDate():
    d = datetime.today()
    day, month, year, hour, minutes, seconds = str(d.day), str(
        d.month), str(d.year), str(d.hour), str(d.minute), str(d.second)
    if int(day) < 10:
        day = '0' + day
    if int(month) < 10:
        month = '0' + month
    if int(hour) < 10:
        hour = '0' + hour
    if int(minutes) < 10:
        minutes = '0' + minutes
    if int(seconds) < 10:
        seconds = '0' + seconds
    return year + "-" + month + "-" + day + " " + hour + ":" + minutes + ":" + seconds
