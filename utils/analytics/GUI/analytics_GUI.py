import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import os
import platform

def get_base_path():
    system = platform.system().lower()
    if system == 'windows':
        return r"C:\sap-project\server\schools"
    else:
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, "sap-project", "server", "schools")

def setup_plot_style(ax, title, x_title, y_title):
    # Set dark background style
    ax.set_facecolor('#1E1E1E')
    ax.figure.set_facecolor('#1E1E1E')
    
    # Set titles and labels
    ax.set_title(title, fontsize=27, color='white', pad=20)
    ax.set_xlabel(x_title, fontsize=14, color='white')
    ax.set_ylabel(y_title, fontsize=14, color='white')
    
    # Set tick colors
    ax.tick_params(colors='white', which='both')
    
    # Set spine colors
    for spine in ax.spines.values():
        spine.set_color('grey')
    
    # Set grid
    ax.grid(axis='y', color='#444', linestyle='-', alpha=0.3)
    
    return ax

def bar_style(ax, title, x_title, y_title):
    ax = setup_plot_style(ax, title, x_title, y_title)
    ax.grid(axis='y', color='#444', linestyle='-', alpha=0.3)
    return ax

def line_style(ax, title, x_title, y_title):
    ax = setup_plot_style(ax, title, x_title, y_title)
    ax.grid(axis='y', color='#444', linestyle='-', alpha=0.3)
    return ax

def visualize_class_accuracy(classes: dict) -> bytes:
    fig, ax = plt.subplots(figsize=(13, 6))
    
    x = list(classes.keys())
    y = list(classes.values())
    
    bars = ax.bar(x, y, color='#4ECDC4')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.0f}', ha='center', va='bottom', color='white')
    
    ax = bar_style(ax, "Class Accuracy Comparison", "Class Code", "Score")
    
    # Save to bytes buffer
    from io import BytesIO
    buf = BytesIO()
    fig.savefig(buf, format='pdf', facecolor='#1E1E1E', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()

def visualize_class_students_accuracy(students: dict) -> bytes:
    fig, ax = plt.subplots(figsize=(13, 6))
    
    x = list(students.keys())
    y = list(students.values())
    
    bars = ax.bar(x, y, color='#4ECDC4')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.0f}', ha='center', va='bottom', color='white')
    
    ax = bar_style(ax, "Student Accuracy Comparison (by Class)", "Student Name", "Score")
    
    # Rotate x-axis labels if they're long
    if max(len(str(label)) for label in x) > 5:
        plt.xticks(rotation=45, ha='right')
    
    # Save to bytes buffer
    from io import BytesIO
    buf = BytesIO()
    fig.savefig(buf, format='pdf', facecolor='#1E1E1E', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()

def visualize_teacher_performance(teachers: dict) -> bytes:
    fig, ax = plt.subplots(figsize=(13, 6))
    
    x = list(teachers.keys())
    y = list(teachers.values())
    
    bars = ax.bar(x, y, color='#4ECDC4')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.0f}', ha='center', va='bottom', color='white')
    
    ax = bar_style(ax, "Teacher Performance Comparison", "Teacher Name", "Score")
    
    # Rotate x-axis labels if they're long
    if max(len(str(label)) for label in x) > 5:
        plt.xticks(rotation=45, ha='right')
    
    # Save to bytes buffer
    from io import BytesIO
    buf = BytesIO()
    fig.savefig(buf, format='pdf', facecolor='#1E1E1E', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()

def visualize_student_accuracy_by_week(student_name: str, accuracy: dict) -> bytes:
    fig, ax = plt.subplots(figsize=(13, 6))
    
    x = list(accuracy.keys())
    y = list(accuracy.values())
    
    ax.plot(x, y, color='#4ECDC4', marker='o', linewidth=2, markersize=8)
    
    ax = line_style(ax, f"Weekly Accuracy for {student_name}", "Day", "Accuracy (%)")
    
    # Save to bytes buffer
    from io import BytesIO
    buf = BytesIO()
    fig.savefig(buf, format='pdf', facecolor='#1E1E1E', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()

def visualize_student_accuracy_by_lesson(student_name: str, lessons: dict) -> bytes:
    fig, ax = plt.subplots(figsize=(13, 6))
    
    x = list(lessons.keys())
    y = list(lessons.values())
    
    bars = ax.bar(x, y, color='#4ECDC4')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.0f}', ha='center', va='bottom', color='white')
    
    ax = bar_style(ax, f"Accuracy by Lesson for {student_name}", "Lesson", "Score")
    
    # Rotate x-axis labels if they're long
    if max(len(str(label)) for label in x) > 5:
        plt.xticks(rotation=45, ha='right')
    
    # Save to bytes buffer
    from io import BytesIO
    buf = BytesIO()
    fig.savefig(buf, format='pdf', facecolor='#1E1E1E', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()