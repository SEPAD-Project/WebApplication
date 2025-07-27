from celery import shared_task
from utils.analytics.Generator.analytics_Generator import (
    compute_class_students_accuracy,
    compute_school_classes_accuracy,
    compute_school_teachers_performance,
    compute_student_accuracy_by_week,
    compute_student_accuracy_by_lesson,
)
from utils.analytics.GUI.analytics_GUI import (
    visualize_class_accuracy,
    visualize_class_students_accuracy,
    visualize_teacher_performance,
    visualize_student_accuracy_by_week,
    visualize_student_accuracy_by_lesson,
)
from utils.server.Website.Email.analytics_sender import send_analytics_email


@shared_task
def task_generate_class_students_accuracy(school_id, class_id, school_email):
    data = compute_class_students_accuracy(school_id, class_id)
    pdf_bytes = visualize_class_students_accuracy(data)
    send_analytics_email(
        receiver=school_email,
        subject='Student Accuracy Comparison',
        pdf_bytes=pdf_bytes,
        filename='class_students_accuracy.pdf'
    )


@shared_task
def task_generate_school_classes_accuracy(school_id, school_email):
    data = compute_school_classes_accuracy(school_id)
    pdf_bytes = visualize_class_accuracy(data)
    send_analytics_email(
        receiver=school_email,
        subject='Class Accuracy Comparison',
        pdf_bytes=pdf_bytes,
        filename='class_accuracy.pdf'
    )


@shared_task
def task_generate_school_teachers_performance(school_id, school_email):
    data = compute_school_teachers_performance(school_id)
    pdf_bytes = visualize_teacher_performance(data)
    send_analytics_email(
        receiver=school_email,
        subject='Teacher Performance Comparison',
        pdf_bytes=pdf_bytes,
        filename='teacher_performance.pdf'
    )


@shared_task
def task_generate_student_accuracy_by_week(school_id, name, family, national_code, class_id, school_email):
    student_name = f"{name} {family}"
    data = compute_student_accuracy_by_week(school_id, class_id, national_code)
    pdf_bytes = visualize_student_accuracy_by_week(student_name, data)
    send_analytics_email(
        receiver=school_email,
        subject=f"Weekly Accuracy - {student_name}",
        pdf_bytes=pdf_bytes,
        filename='student_accuracy_by_week.pdf'
    )


@shared_task
def task_generate_student_accuracy_by_lesson(school_id, name, family, national_code, class_id, school_email):
    student_name = f"{name} {family}"
    data = compute_student_accuracy_by_lesson(school_id, class_id, national_code)
    pdf_bytes = visualize_student_accuracy_by_lesson(student_name, data)
    send_analytics_email(
        receiver=school_email,
        subject=f"Lesson Accuracy - {student_name}",
        pdf_bytes=pdf_bytes,
        filename='student_accuracy_by_lesson.pdf'
    )
