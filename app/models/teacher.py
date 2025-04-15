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
        teacher_classes (str): A string representing the class codes the teacher is associated with.
                               This could be replaced with a proper relationship in the future for better normalization.
        lesson (str): The subject or lesson taught by the teacher.
    """
    __tablename__ = 'teachers'  # Specifies the table name in the database

    # Define the columns in the table
    
    # Unique identifier for the teacher
    id = db.Column(db.Integer, primary_key=True)
    # First name of the teacher (required)
    teacher_name = db.Column(db.String(100), nullable=False)
    # Last name (family name) of the teacher (required)
    teacher_family = db.Column(db.String(100), nullable=False)
    # Unique national code of the teacher (required)
    teacher_national_code = db.Column(
        db.String(100), nullable=False, unique=True)
    # Password for the teacher (required)
    teacher_password = db.Column(db.String(100), nullable=False)
    # Classes associated with the teacher (required)
    teacher_classes = db.Column(db.String(100), nullable=False)
    # Subject or lesson taught by the teacher (required)
    lesson = db.Column(db.String(100), nullable=False)

    def __init__(self, teacher_name, teacher_family, teacher_national_code, teacher_password, teacher_classes, lesson):
        """
        Constructor to initialize the Teacher object with required attributes.

        Args:
            teacher_name (str): The first name of the teacher.
            teacher_family (str): The last name of the teacher.
            teacher_national_code (str): The unique national code of the teacher.
            teacher_password (str): The password for the teacher.
            teacher_classes (str): A string representing the class codes the teacher is associated with.
            lesson (str): The subject or lesson taught by the teacher.
        """
        self.teacher_name = teacher_name  # Set the first name of the teacher
        self.teacher_family = teacher_family  # Set the last name of the teacher
        # Set the national code of the teacher
        self.teacher_national_code = teacher_national_code
        self.teacher_password = teacher_password  # Set the password of the teacher
        # Set the classes associated with the teacher
        self.teacher_classes = teacher_classes
        self.lesson = lesson  # Set the subject or lesson taught by the teacher
