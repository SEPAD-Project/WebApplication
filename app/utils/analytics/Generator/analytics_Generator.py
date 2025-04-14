from app.utils.generate_class_code import generate_class_code
from flask_login import current_user
from app.models.student import Student
from app.models._class import Class
from app.models.school import School
from app.models.teacher import Teacher
from app.utils.excel_reading import schedule_extraction
from os import listdir
import glob
import datetime

def Generator_compare_students(class_name):
    BASE_PATH = f"c:\sap-project\server\schools\{current_user.school_code}\{class_name}"

    accuracy_by_student = {}
    
    class_code = generate_class_code(current_user.school_code, class_name)
    students = Student.query.filter(Student.class_code==class_code).all()

    for student in students:
        file_path = BASE_PATH+f"\{student.student_national_code}.txt"

        with open(file_path, 'r') as file:
            results = [result.split('|')[0] for result in file.readlines()[1:]]

        for index, content in enumerate(results):
            if content == '5':
                results[index] = 1
            else:
                results[index] = 0

        accuracy_by_student[student.student_name] = (sum(results) / len(results)) * 100

    return accuracy_by_student

def Generator_compare_classes():
    accuracy_by_class = {}

    classes = [class_.class_name for class_ in Class.query.filter(Class.school_code==current_user.school_code).all()]

    for class_ in classes:
        students_accuracy = list(Generator_compare_students(class_).values())

        if students_accuracy == []:
            accuracy_by_class[class_] = 0
            continue

        accuracy_by_class[class_] = sum(students_accuracy) / len(students_accuracy)

    return accuracy_by_class

def Generator_compare_teachers():
    school_dir = f"c:\sap-project\server\schools\{current_user.school_code}"

    teachers = {}
    school = School.query.filter(School.school_code == current_user.school_code).first()
    school_teachers = eval(school.teachers)
    for teacher_nc in school_teachers:
        teachers[teacher_nc] = [0, 0]

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

def Generator_student_lessons(class_name, national_code):
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
    
    for lesson in lessons:
        value = lessons[lesson]
        try:
            score = (value[0] / value[1]) * 100
        except:
            score = 0
        
        lessons[lesson] = score

    return lessons

def Generator_student_over_week(class_name, national_code):
    file_path = f"c:\sap-project\server\schools\{current_user.school_code}\{class_name}\{national_code}.txt"
    over_week = {}

    today = datetime.date.today()
    dates = [str(today.strftime("%Y-%m-%d"))]
    for i in range(1,7):
        dates.append(str((today-datetime.timedelta(i)).strftime("%Y-%m-%d")))

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
