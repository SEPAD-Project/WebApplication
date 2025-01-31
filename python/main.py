from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from generate_class_code import generate_class_code

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql://root:sapprogram2583@185.4.28.110:5000/sap'
)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "go_to_login"


db = SQLAlchemy(app)

class School(db.Model, UserMixin):
    __tablename__ = 'schools'
    
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(100), nullable=False)
    school_code = db.Column(db.Integer, nullable=False, unique=True)
    manager_personal_code = db.Column(db.Integer, nullable=False, unique=True)
    province = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)

    def __init__(self, school_name, school_code, manager_personal_code, province, city):
        self.school_name = school_name
        self.school_code = school_code
        self.manager_personal_code = manager_personal_code
        self.province = province
        self.city = city

    def get_id(self):
        return str(self.id)

class Class(db.Model):
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100), nullable=False)
    class_code = db.Column(db.String(100), nullable=False, unique=True)
    school_code = db.Column(db.Integer, nullable=False)

    def __init__(self, class_name, class_code, school_code):
        self.class_name = class_name
        self.class_code = class_code
        self.school_code = school_code

@login_manager.user_loader
def load_user(user_id):
    return School.query.get(int(user_id))

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def go_to_home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def go_to_login():
    if current_user.is_authenticated:
        return redirect(url_for('go_to_panel_home'))

    if request.method == 'POST':
        given_school_code = request.form['username']
        given_manager_personal_code = request.form['password']

        school = School.query.filter(School.school_code == int(given_school_code)).first()
        if school is None:
            return redirect(url_for('go_to_incorrect_username_password'))

        manager_personal_code = school.manager_personal_code
        
        if manager_personal_code == int(given_manager_personal_code):
            login_user(school, remember=True)
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
        
        try:
            db.session.add(new_school)
            db.session.commit()
        except:
            return redirect(url_for('go_to_duplicated_school_info'))
        
        return redirect(url_for('go_to_notify_user'))
    
    return render_template('signup.html')

@app.route('/notify_user')
def go_to_notify_user():
    return render_template('notif_username_password_on_signup.html')

@app.route('/panel_home')
@login_required
def go_to_panel_home():
    return render_template('management_panel/home.html')

@app.route('/panel_school_info')
@login_required
def go_to_panel_school_info():
    data = School.query.filter(School.school_code == int(current_user.school_code)).first()
    return render_template('management_panel/school_info.html', data=data)

@app.route('/panel_classes', methods=['GET', 'POST'])
@login_required
def go_to_panel_classes():
    classes = Class.query.filter(Class.school_code == int(current_user.school_code)).all()
    return render_template('management_panel/classes.html', classes=classes)

@app.route('/panel_teachers')
@login_required
def go_to_panel_teachers():
    return render_template('management_panel/teachers.html')

@app.route('/panel_students')
@login_required
def go_to_panel_students():
    return render_template('management_panel/students.html')

@app.route('/add_class', methods=['GET', 'POST'])
def go_to_add_class():
    school_code = int(current_user.school_code)

    if request.method == 'POST':
        class_name = request.form['class_name']
        class_code = generate_class_code(school_code, class_name)
        try:
            new_class = Class(class_name, class_code, school_code)
            db.session.add(new_class)
            db.session.commit()
        except:
            return redirect(url_for('go_to_duplicated_class_info'))
        
        return redirect(url_for('go_to_panel_classes'))

    return render_template('management_panel/add_class.html')

@app.route('/duplicated_school_info')
def go_to_duplicated_school_info():
    return render_template('duplicated_school_info.html')

@app.route('/duplicated_class_info')
@login_required
def go_to_duplicated_class_info():
    return render_template('duplicated_class_info.html')

if __name__ == '__main__':
    app.run(debug=True)
