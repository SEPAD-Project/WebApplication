from app.utils.analytics.Generator.compare_student import compare_students 
from flask_login import current_user
from app.models._class import Class

def compare_classes():
    accuracy_by_class = {}

    classes = [class_.class_name for class_ in Class.query.filter(Class.school_code==current_user.school_code).all()]

    for class_ in classes:
        students_accuracy = list(compare_students(class_).values())

        if students_accuracy == []:
            accuracy_by_class[class_] = 0
            continue

        accuracy_by_class[class_] = sum(students_accuracy) / len(students_accuracy)

    return accuracy_by_class