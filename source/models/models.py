from source import db
from flask_login import UserMixin

# جدول میانی Teacher <-> Class
teacher_class = db.Table('teacher_class',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id'), primary_key=True)
)

# جدول میانی Teacher <-> School
teacher_school = db.Table('teacher_school',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True),
    db.Column('school_id', db.Integer, db.ForeignKey('schools.id'), primary_key=True)
)

# ---------------------- School ----------------------
class School(db.Model, UserMixin):
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(100), nullable=False)
    school_code = db.Column(db.String(100), nullable=False, unique=True)
    manager_personal_code = db.Column(db.String(100), nullable=False, unique=True)
    province = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    classes = db.relationship("Class", back_populates="school", cascade="all, delete")
    students = db.relationship("Student", back_populates="school", cascade="all, delete")
    teachers = db.relationship("Teacher", secondary=teacher_school, back_populates="schools")

    def __init__(self, school_name, school_code, manager_personal_code, province, city, email):
        self.school_name = school_name
        self.school_code = school_code
        self.manager_personal_code = manager_personal_code
        self.province = province
        self.city = city
        self.email = email

    def get_id(self):
        return str(self.id)

# ---------------------- Class ----------------------
class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100), nullable=False)
    class_code = db.Column(db.String(100), nullable=False, unique=True)

    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    school = db.relationship("School", back_populates="classes")

    teachers = db.relationship("Teacher", secondary=teacher_class, back_populates="classes")
    students = db.relationship("Student", back_populates="class_", cascade="all, delete")

    def __init__(self, class_name, class_code, school_id):
        self.class_name = class_name
        self.class_code = class_code
        self.school_id = school_id

# ---------------------- Student ----------------------
class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    student_family = db.Column(db.String(100), nullable=False)
    student_national_code = db.Column(db.String(100), nullable=False, unique=True)
    student_password = db.Column(db.String(100), nullable=False)
    student_phone_number = db.Column(db.String(100), nullable=False, unique=True)

    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    class_ = db.relationship("Class", back_populates="students")

    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    school = db.relationship("School", back_populates="students")
    
    def __init__(self, student_name, student_family, student_national_code, student_password, student_phone_number, class_id, school_id):
        self.student_name = student_name
        self.student_family = student_family
        self.student_national_code = student_national_code
        self.student_password = student_password
        self.student_phone_number = student_phone_number
        self.class_id = class_id
        self.school_id = school_id

# ---------------------- Teacher ----------------------
class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(100), nullable=False)
    teacher_family = db.Column(db.String(100), nullable=False)
    teacher_national_code = db.Column(db.String(100), nullable=False, unique=True)
    teacher_password = db.Column(db.String(100), nullable=False)
    lesson = db.Column(db.String(100), nullable=False)

    classes = db.relationship("Class", secondary=teacher_class, back_populates="teachers")
    schools = db.relationship("School", secondary=teacher_school, back_populates="teachers")

    def __init__(self, teacher_name, teacher_family, teacher_national_code, teacher_password, lesson):
        self.teacher_name = teacher_name
        self.teacher_family = teacher_family
        self.teacher_national_code = teacher_national_code
        self.teacher_password = teacher_password
        self.lesson = lesson
