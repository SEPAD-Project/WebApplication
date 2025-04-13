from app.models.school import School
from app.models.teacher import Teacher
from app.utils.excel_reading import schedule_extraction
from flask_login import current_user
from os import listdir
import glob
import datetime

def compare_teachers():
    school_dir = f"c:\sap-project\server\schools\{current_user.school_code}"

    teachers = {}
    school = School.query.filter(School.school_code == current_user.school_code).first()
    school_teachers = eval(school.teachers)
    for teacher_nc in school_teachers:
        teachers[teacher_nc] = [0, 0]

    print(teachers)

    for class_name in listdir(school_dir):
        class_dir = school_dir + f"\{class_name}"
        files_path = glob.glob(class_dir + "\*.txt")

        class_schedule = schedule_extraction(class_dir + "\schedule.xlsx", "Sheet1")

        for file_path in files_path:
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
                        if content[0] == '5': 
                            teachers[str(times[time_range])][0] += 1
                        teachers[str(times[time_range])][1] += 1


    for teacher_nc in school_teachers:
        value = teachers[teacher_nc]
        try:
            score = (value[0] / value[1]) * 100
        except:
            score = 0
        
        teacher = Teacher.query.filter(Teacher.teacher_national_code == teacher_nc).first()
        teachers[teacher.teacher_name+' '+teacher.teacher_family] = score
        teachers.pop(teacher.teacher_national_code)

    return teachers
