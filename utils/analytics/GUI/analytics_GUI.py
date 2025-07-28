import plotly.express as px
import os
import platform

def get_base_path():
    system = platform.system().lower()
    if system == 'windows':
        return r"C:\sap-project\server\schools"
    else:
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, "sap-project", "server", "schools")


def bar_style(fig, title, x_title, y_title):
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


def line_style(fig, title, x_title, y_title):
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


def visualize_class_accuracy(classes: dict) -> bytes:
    fig = px.bar(
        x=list(classes.keys()),
        y=list(classes.values()),
        text=list(classes.values())
    )
    fig = bar_style(fig, "Class Accuracy Comparison", "Class Code", "Score")
    return fig.to_image(format="pdf", scale=2)


def visualize_class_students_accuracy(students: dict) -> bytes:
    fig = px.bar(
        x=list(students.keys()),
        y=list(students.values()),
        text=list(students.values())
    )
    fig = bar_style(fig, "Student Accuracy Comparison (by Class)", "Student Name", "Score")
    return fig.to_image(format="pdf", scale=2)


def visualize_teacher_performance(teachers: dict) -> bytes:
    fig = px.bar(
        x=list(teachers.keys()),
        y=list(teachers.values()),
        text=list(teachers.values())
    )
    fig = bar_style(fig, "Teacher Performance Comparison", "Teacher Name", "Score")
    return fig.to_image(format="pdf", scale=2)


def visualize_student_accuracy_by_week(student_name: str, accuracy: dict) -> bytes:
    fig = px.line(
        x=list(accuracy.keys()),
        y=list(accuracy.values()),
        markers=True,
        labels={'x': 'Day', 'y': 'Accuracy (%)'}
    )
    fig = line_style(fig, f"Weekly Accuracy for {student_name}", "Day", "Accuracy (%)")
    return fig.to_image(format="pdf", scale=2)


def visualize_student_accuracy_by_lesson(student_name: str, lessons: dict) -> bytes:
    print(lessons)
    fig = px.bar(
        x=list(lessons.keys()),
        y=list(lessons.values()),
        text=list(lessons.values())
    )
    fig = bar_style(fig, f"Accuracy by Lesson for {student_name}", "Lesson", "Score")
    return fig.to_image(format="pdf", scale=2)
