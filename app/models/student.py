from app import db


class Student(db.Model):
    """
    Student model representing a student entity in the database.
    
    Attributes:
        id (int): The primary key of the student.
        student_name (str): The first name of the student.
        student_family (str): The last name (family name) of the student.
        student_national_code (str): The unique national code of the student.
        student_password (str): The password of the student for authentication.
        class_code (str): The code of the class the student belongs to.
        school_code (str): The unique code of the school the student belongs to.
    """
    __tablename__ = 'students'  # Specifies the name of the table in the database
    
    # Define the columns in the table
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the student
    student_name = db.Column(db.String(100), nullable=False)  # First name of the student
    student_family = db.Column(db.String(100), nullable=False)  # Last name (family name) of the student
    student_national_code = db.Column(db.String(100), nullable=False, unique=True)  # Unique national code of the student
    student_password = db.Column(db.String(100), nullable=False)  # Password for the student
    class_code = db.Column(db.String(100), nullable=False)  # Class code to which the student belongs
    school_code = db.Column(db.String(100), nullable=False)  # School code to which the student belongs

    def __init__(self, student_name, student_family, student_national_code, student_password, class_code, school_code):
        """
        Constructor to initialize the Student object with required attributes.
        
        Args:
            student_name (str): The first name of the student.
            student_family (str): The last name of the student.
            student_national_code (str): The unique national code of the student.
            student_password (str): The password for the student.
            class_code (str): The code of the class the student belongs to.
            school_code (str): The code of the school the student belongs to.
        """
        self.student_name = student_name  # Set the first name of the student
        self.student_family = student_family  # Set the last name of the student
        self.student_national_code = student_national_code  # Set the national code of the student
        self.student_password = student_password  # Set the password of the student
        self.class_code = class_code  # Set the class code of the student
        self.school_code = school_code  # Set the school code of the student
