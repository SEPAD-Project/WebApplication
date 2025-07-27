# Standard Library Imports
import os
import glob
import datetime
import platform

from classes.models import Class
from teachers.models import Teacher
from schools.models import School

from utils.excel_reading import schedule_extraction



def get_base_path():
    """Return appropriate paths based on the operating system"""
    system = platform.system().lower()
    
    if system == 'windows':
        return r"C:\sap-project\server\schools"
    else:
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, "sap-project", "server", "schools")
    

def compute_class_students_accuracy(school_id, class_id):
    """
    Calculate accuracy percentages for all students in a class based on their result files.

    Args:
        class_id (str): ID of the class to process.

    Returns:
        dict: Mapping of student full names to their accuracy percentage (0–100).
    """
    # Define base path to student result files
    base_path = os.path.join(get_base_path(), str(school_id), str(class_id))
    students_accuracy = {}

    # Fetch the class object
    class_ = Class.objects.get(id=class_id)

    # Iterate over students in the class
    for student in class_.students.all():
        file_path = os.path.join(base_path, f"{student.student_national_code}.txt")

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()[1:]  # Skip header
                # Convert each result to 1 if correct ('5'), else 0
                results = [1 if line.split(
                    '|=|')[0] == '5' else 0 for line in lines]

            # Calculate accuracy percentage
            accuracy = (sum(results) / len(results)) * 100

        except FileNotFoundError:
            # No result file found for this student
            accuracy = 0
        except ZeroDivisionError:
            # File exists but has no valid results
            accuracy = 0

        # Store result by student full name
        full_name = f"{student.student_name} {student.student_family}"
        students_accuracy[full_name] = accuracy

    return students_accuracy


def compute_school_classes_accuracy(school_id):
    """
    Calculate average accuracy percentage for each class in the current school.

    Returns:
        dict: Mapping of class names to their average accuracy (0–100).
    """
    classes_accuracy = {}

    # Fetch all classes that belong to the current school
    classes = School.objects.get(id=school_id).classes.all()

    for class_ in classes:
        # Get list of accuracy values for students in the class
        student_accuracies = list(
            compute_class_students_accuracy(class_.id).values()
        )

        if not student_accuracies:
            # Handle case where class has no valid student results
            classes_accuracy[class_.class_name] = 0
            continue

        # Calculate and store average class accuracy
        avg_accuracy = sum(student_accuracies) / len(student_accuracies)
        classes_accuracy[class_.class_name] = avg_accuracy

    return classes_accuracy


def compute_school_teachers_performance(school_id):
    """
    Calculate performance metrics for each teacher based on student result files.

    Returns:
        dict: Mapping from teacher full name to accuracy percentage (0–100).
    """
    school_dir = os.path.join(get_base_path(), str(school_id))
    teachers_performance = {}

    # Fetch all teachers for current school
    school = School.objects.get(id=school_id)
    teacher_codes = [t.teacher_national_code for t in school.teachers.all()]

    # Initialize performance counter for each teacher
    for teacher_code in teacher_codes:
        teachers_performance[teacher_code] = [0, 0]  # [correct, total]

    # Traverse class directories in the school directory
    for class_id in os.listdir(school_dir):
        class_dir = os.path.join(school_dir, class_id)

        if not os.path.isdir(class_dir):
            continue  # Skip files

        # Load class schedule (if exists)
        schedule_path = os.path.join(class_dir, "schedule.xlsx")
        try:
            class_schedule = schedule_extraction(schedule_path, "Sheet1")
        except FileNotFoundError:
            continue

        # Get all student result files (.txt)
        result_files = glob.glob(os.path.join(class_dir, "*.txt"))

        for file_path in result_files:
            try:
                with open(file_path, 'r') as f:
                    lines = f.readlines()[1:]  # Skip header
            except IOError:
                continue  # Skip unreadable files

            for line in lines:
                # Parse line into result and datetime
                parts = line.strip().split('|=|')
                if len(parts) < 2:
                    continue

                result_code, datetime_str = parts

                try:
                    date_str, time_str = datetime_str.split()
                    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    result_weekday = date_obj.strftime("%A")
                    result_time = datetime.time.fromisoformat(time_str)
                except ValueError:
                    continue  # Skip malformed date/time

                # Find which teacher was responsible at that time
                for time_range, teacher_code in class_schedule.get(result_weekday, {}).items():
                    if not (teacher_code in teachers_performance.keys):
                        continue
                    try:
                        start_str, end_str = time_range.split('-')
                        start_time = datetime.time.fromisoformat(start_str)
                        end_time = datetime.time.fromisoformat(end_str)
                    except ValueError:
                        continue  # Skip bad time ranges

                    # Check if result time falls in the range
                    if start_time <= result_time <= end_time:
                        teacher_code = str(teacher_code)

                        if result_code == '5':
                            # correct
                            teachers_performance[teacher_code][0] += 1
                        teachers_performance[teacher_code][1] += 1  # total

    # Map teacher codes to their full names
    teacher_name_map = {}
    for teacher in school.teachers.all():
        if teacher:
            teacher_name_map[teacher.teacher_national_code] = f"{teacher.teacher_name} {teacher.teacher_family}"

    # Compute final percentage performance
    final_performance = {}
    for teacher_nc, (correct, total) in teachers_performance.items():
        if teacher_nc not in teacher_name_map:
            continue

        score = (correct / total) * 100 if total > 0 else 0
        full_name = teacher_name_map[teacher_nc]
        final_performance[full_name] = round(score, 2)

    return final_performance


def compute_student_accuracy_by_lesson(school_id, class_id, student_national_code):
    """
    Calculate a student's answer accuracy by lesson, based on result timestamps.

    Args:
        class_id (str): ID of the class the student belongs to.
        student_national_code (str): ID of the student.

    Returns:
        dict: Mapping from lesson names to accuracy percentage (0–100).
    """
    base_dir = os.path.join(get_base_path(), str(school_id), str(class_id))
    result_file = os.path.join(base_dir, f"{student_national_code}.txt")
    schedule_file = os.path.join(base_dir, "schedule.xlsx")

    lessons_performance = {}

    # Load schedule for this class
    try:
        class_schedule = schedule_extraction(schedule_file, 'Sheet1')
    except FileNotFoundError:
        return {}

    # Get teacher → lesson map
    school = School.objects.get(id=school_id)
    teachers = school.teachers.all()
    teacher_lesson_map = {t.teacher_national_code: t.lesson for t in teachers}

    # Read result file
    try:
        with open(result_file) as f:
            result_lines = f.readlines()[1:]  # Skip header
    except IOError:
        return {}

    # Parse and assign each result to a lesson
    for line in result_lines:
        parts = line.strip().split('|=|')
        if len(parts) < 2:
            continue

        result_code, datetime_str = parts
        try:
            date_str, time_str = datetime_str.split()
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            result_weekday = date_obj.strftime("%A")
            result_time = datetime.time.fromisoformat(time_str)
        except ValueError:
            continue

        # Match result to time slot and teacher
        for time_range, teacher_code in class_schedule.get(result_weekday, {}).items():
            try:
                start_str, end_str = time_range.split('-')
                start_time = datetime.time.fromisoformat(start_str)
                end_time = datetime.time.fromisoformat(end_str)
            except ValueError:
                continue

            if start_time <= result_time <= end_time:
                lesson = teacher_lesson_map.get(str(teacher_code))
                if not lesson:
                    continue

                if lesson not in lessons_performance:
                    lessons_performance[lesson] = [0, 0]  # [correct, total]

                if result_code == '5':
                    lessons_performance[lesson][0] += 1  # correct
                lessons_performance[lesson][1] += 1  # total

    # Convert to percentage
    for lesson, (correct, total) in lessons_performance.items():
        try:
            lessons_performance[lesson] = round((correct / total) * 100, 2)
        except ZeroDivisionError:
            lessons_performance[lesson] = 0.0

    return lessons_performance


def compute_student_accuracy_by_week(school_id, class_id, student_national_code):
    """
    Calculate a student's answer accuracy for each day in the past week.

    Args:
        class_id (str): ID of the class the student belongs to.
        student_national_code (str): ID of the student.

    Returns:
        dict: Mapping from date (YYYY-MM-DD) to accuracy percentage (0–100).
    """
    # Build the path to the result file
    file_path = os.path.join(get_base_path(), str(school_id), str(class_id), f"{student_national_code}.txt"),

    # Generate past 7 days including today
    today = datetime.date.today()
    date_strings = [
        (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(7)
    ]

    # Initialize dictionary to track correct and total answers per day
    daily_performance = {date: [0, 0] for date in date_strings}

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()[1:]  # Skip header

            for line in lines:
                parts = line.strip().split('|=|')
                if len(parts) < 2:
                    continue

                result_code, datetime_str = parts
                result_date = datetime_str.split()[0]

                # Track performance if the date is in range
                if result_date in daily_performance:
                    if result_code == '5':
                        daily_performance[result_date][0] += 1  # correct
                    daily_performance[result_date][1] += 1     # total

    except FileNotFoundError:
        # If result file doesn't exist, return all 0.0s
        return {date: 0.0 for date in date_strings}

    # Convert [correct, total] to percentage
    for date, (correct, total) in daily_performance.items():
        daily_performance[date] = (
            round((correct / total) * 100, 2) if total > 0 else 0.0
        )

    return daily_performance
