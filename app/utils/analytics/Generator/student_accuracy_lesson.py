from flask_login import current_user

def student_lessons(class_name, national_code):
    file_path = f"c:\sap-project\server\schools\{current_user.school_code}\{class_name}\{national_code}.txt"
    lessons = {}

    with open(file_path, 'r') as f:
        lines = f.readlines()[1:]

    for line in lines:
        content = line.split('|')
        lesson = content[6].rstrip('\n')
        if not (lesson in list(lessons.keys())):
            lessons[lesson] = [0, 0]
        if content[0] == '5':
            lessons[lesson][0] += 1
        lessons[lesson][1] +=  1

    for lesson in lessons:
        lessons[lesson] = (lessons[lesson][0] / lessons[lesson][1]) * 100

    return lessons
