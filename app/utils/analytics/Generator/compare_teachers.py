from app.models.school import School
from app.models.teacher import Teacher
from flask_login import current_user
from os import listdir
import glob

def compare_teachers():
    school_dir = f"c:\sap-project\server\schools\{current_user.school_code}"

    teachers = {}
    school = School.query.filter(School.school_code == current_user.school_code).first()
    school_teachers = eval(school.teachers)
    for teacher_nc in school_teachers:
        teachers[teacher_nc] = [0, 0]

    for class_name in listdir(school_dir):
        class_dir = school_dir + f"\{class_name}"
        files_path = glob.glob(class_dir + "\*.txt")

        for file_path in files_path:
            with open(file_path) as f:
                lines = f.readlines()[1:]

            for line in lines:
                content = line.split('|')
                score = 1 if content[0] == '5' else 0
                teachers[content[4]][0] += score
                teachers[content[4]][1] += 1


    for teacher_nc in school_teachers:
        value = teachers[teacher_nc]
        score = (value[0] / value[1]) * 100
        
        teacher = Teacher.query.filter(Teacher.teacher_national_code == teacher_nc).first()
        teachers[teacher.teacher_name+' '+teacher.teacher_family] = score
        teachers.pop(teacher.teacher_national_code)

    return teachers
