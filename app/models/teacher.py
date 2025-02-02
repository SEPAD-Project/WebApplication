from app import db

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(100), nullable=False)
    teacher_family = db.Column(db.String(100), nullable=False)
    teacher_national_code = db.Column(db.String(100), nullable=False, unique=True)
    teacher_password = db.Column(db.String(100), nullable=False)
    teacher_classes = db.Column(db.String(100), nullable=False)

    def __init__(self, teacher_name, teacher_family, teacher_national_code, teacher_password, teacher_classes):
        self.teacher_name = teacher_name
        self.teacher_family = teacher_family
        self.teacher_national_code = teacher_national_code
        self.teacher_password = teacher_password
        self.teacher_classes = teacher_classes
        