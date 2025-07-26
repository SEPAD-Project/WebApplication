from source.utils.analytics.Generator.analytics_Generator import (
    calculate_students_accuracy,
    calculate_classes_accuracy,
    calculate_teachers_performance,
    calculate_student_weekly_accuracy,
    calculate_student_accuracy_by_lesson,
)

# Chart generation
from source.utils.analytics.GUI.analytics_GUI import (
    show_students_accuracy,
    show_classes_accuracy,
    show_teachers_performance,
    show_student_weekly_accuracy,
    show_student_accuracy_by_lesson,
)

from source.server_side.Website.Email.analytics_sender import send_analytics_email
from source import celery

@celery.task
def start_process_compare_students(school_id ,class_id, school_email):
    # Generate accuracy data and save the chart
    data = calculate_students_accuracy(str(school_id), str(class_id))
    show_students_accuracy(data)

    send_analytics_email(school_email, 'Compare Students', r"c:\sap-project\server\compare_students.pdf")

@celery.task
def start_process_compare_classes(school_id, school_email):
    # Generate accuracy data and save the chart
    data = calculate_classes_accuracy(str(school_id))
    show_classes_accuracy(data)

    send_analytics_email(school_email, 'Compare Classes', r"c:\sap-project\server\compare_classes.pdf")

@celery.task
def start_process_compare_teachers(school_id, school_email):
    # Generate accuracy data and save the chart
    data = calculate_teachers_performance(str(school_id))
    show_teachers_performance(data)

    send_analytics_email(school_email, 'Compare Teachers', r"c:\sap-project\server\compare_teachers.pdf")

@celery.task
def start_process_student_accuracy_week(school_id, name, family, national_code, class_id, school_email):
    # Generate accuracy data and save the chart
    data = calculate_student_weekly_accuracy(str(school_id), str(class_id), str(national_code))
    show_student_weekly_accuracy(f"{name} {family}", data)

    send_analytics_email(school_email, 'Weekly Accuracy ', r"c:\sap-project\server\student_accuracy_week.pdf")

@celery.task
def start_process_compare_student_accuracy_by_lesson(school_id, name, family, national_code, class_id, school_email):
    # Calculate per-lesson accuracy and generate chart
    data = calculate_student_accuracy_by_lesson(str(school_id), str(class_id), str(national_code))
    show_student_accuracy_by_lesson(f"{name} {family}", data)

    send_analytics_email(school_email, 'Accuracy by Lesson', r"c:\sap-project\server\student_accuracy_by_lesson.pdf")