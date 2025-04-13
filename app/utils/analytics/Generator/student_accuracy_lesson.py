from flask_login import current_user
from app.models.school import School
from app.models.teacher import Teacher
import datetime
from app.utils.excel_reading import schedule_extraction

def student_lessons(class_name, national_code):
    file_path = f"c:\sap-project\server\schools\{current_user.school_code}\{class_name}\{national_code}.txt"
    lessons = {}
    class_schedule = schedule_extraction(f"c:\sap-project\server\schools\{current_user.school_code}\{class_name}\schedule.xlsx", 'Sheet1')

    school_teachers = eval(School.query.filter(School.school_code==current_user.school_code).first().teachers)
    teachers_lesson = {}
    for teacher_nc in school_teachers:
        teachers_lesson[teacher_nc] = Teacher.query.filter(Teacher.teacher_national_code==teacher_nc).first().lesson
    
    with open(file_path) as f:
        lines = f.readlines()[1:]

    for line in lines:
        content = line.split('|')
        date_time = content[2].split()
        date_obj = datetime.datetime.strptime(date_time[0], "%Y-%m-%d")
        weekday = date_obj.strftime("%A")
        times = class_schedule[weekday]

        for time_range in list(times.keys()):
            start_time = datetime.time.fromisoformat(time_range.split('-')[0])
            end_time = datetime.time.fromisoformat(time_range.split('-')[1])
            check_time = datetime.time.fromisoformat(date_time[1])

            if start_time <= check_time <= end_time:
                lesson = teachers_lesson[str(times[time_range])]
                if not (lesson in list(lessons.keys())):
                    lessons[lesson] = [0, 0]

                if content[0] == '5':
                    lessons[lesson][0] += 1
                lessons[lesson][1] += 1
    
    print(lessons)
    for lesson in lessons:
        value = lessons[lesson]
        try:
            score = (value[0] / value[1]) * 100
        except:
            score = 0
        
        lessons[lesson] = score

    return lessons
