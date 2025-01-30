from flask import Flask, render_template, request, redirect, url_for, make_response, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql://root:sapprogram2583@185.4.28.110:5000/sap'
)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

db = SQLAlchemy(app)

class School(db.Model):
    __tablename__ = 'schools'
    
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(100), nullable=False)
    school_code = db.Column(db.String(100), nullable=False)
    manager_personal_code = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)

    def __init__(self, school_name, school_code, manager_personal_code, province, city):
        self.school_name = school_name
        self.school_code = school_code
        self.manager_personal_code = manager_personal_code
        self.province = province
        self.city = city

class Class(db.Model):
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100), nullable=False)
    class_code = db.Column(db.String(100), nullable=False)
    class_student_count = db.Column(db.String(100), nullable=False)
    school_code = db.Column(db.String(100), nullable=False)

    def __init__(self, class_name, class_code, class_students_count, school_code):
        self.class_name = class_name
        self.class_code = class_code
        self.class_student_count = class_students_count
        self.school_code = school_code

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def go_to_home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def go_to_login():
    try:
        school = School.query.filter(School.school_code == session['username']).first()
        manager_personal_code = school.manager_personal_code
        if manager_personal_code == session['password']:
                return redirect(url_for('go_to_panel_home'))
    except:
        pass
        
    if request.method == 'POST':
        given_school_code = request.form['username']
        given_manager_personal_code = request.form['password']

        school = School.query.filter(School.school_code == given_school_code).first()
        if school is None:
            return redirect(url_for('go_to_incorrect_username_password'))
        manager_personal_code = school.manager_personal_code

        session['username'] = given_school_code
        session['password'] = given_manager_personal_code
        
        if manager_personal_code == given_manager_personal_code:
            response = make_response("Cookie has been set!")
            response.set_cookie("username", given_school_code, max_age=60*60*24*7, httponly=True, samesite='Lax')  
            response.set_cookie("password", given_manager_personal_code, max_age=60*60*24*7, httponly=True, samesite='Lax')
            return redirect(url_for('go_to_panel_home'))
        else:
            return redirect(url_for('go_to_incorrect_username_password'))

    return render_template('login.html')

@app.route('/incorrect_username_password')
def go_to_incorrect_username_password():
    return render_template('incorrect_username_password.html')

@app.route('/signup', methods=['GET', 'POST'])
def go_to_signup():
    if request.method == 'POST':
        school_name = request.form['school_name']
        school_code = request.form['school_code']
        manager_personal_code = request.form['manager_personal_code']
        province = request.form['province']
        city = request.form['city']

        new_school = School(school_name=school_name, 
                            school_code=school_code,
                            manager_personal_code=manager_personal_code,
                            province=province,
                            city=city)
        db.session.add(new_school)
        db.session.commit()
        
        return redirect(url_for('go_to_notify_user'))
    
    return render_template('signup.html')

@app.route('/notify_user')
def go_to_notify_user():
    return render_template('notif_username_password_on_signup.html')

@app.route('/panel_home')
def go_to_panel_home():
    return render_template('management_panel/home.html')

@app.route('/panel_school_info')
def go_to_panel_school_info():
    data = School.query.filter(School.school_code == session['username']).first()
    return render_template('management_panel/school_info.html', data=data)

@app.route('/panel_classes', methods=['GET', 'POST'])
def go_to_panel_classes():
    school_code = session['username']
    classes = Class.query.filter(Class.school_code == school_code).all()
    return render_template('management_panel/classes.html', classes=classes)

@app.route('/panel_teachers')
def go_to_panel_teachers():
    return render_template('management_panel/teachers.html')

@app.route('/panel_students')
def go_to_panel_students():
    return render_template('management_panel/students.html')

@app.route('/add_class', methods=['GET', 'POST'])
def go_to_add_class():
    school_code = session['username']

    if request.method == 'POST':
        class_name = request.form['class_name']
        class_code = request.form['class_code']
        students_count = request.form['students_count']

        new_class = Class(class_name, class_code, students_count, school_code)
        db.session.add(new_class)
        db.session.commit()

        return render_template('management_panel/classes.html')

    return render_template('management_panel/add_class.html')


if __name__ == '__main__':
    app.run(debug=True)
