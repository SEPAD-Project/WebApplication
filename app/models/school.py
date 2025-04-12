from app import db
from flask_login import UserMixin


class School(db.Model, UserMixin):
    """
    School model representing a school entity in the database.
    
    Attributes:
        id (int): The primary key of the school.
        school_name (str): The name of the school.
        school_code (str): The unique code identifying the school.
        manager_personal_code (str): The personal code of the school's manager.
        province (str): The province where the school is located.
        city (str): The city where the school is located.
        teachers (str): A string representing the list of teacher national codes associated with the school.
    """
    __tablename__ = 'schools'  # Specifies the name of the table in the database
    
    # Define the columns in the table
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the school
    school_name = db.Column(db.String(100), nullable=False)  # Name of the school
    school_code = db.Column(db.String(100), nullable=False, unique=True)  # Unique code for the school
    manager_personal_code = db.Column(db.String(100), nullable=False, unique=True)  # Manager's personal code
    province = db.Column(db.String(100), nullable=False)  # Province where the school is located
    city = db.Column(db.String(100), nullable=False)  # City where the school is located
    teachers = db.Column(db.String(100), nullable=False)  # List of teachers associated with the school (as a string)
    email = db.Column(db.String(100), nullable=False)

    def __init__(self, school_name, school_code, manager_personal_code, province, city, teachers, email):
        """
        Constructor to initialize the School object with required attributes.
        
        Args:
            school_name (str): The name of the school.
            school_code (str): The unique code of the school.
            manager_personal_code (str): The personal code of the school's manager.
            province (str): The province where the school is located.
            city (str): The city where the school is located.
            teachers (str): A string representing the list of teachers for the school.
        """
        self.school_name = school_name  # Set the name of the school
        self.school_code = school_code  # Set the unique school code
        self.manager_personal_code = manager_personal_code  # Set the manager's personal code
        self.province = province  # Set the province of the school
        self.city = city  # Set the city of the school
        self.teachers = teachers  # Set the list of teachers for the school (as a string)
        self.email = email

    def get_id(self):
        """
        Override the default method to return the school ID as a string, 
        which is necessary for Flask-Login functionality.
        
        Returns:
            str: The ID of the school as a string.
        """
        return str(self.id)
