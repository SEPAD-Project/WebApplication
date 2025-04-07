import plotly.express as px

def bar_style(fig ,title, x_title, y_title):
    fig.update_traces(
        texttemplate='%{text:.0f}',
        textposition='outside',
        marker_color='#4ECDC4',
    )

    fig.update_layout(
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


def compare_classes(classes: dict):
    fig = px.bar(
        x=list(classes.keys()),
        y=list(classes.values()),
        text=list(classes.values()),
        title="Compare Classes"
    )

    fig = bar_style(fig, title="Compare Classes", x_title="Class Code", y_title="Score")

    fig.write_html("compare_classes.html")

def compare_students(students: dict):
    fig = px.bar(
        x=list(students.keys()),
        y=list(students.values()),
        text=list(students.values()),
        title="Compare Students"
    )

    fig = bar_style(fig, title="Compare Students", x_title="Student Name", y_title="Score")

    fig.write_html("compare_students.html")


if __name__=="__main__":
    compare_classes({'1051': 25.5, '1052': 84.3, '1053': 56.7, '1054': 96.3, '1051': 25.5, '1052': 84.3, '1053': 56.7, '1054': 96.3})
    compare_students({
    'Alex': 82.5, 'John': 75.2, 'Emma': 91.8, 'Max': 68.4, 'Liam': 85.0, 
    'Sophia': 88.6, 'Ryan': 79.3, 'Mia': 92.1, 'Noah': 67.5, 'James': 73.8, 
    'Ava': 84.2, 'Oliver': 77.9, 'Ella': 90.4, 'Jack': 69.1, 'Amelia': 81.3, 
    'Lucas': 89.7, 'Charlotte': 93.5, 'Ethan': 74.6, 'Zoe': 70.8, 'Ben': 78.3
    })
