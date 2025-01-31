from app import db


class Class(db.Model):
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100), nullable=False)
    class_code = db.Column(db.String(100), nullable=False, unique=True)
    school_code = db.Column(db.Integer, nullable=False)
    teachers = db.Column(db.JSON)

    def __init__(self, class_name, class_code, school_code, teachers):
        self.class_name = class_name
        self.class_code = class_code
        self.school_code = school_code
        self.teachers = teachers
