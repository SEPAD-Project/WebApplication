from flask import Flask, render_template

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def go_to_home():
    return render_template('home.html')

@app.route('/login')
def go_to_login():
    return render_template('login.html')

@app.route('/signup')
def go_to_signup():
    return render_template('signup.html')

@app.route('/notify_user')
def go_to_notify_user():
    return render_template('notif_username_password_on_signup.html')

@app.route('/panel_home')
def go_to_panel_home():
    return render_template('management_panel/home.html')

@app.route('/panel_school_info')
def go_to_panel_school_info():
    return render_template('management_panel/school_info.html')

@app.route('/panel_classes')
def go_to_panel_classes():
    return render_template('management_panel/classes.html')

@app.route('/panel_teachers')
def go_to_panel_teachers():
    return render_template('management_panel/teachers.html')

@app.route('/panel_students')
def go_to_panel_students():
    return render_template('management_panel/students.html')

if __name__ == '__main__':
    app.run(debug=True)
