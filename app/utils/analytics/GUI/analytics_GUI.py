import plotly.express as px


def bar_style(fig, title, x_title, y_title):
    """
    Apply consistent styling to bar charts with dark theme.

    Args:
        fig: Plotly figure object
        title: Chart title text
        x_title: X-axis label
        y_title: Y-axis label

    Returns:
        Styled Plotly figure
    """
    # Update bar appearance
    fig.update_traces(
        texttemplate='%{text:.0f}',  # Display whole numbers
        textposition='outside',      # Place labels above bars
        marker_color='#4ECDC4',     # Teal color for bars
    )

    # Update overall layout
    fig.update_layout(
        width=1300,
        height=600,
        autosize=False,
        bargap=0.5,  # Spacing between bars

        # Title styling
        title=dict(
            text=title,
            font=dict(size=27, color='white', family='sans-serif'),
            xanchor='center',
            x=0.5  # Center title
        ),

        # Global font settings
        font=dict(size=14, color='white', family='sans-serif'),

        # Dark theme colors
        plot_bgcolor='#1E1E1E',    # Chart background
        paper_bgcolor='#1E1E1E',   # Surrounding area

        # X-axis styling
        xaxis=dict(
            title=dict(text=x_title, font=dict(color='white')),
            showgrid=False,        # No grid lines
            tickfont=dict(color='white'),
            linecolor='grey',      # Axis line color
            ticks='outside',       # Ticks point outward
        ),

        # Y-axis styling
        yaxis=dict(
            title=dict(text=y_title, font=dict(color='white')),
            gridcolor='#444',     # Subtle grid lines
            zeroline=False,       # No zero line
            tickfont=dict(color='white'),
            linecolor='grey'      # Axis line color
        ),
    )
    return fig


def line_style(fig, title, x_title, y_title):
    """
    Apply consistent styling to line charts with dark theme.

    Args:
        fig: Plotly figure object
        title: Chart title text
        x_title: X-axis label
        y_title: Y-axis label

    Returns:
        Styled Plotly figure
    """
    # Set line color
    fig.update_traces(line=dict(color='#4ECDC4'))

    # Update layout with same dark theme as bar charts
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
    Generate and save a bar chart comparing class performance.

    This function creates a bar chart visualizing the scores of different classes.
    The chart is styled using the `bar_style` function for consistent dark theme formatting.
    The output is saved as a PDF file for easy sharing or reporting.

    Args:
        classes: Dictionary of {class_name: score}, where class_name is the label 
                and score represents the performance metric (e.g., accuracy, grades).
    """
    fig = px.bar(
        x=list(classes.keys()),
        y=list(classes.values()),
        text=list(classes.values())  # Display scores on bars
    )
    fig = bar_style(fig, "Compare Classes", "Class Code", "Score")
    fig.write_image(r"c:\sap-project\server\compare_classes.pdf",
                    format="pdf", scale=2)


def show_students_accuracy(students: dict):
    """
    Generate and save a bar chart comparing student performance.

    This function visualizes the scores of individual students in a bar chart.
    It uses the `bar_style` function to ensure a consistent dark theme appearance.
    The chart is exported as a PDF file for further use.

    Args:
        students: Dictionary of {student_name: score}, where student_name is the label 
                  and score represents the performance metric (e.g., test scores, grades).
    """
    fig = px.bar(
        x=list(students.keys()),
        y=list(students.values()),
        text=list(students.values())
    )
    fig = bar_style(fig, "Compare Students", "Student Name", "Score")
    fig.write_image(
        r"c:\sap-project\server\compare_students.pdf", format="pdf")


def show_teachers_performance(teachers: dict):
    """
    Generate and save a bar chart comparing teacher performance.

    This function creates a bar chart to compare the performance metrics of teachers.
    The chart is styled using the `bar_style` function for a professional dark theme look.
    The final chart is saved as a PDF file.

    Args:
        teachers: Dictionary of {teacher_name: score}, where teacher_name is the label 
                  and score represents the performance metric (e.g., evaluation scores).
    """
    fig = px.bar(
        x=list(teachers.keys()),
        y=list(teachers.values()),
        text=list(teachers.values())
    )
    fig = bar_style(fig, "Compare Teachers", "Teacher Name", "Score")
    fig.write_image(
        r"c:\sap-project\server\compare_teachers.pdf", format="pdf")


def show_student_weekly_accuracy(student_name: str, accuracy: dict):
    """
    Generate and save a line chart of a student's weekly accuracy.

    This function visualizes the daily accuracy of a student over a week using a line chart.
    Markers are included for clarity, and the chart is styled with the `line_style` function 
    for a clean, dark-themed appearance. The result is exported as a PDF.

    Args:
        student_name: Name of the student, used in the chart title.
        accuracy: Dictionary of {weekday: accuracy_score}, where weekday is the day of the week 
                  and accuracy_score represents the daily performance metric.
    """
    fig = px.line(
        x=list(accuracy.keys()),
        y=list(accuracy.values()),
        markers=True,  # Highlight data points
        labels={'x': 'Day', 'y': 'Accuracy (%)'}
    )
    fig = line_style(
        fig, f"{student_name}'s Weekly Accuracy", "Day", "Accuracy (%)")
    fig.write_image(
        r"c:\sap-project\server\student_accuracy_week.pdf", format="pdf")


def show_student_accuracy_by_lesson(student_name: str, lessons: dict):
    """
    Generate and save a bar chart of a student's accuracy by lesson.

    This function creates a bar chart to display the accuracy of a student across different lessons.
    The chart is styled using the `bar_style` function for consistency and professionalism.
    The output is saved as a PDF file for easy access and sharing.

    Args:
        student_name: Name of the student, used in the chart title.
        lessons: Dictionary of {lesson_name: accuracy_score}, where lesson_name is the subject 
                 and accuracy_score represents the performance metric for that lesson.
    """
    fig = px.bar(
        x=list(lessons.keys()),
        y=list(lessons.values()),
        text=list(lessons.values())
    )
    fig = bar_style(
        fig, f"{student_name}'s Lesson Accuracy", "Lesson", "Score")
    fig.write_image(
        r"c:\sap-project\server\student_accuracy_by_lesson.pdf", format="pdf")


if __name__ == "__main__":
    # Sample data demonstrations
    show_classes_accuracy({'1051': 25.5, '1052': 84.3,
                           '1053': 56.7, '1054': 96.3})

    show_students_accuracy({
        'Alex': 82.5, 'John': 75.2, 'Emma': 91.8, 'Max': 68.4,
        'Liam': 85.0, 'Sophia': 88.6, 'Ryan': 79.3, 'Mia': 92.1
    })

    show_student_weekly_accuracy("Parsa Safaie", {
        'Monday': 85.5, 'Tuesday': 87.2, 'Wednesday': 88.1,
        'Thursday': 90.4, 'Friday': 92.3, 'Saturday': 91.5, 'Sunday': 89.0
    })

    show_teachers_performance({
        'Mr. Lee': 92.5, 'Ms. Kim': 87.3, 'Mr. Ray': 78.4,
        'Mrs. Fox': 84.1, 'Mr. Jay': 90.2, 'Ms. Zoe': 76.9
    })

    show_student_accuracy_by_lesson("Parsa Safaie", {
        "Math": 88.5, "Physics": 92.3, "Chemistry": 85.7,
        "Biology": 79.6, "English": 90.1, "Computer": 95.4
    })
