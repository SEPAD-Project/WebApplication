from app import db

from flask_login import UserMixin

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