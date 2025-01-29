from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql://root:sapprogram2583@185.4.28.110:5000/sap'
)
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


@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def go_to_home():
    return render_template('home.html')

@app.route('/login')
def go_to_login():
    return render_template('login.html')

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
