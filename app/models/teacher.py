from app import db

class Teacher(db.Model):
    """
    Teacher model representing a teacher entity in the database.
    
    Attributes:
        id (int): The primary key of the teacher.
        teacher_name (str): The first name of the teacher.
        teacher_family (str): The last name (family name) of the teacher.
        teacher_national_code (str): The unique national code of the teacher.
        teacher_password (str): The password of the teacher for authentication.
        teacher_classes (str): The classes the teacher is associated with (a string representing class codes).
    """
    __tablename__ = 'teachers'  # Specifies the name of the table in the database
    
    # Define the columns in the table
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the teacher
    teacher_name = db.Column(db.String(100), nullable=False)  # First name of the teacher
    teacher_family = db.Column(db.String(100), nullable=False)  # Last name (family name) of the teacher
    teacher_national_code = db.Column(db.String(100), nullable=False, unique=True)  # Unique national code of the teacher
    teacher_password = db.Column(db.String(100), nullable=False)  # Password for the teacher
    teacher_classes = db.Column(db.String(100), nullable=False)  # Classes associated with the teacher, stored as a string of class codes
    lesson = db.Column(db.String(100), nullable=False)

    def __init__(self, teacher_name, teacher_family, teacher_national_code, teacher_password, teacher_classes, lesson):
        """
        Constructor to initialize the Teacher object with required attributes.
        
        Args:
            teacher_name (str): The first name of the teacher.
            teacher_family (str): The last name of the teacher.
            teacher_national_code (str): The unique national code of the teacher.
            teacher_password (str): The password for the teacher.
            teacher_classes (str): The classes the teacher is associated with (a string representing class codes).
            lesson (str): lesson of teacher.
        """
        self.teacher_name = teacher_name  # Set the first name of the teacher
        self.teacher_family = teacher_family  # Set the last name of the teacher
        self.teacher_national_code = teacher_national_code  # Set the national code of the teacher
        self.teacher_password = teacher_password  # Set the password of the teacher
        self.teacher_classes = teacher_classes  # Set the classes associated with the teacher
        self.lesson = lesson
