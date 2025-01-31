from app import db

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    student_family = db.Column(db.String(100), nullable=False)
    student_national_code = db.Column(db.String(100), nullable=False, unique=True)
    student_password = db.Column(db.String(100), nullable=False)
    class_code = db.Column(db.String(100), nullable=False)
    school_code = db.Column(db.String(100), nullable=False)

    def __init__(self, student_name, student_family, student_national_code, student_password, class_code, school_code):
        self.student_name = student_name
        self.student_family = student_family
        self.student_national_code = student_national_code
        self.student_password = student_password
        self.class_code = class_code
        self.school_code = school_code
        