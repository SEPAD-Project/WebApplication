from app.utils.generate_class_code import generate_class_code
from flask_login import current_user
from app.models.student import Student

def compare_students(class_name):
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
