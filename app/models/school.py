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
                        This could be replaced with a proper relationship in the future for better normalization.
        email (str): The email address of the school.
    """
    __tablename__ = 'schools'  # Specifies the table name in the database

    # Define the columns in the table

    # Unique identifier for the school
    id = db.Column(db.Integer, primary_key=True)
    # Name of the school (required)
    school_name = db.Column(db.String(100), nullable=False)
    # Unique code for the school (required)
    school_code = db.Column(db.String(100), nullable=False, unique=True)
    # Manager's personal code (required)
    manager_personal_code = db.Column(
        db.String(100), nullable=False, unique=True)
    # Province where the school is located (required)
    province = db.Column(db.String(100), nullable=False)
    # City where the school is located (required)
    city = db.Column(db.String(100), nullable=False)
    # List of teachers associated with the school (required)
    teachers = db.Column(db.String(100), nullable=False)
    # Email address of the school (required)
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
            teachers (str, optional): A string representing the list of teacher national codes associated with the school.
                                      Defaults to None if no teachers are assigned initially.
            email (str, optional): The email address of the school. Defaults to None.
        """
        self.school_name = school_name  # Set the name of the school
        self.school_code = school_code  # Set the unique school code
        # Set the manager's personal code
        self.manager_personal_code = manager_personal_code
        self.province = province  # Set the province of the school
        self.city = city  # Set the city of the school
        self.teachers = teachers  # Set the list of teachers
        self.email = email  # Set the email address of the school

    def get_id(self):
        """
        Override the default method to return the school ID as a string, 
        which is necessary for Flask-Login functionality.

        Returns:
            str: The ID of the school as a string.
        """
        return str(self.id)
