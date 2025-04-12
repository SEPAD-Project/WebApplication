from datetime import date as d ,timedelta
from flask_login import current_user

def student_over_week(class_name, national_code):
    file_path = f"c:\sap-project\server\schools\{current_user.school_code}\{class_name}\{national_code}.txt"
    over_week = {}

    today = d.today()
    dates = [str(today.strftime("%Y-%m-%d"))]
    for i in range(1,7):
        dates.append(str((today-timedelta(i)).strftime("%Y-%m-%d")))

    for date in dates:
        over_week[date] = [0, 0]

    with open(file_path, 'r') as f:
        lines = f.readlines()[1:]

    for line in lines:
        content = line.split('|')
        result_date = content[2].split()[0]
        if result_date in dates:
            if content[0] == '5':
                over_week[result_date][0] += 1
            over_week[result_date][1] +=  1

    for date in over_week:
        try:
            over_week[date] = (over_week[date][0] / over_week[date][1]) * 100
        except ZeroDivisionError:
            over_week[date] = 0

    return over_week
