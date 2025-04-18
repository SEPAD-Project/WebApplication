import datetime
import os
import glob

from flask_login import current_user

# Model imports
from app.models.models import *

# Utility imports
from app.utils.excel_reading import schedule_extraction
from app.utils.generate_class_code import generate_class_code


def calculate_students_accuracy(class_name):
    """
    Calculate and compare the accuracy percentages of students in a given class
    based on their result files.

    This function reads each student's result file (in txt format), processes the data,
    and calculates their accuracy percentage. The results are returned as a dictionary
    mapping student names to their accuracy percentages.

    Args:
        class_name (str): The name of the class to evaluate students from

    Returns:
        dict: A dictionary where keys are student names and values are their 
              accuracy percentages (0-100)

    Example:
        >>> Generator_compare_students("10A")
        {'John Doe': 85.5, 'Jane Smith': 92.3}
    """
    # Base path where student result files are stored
    BASE_PATH = f"c:\sap-project\server\schools\{current_user.school_code}\{class_name}"

    # Dictionary to store accuracy percentages by student name
    students_accuracy = {}

    # Generate the class code and get all students in this class
    class_code = generate_class_code(current_user.school_code, class_name)
    students = Student.query.filter(Student.class_code == class_code).all()

    for student in students:
        # Construct the file path for each student's result file
        file_path = BASE_PATH + f"\{student.student_national_code}.txt"

        # Read and process the result file
        with open(file_path, 'r') as file:
            # Skip header line and extract the first part of each result (before '|=|')
            results = [result.split('|=|')[0]
                       for result in file.readlines()[1:]]

        # Convert results to binary values (1 for '5', 0 otherwise)
        for index, content in enumerate(results):
            if content == '5':
                results[index] = 1  # Correct answer
            else:
                results[index] = 0  # Incorrect answer

        # Calculate accuracy percentage and store in dictionary
        students_accuracy[student.student_name] = (
            sum(results) / len(results)) * 100

    return students_accuracy


def calculate_classes_accuracy():
    """
    Calculate the average accuracy percentage for all classes in the current user's school.

    This function:
    1. Retrieves all classes in the current school
    2. For each class, gets individual student accuracies
    3. Calculates the class average accuracy
    4. Returns a dictionary of class names to their average accuracy

    Returns:
        dict: A dictionary mapping class names to their average accuracy percentages (0-100).
              Returns 0 for classes with no students.

    Example:
        >>> calculate_class_accuracy()
        {'10A': 78.5, '10B': 85.2, '11A': 72.8}
    """
    classes_accuracy = {}  # Dictionary to store results

    # Get all class names in the current school
    classes = [
        class_.class_name
        for class_ in Class.query.filter(
            Class.school_code == current_user.school_code
        ).all()
    ]

    for class_name in classes:
        # Get accuracy percentages for all students in this class
        student_accuracies = list(
            calculate_students_accuracy(class_name).values())

        # Handle empty classes (avoid division by zero)
        if not student_accuracies:
            classes_accuracy[class_name] = 0
            continue

        # Calculate class average accuracy
        classes_accuracy[class_name] = sum(
            student_accuracies) / len(student_accuracies)

    return classes_accuracy


def calculate_teachers_performance():
    """
    Calculate teacher performance metrics based on student result files.

    Processes student result files across all classes to determine:
    - Number of correct results (code '5')
    - Total result attempts
    for each teacher based on their scheduled class times.

    Returns:
        dict: Teacher national codes mapped to [correct_codes, total_codes]
    """
    # Use raw string for Windows paths and os.path.join for path construction
    school_dir = f"c:\sap-project\server\schools\{current_user.school_code}"

    # Initialize teacher tracking dictionary
    teachers_performance = {}

    # Get all teachers in the school
    school = School.query.filter(
        School.school_code == current_user.school_code
    ).first()

    # Convert string representation of list to actual list
    teacher_codes = eval(school.teachers) if school.teachers else []

    # Initialize counters for each teacher: [correct_codes, total_codes]
    for teacher_code in teacher_codes:
        teachers_performance[teacher_code] = [0, 0]

    # Process each class directory
    for class_name in os.listdir(school_dir):
        class_dir = os.path.join(school_dir, class_name)

        # Skip if not a directory
        if not os.path.isdir(class_dir):
            continue

        # Get all student result files
        result_files = glob.glob(os.path.join(class_dir, "*.txt"))

        # Load class schedule
        schedule_path = os.path.join(class_dir, "schedule.xlsx")
        try:
            class_schedule = schedule_extraction(schedule_path, "Sheet1")
        except FileNotFoundError:
            continue  # Skip if no schedule file

        # Process each student's result file
        for file_path in result_files:
            try:
                with open(file_path) as f:
                    # Skip header line
                    result_lines = f.readlines()[1:]
            except IOError:
                continue  # Skip unreadable files

            for line in result_lines:
                # Parse result data: result_code|=|datetime
                parts = line.strip().split('|=|')
                if len(parts) < 2:
                    continue  # Skip malformed lines

                result_code, datetime_str = parts
                date_str, time_str = datetime_str.split()

                try:
                    # Parse date and determine weekday
                    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    result_weekday = date_obj.strftime("%A")
                    result_time = datetime.time.fromisoformat(time_str)
                except ValueError:
                    continue  # Skip invalid date/time formats

                # Check scheduled time slots for this weekday
                for time_range, teacher_code in class_schedule.get(result_weekday, {}).items():
                    try:
                        start_str, end_str = time_range.split('-')
                        start_time = datetime.time.fromisoformat(start_str)
                        end_time = datetime.time.fromisoformat(end_str)
                    except ValueError:
                        continue  # Skip invalid time ranges

                    # If result date and time falls within this time slot
                    if start_time <= result_time <= end_time:
                        teacher_code = str(teacher_code)
                        # Count correct result code (code '5')
                        if result_code == '5':
                            teachers_performance[teacher_code][0] += 1
                        # Count total result codes
                        teachers_performance[teacher_code][1] += 1

    # Create a mapping from teacher codes to their full names
    teacher_name_map = {
        teacher_nc: f"{teacher.teacher_name} {teacher.teacher_family}"
        for teacher_nc in teacher_codes
        if (teacher := Teacher.query.filter(
            Teacher.teacher_national_code == teacher_nc
        ).first())
    }

    # Calculate and transform the performance data
    final_performance = {}
    for teacher_nc, (correct, total) in teachers_performance.items():
        if teacher_nc not in teacher_name_map:
            continue  # Skip if teacher not found

        try:
            score = (correct / total) * 100 if total > 0 else 0
        except ZeroDivisionError:
            score = 0

        full_name = teacher_name_map[teacher_nc]
        final_performance[full_name] = round(score, 2)

    return final_performance


def calculate_student_accuracy_by_lesson(class_name, national_code):
    """
    Calculate a student's performance by lesson based on their result files.

    Args:
        class_name (str): The name of the student's class
        national_code (str): The student's national identification code

    Returns:
        dict: Lesson names mapped to performance percentages (0-100)
    """
    # Use raw strings for Windows paths and os.path.join for path construction
    base_dir = f"c:\sap-project\server\schools\{current_user.school_code}\{class_name}"
    result_file = os.path.join(base_dir, f"{national_code}.txt")
    schedule_file = os.path.join(base_dir, "schedule.xlsx")

    # Initialize lessons tracking dictionary
    lessons_performance = {}

    try:
        # Load class schedule
        class_schedule = schedule_extraction(schedule_file, 'Sheet1')
    except FileNotFoundError:
        return {}  # Return empty if schedule missing

    # Get all teachers and their lessons in one query
    school = School.query.filter(
        School.school_code == current_user.school_code).first()
    teacher_codes = eval(school.teachers) if school.teachers else []

    # Create teacher-lesson mapping
    teachers = Teacher.query.filter(
        Teacher.teacher_national_code.in_(teacher_codes)).all()
    teacher_lesson_map = {t.teacher_national_code: t.lesson for t in teachers}

    try:
        with open(result_file) as f:
            result_lines = f.readlines()[1:]  # Skip header
    except IOError:
        return {}  # Return empty if answer file missing

    for line in result_lines:
        parts = line.strip().split('|=|')
        if len(parts) < 2:
            continue  # Skip malformed lines

        result_code, datetime_str = parts
        try:
            date_str, time_str = datetime_str.split()
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            result_weekday = date_obj.strftime("%A")
            result__time = datetime.time.fromisoformat(time_str)
        except ValueError:
            continue  # Skip invalid date/time

        # Check scheduled time slots for this weekday
        for time_range, teacher_code in class_schedule.get(result_weekday, {}).items():
            try:
                start_str, end_str = time_range.split('-')
                start_time = datetime.time.fromisoformat(start_str)
                end_time = datetime.time.fromisoformat(end_str)
            except ValueError:
                continue  # Skip invalid time ranges

            if start_time <= result__time <= end_time:
                lesson = teacher_lesson_map.get(str(teacher_code))
                if lesson:
                    # Initialize lesson tracking if not exists
                    if lesson not in lessons_performance:
                        lessons_performance[lesson] = [
                            0, 0]  # [correct, total]

                    # Count answers
                    if result_code == '5':
                        lessons_performance[lesson][0] += 1
                    lessons_performance[lesson][1] += 1

    # Calculate final percentages
    for lesson, (correct, total) in lessons_performance.items():
        try:
            lessons_performance[lesson] = round((correct / total) * 100, 2)
        except ZeroDivisionError:
            lessons_performance[lesson] = 0.0

    return lessons_performance


def calculate_student_weekly_accuracy(class_name, national_code):
    """
    Calculate a student's daily accuracy over the past week.

    Args:
        class_name (str): The student's class name
        national_code (str): The student's national ID code

    Returns:
        dict: Dates (YYYY-MM-DD) mapped to daily performance percentages (0-100)
              for the past 7 days (including today)
    """
    # Construct file path using os.path.join for cross-platform compatibility
    file_path = os.path.join(
        f"c:\sap-project\server\schools\{current_user.school_code}",
        class_name,
        f"{national_code}.txt"
    )

    # Generate dates for the past week (today + previous 6 days)
    today = datetime.date.today()
    date_range = [today - datetime.timedelta(days=i) for i in range(7)]
    date_strings = [d.strftime("%Y-%m-%d") for d in date_range]

    # Initialize daily performance tracking
    daily_performance = {date: [0, 0]
                         for date in date_strings}  # [correct, total]

    try:
        with open(file_path, 'r') as f:
            for line in f.readlines()[1:]:  # Skip header line
                parts = line.strip().split('|=|')
                if len(parts) < 2:
                    continue  # Skip malformed lines

                result_code, _, datetime_str = parts
                result_date = datetime_str.split()[0]

                if result_date in daily_performance:
                    # Count correct answers (code '5') and total answers
                    if result_code == '5':
                        daily_performance[result_date][0] += 1
                    daily_performance[result_date][1] += 1

    except FileNotFoundError:
        # Return zeros if file missing
        return {date: 0.0 for date in date_strings}

    # Calculate percentages
    for date, (correct, total) in daily_performance.items():
        try:
            daily_performance[date] = round((correct / total) * 100, 2)
        except ZeroDivisionError:
            daily_performance[date] = 0.0

    return daily_performance
