import plotly.express as px


def bar_style(fig, title, x_title, y_title):
    """
    Apply consistent dark theme styling to bar charts.

    Args:
        fig: Plotly figure object to style.
        title (str): Chart title.
        x_title (str): X-axis label.
        y_title (str): Y-axis label.

    Returns:
        plotly.graph_objs.Figure: Styled figure.
    """
    fig.update_traces(
        texttemplate='%{text:.0f}',  # Round displayed values
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
    """
    Apply consistent dark theme styling to line charts.

    Args:
        fig: Plotly figure object to style.
        title (str): Chart title.
        x_title (str): X-axis label.
        y_title (str): Y-axis label.

    Returns:
        plotly.graph_objs.Figure: Styled figure.
    """
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


def show_classes_accuracy(classes: dict):
    """
    Create and save a bar chart comparing accuracy across classes.

    Args:
        classes (dict): Mapping from class names to scores (e.g., accuracy %).
    """
    fig = px.bar(
        x=list(classes.keys()),
        y=list(classes.values()),
        text=list(classes.values())
    )
    fig = bar_style(fig, "Compare Classes", "Class Code", "Score")
    fig.write_image(r"c:\sap-project\server\compare_classes.pdf", format="pdf", scale=2)


def show_students_accuracy(students: dict):
    """
    Create and save a bar chart comparing accuracy across students.

    Args:
        students (dict): Mapping from student names to scores (e.g., accuracy %).
    """
    fig = px.bar(
        x=list(students.keys()),
        y=list(students.values()),
        text=list(students.values())
    )
    fig = bar_style(fig, "Compare Students", "Student Name", "Score")
    fig.write_image(r"c:\sap-project\server\compare_students.pdf", format="pdf")




def show_teachers_performance(teachers: dict):
    """
    Generate and save a bar chart comparing teacher performance.

    Args:
        teachers (dict): Mapping from teacher names to performance scores.
    """
    fig = px.bar(
        x=list(teachers.keys()),
        y=list(teachers.values()),
        text=list(teachers.values())
    )
    fig = bar_style(fig, "Compare Teachers", "Teacher Name", "Score")
    fig.write_image(r"c:\sap-project\server\compare_teachers.pdf", format="pdf")


def show_student_weekly_accuracy(student_name: str, accuracy: dict):
    """
    Generate and save a line chart of a student's daily accuracy over a week.

    Args:
        student_name (str): Name of the student for chart title.
        accuracy (dict): Mapping from weekday to accuracy percentage.
    """
    fig = px.line(
        x=list(accuracy.keys()),
        y=list(accuracy.values()),
        markers=True,
        labels={'x': 'Day', 'y': 'Accuracy (%)'}
    )
    fig = line_style(
        fig, f"{student_name}'s Weekly Accuracy", "Day", "Accuracy (%)")
    fig.write_image(r"c:\sap-project\server\student_accuracy_week.pdf", format="pdf")


def show_student_accuracy_by_lesson(student_name: str, lessons: dict):
    """
    Generate and save a bar chart showing student's accuracy by lesson.

    Args:
        student_name (str): Name of the student.
        lessons (dict): Mapping from lesson names to accuracy percentages.
    """
    fig = px.bar(
        x=list(lessons.keys()),
        y=list(lessons.values()),
        text=list(lessons.values())
    )
    fig = bar_style(
        fig, f"{student_name}'s Lesson Accuracy", "Lesson", "Score")
    fig.write_image(r"c:\sap-project\server\student_accuracy_by_lesson.pdf", format="pdf")


# --- Example usage / standalone test ---
if __name__ == "__main__":
    # Sample class performance
    show_classes_accuracy({
        '1051': 25.5, '1052': 84.3, '1053': 56.7, '1054': 96.3
    })

    # Sample student performance
    show_students_accuracy({
        'Alex': 82.5, 'John': 75.2, 'Emma': 91.8, 'Max': 68.4,
        'Liam': 85.0, 'Sophia': 88.6, 'Ryan': 79.3, 'Mia': 92.1
    })

    # Sample student weekly accuracy
    show_student_weekly_accuracy("Parsa Safaie", {
        'Monday': 85.5, 'Tuesday': 87.2, 'Wednesday': 88.1,
        'Thursday': 90.4, 'Friday': 92.3, 'Saturday': 91.5, 'Sunday': 89.0
    })

    # Sample teacher performance
    show_teachers_performance({
        'Mr. Lee': 92.5, 'Ms. Kim': 87.3, 'Mr. Ray': 78.4,
        'Mrs. Fox': 84.1, 'Mr. Jay': 90.2, 'Ms. Zoe': 76.9
    })

    # Sample lesson accuracy
    show_student_accuracy_by_lesson("Parsa Safaie", {
        "Math": 88.5, "Physics": 92.3, "Chemistry": 85.7,
        "Biology": 79.6, "English": 90.1, "Computer": 95.4
    })
    