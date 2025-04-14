import plotly.express as px

def bar_style(fig ,title, x_title, y_title):
    fig.update_traces(
        texttemplate='%{text:.0f}',
        textposition='outside',
        marker_color='#4ECDC4',
    )

    fig.update_layout(
        width=1300,
        height=600,
        autosize=False,
        bargap=0.5,

        title=dict(
            text=title,
            font=dict(size=27, color='white', family='sans-serif'),
            xanchor='center',
            x=0.5
        ),

        font=dict(size=14, color='white', family='sans-serif'),

        plot_bgcolor='#1E1E1E',
        paper_bgcolor='#1E1E1E',

        xaxis=dict(
            title=dict(text=x_title, font=dict(color='white')),
            showgrid=False,
            tickfont=dict(color='white'),
            linecolor='grey',
            ticks='outside',
        ),

        yaxis=dict(
            title=dict(text=y_title, font=dict(color='white')),
            gridcolor='#444',
            zeroline=False,
            tickfont=dict(color='white'),
            linecolor='grey'
        ),
    )

    return fig
 

 #==================================================


def line_style(fig ,title, x_title, y_title):
    fig.update_traces(line=dict(color='#4ECDC4'))

    fig.update_layout(
        width=1300,
        height=600,
        autosize=False,
        
        title=dict(
            text=title,
            font=dict(size=22, color='white', family='sans-serif'),
            xanchor='center',
            x=0.5
        ),

        font=dict(size=14, color='white', family='sans-serif'),

        plot_bgcolor='#1E1E1E',
        paper_bgcolor='#1E1E1E',

        xaxis=dict(
            title=dict(text=x_title, font=dict(color='white')),
            showgrid=False,
            tickfont=dict(color='white'),
            linecolor='grey',
            ticks='outside',
        ),

        yaxis=dict(
            title=dict(text=y_title, font=dict(color='white')),
            gridcolor='#444',
            zeroline=False,
            tickfont=dict(color='white'),
            linecolor='grey'
        ),

    )

    return fig


 #==================================================


def GUI_compare_classes(classes: dict):
    fig = px.bar(
        x=list(classes.keys()),
        y=list(classes.values()),
        text=list(classes.values()),
        title="Compare Classes"
    )

    fig = bar_style(fig, title="Compare Classes", x_title="Class Code", y_title="Score")

    fig.write_image("c:\sap-project\server\compare_classes.pdf", format="pdf", scale=2)


 #==================================================


def GUI_compare_students(students: dict):
    fig = px.bar(
        x=list(students.keys()),
        y=list(students.values()),
        text=list(students.values()),
        title="Compare Students"
    )

    fig = bar_style(fig, title="Compare Students", x_title="Student Name", y_title="Score")

    fig.write_image("c:\sap-project\server\compare_students.pdf", format="pdf")


 #==================================================


def GUI_compare_teachers(teachers: dict):
    fig = px.bar(
        x=list(teachers.keys()),
        y=list(teachers.values()),
        text=list(teachers.values()),
        title="Compare Teachers"
    )

    fig = bar_style(fig, title="Compare Teachers", x_title="Teacher Name", y_title="Score")

    fig.write_image("c:\sap-project\server\compare_teachers.pdf", format="pdf")

 #==================================================


def GUI_student_accuracy_week(student_name:str, accuracy: dict):
    fig = px.line(
        x=list(accuracy.keys()),
        y=list(accuracy.values()),
        markers=True,
        title=f"'{student_name}' Accuracy Over the Week",
        labels={'x': 'Day', 'y': 'Accuracy (%)'}
    )

    fig = line_style(fig, title=f"'{student_name}' Accuracy Over the Week", x_title="Day", y_title="Accuracy (%)")

    fig.write_image("c:\sap-project\server\student_accuracy_week.pdf", format="pdf")


 #==================================================


def GUI_student_accuracy_by_lesson(student_name:str, lessons: dict):
    fig = px.bar(
        x=list(lessons.keys()),
        y=list(lessons.values()),
        text=list(lessons.values()),
        title=f"'{student_name}' Accuracy In Each Lesson"
    )

    fig = bar_style(fig, f"'{student_name}' Accuracy In Each Lesson", x_title="Lesson", y_title="Score")

    fig.write_image("c:\sap-project\server\student_accuracy_by_lesson.pdf", format="pdf")


if __name__=="__main__":
    GUI_compare_classes({'1051': 25.5, '1052': 84.3, '1053': 56.7, '1054': 96.3, '1051': 25.5, '1052': 84.3, '1053': 56.7, '1054': 96.3})

    GUI_compare_students({
    'Alex': 82.5, 'John': 75.2, 'Emma': 91.8, 'Max': 68.4, 'Liam': 85.0, 
    'Sophia': 88.6, 'Ryan': 79.3, 'Mia': 92.1, 'Noah': 67.5, 'James': 73.8, 
    'Ava': 84.2, 'Oliver': 77.9, 'Ella': 90.4, 'Jack': 69.1, 'Amelia': 81.3, 
    'Lucas': 89.7, 'Charlotte': 93.5, 'Ethan': 74.6, 'Zoe': 70.8, 'Ben': 78.3
    })

    GUI_student_accuracy_week("Parsa Safaie",
        {
        'Monday': 85.5, 'Tuesday': 87.2, 'Wednesday': 88.1, 'Thursday': 90.4,
        'Friday': 92.3, 'Saturday': 91.5, 'Sunday': 89.0
    })

    GUI_compare_teachers({'Mr. Lee': 92.5, 'Ms. Kim': 87.3, 'Mr. Ray': 78.4,
    'Mrs. Fox': 84.1, 'Mr. Jay': 90.2, 'Ms. Zoe': 76.9,
    'Mr. Tom': 88.0, 'Ms. Eve': 85.7, 'Mr. Dan': 91.3, 'Ms. Ana': 83.6
    })

    GUI_student_accuracy_by_lesson("Parsa Safaie", {
    "Math": 88.5, "Physics": 92.3, "Chemistry": 85.7,
    "Biology": 79.6, "English": 90.1, "Computer": 95.4,
    "History": 72.8, "Geography": 76.3, "Literature": 81.2, "Geometry": 84.0
    })


