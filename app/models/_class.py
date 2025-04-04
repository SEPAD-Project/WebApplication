from app import db


class Class(db.Model):
    """
    Class model representing a class in the database.
    
    Attributes:
        id (int): Primary key of the class.
        class_name (str): The name of the class.
        class_code (str): The unique code of the class.
        school_code (str): The code of the school to which the class belongs.
        teachers (str): A string representing the list of teacher national codes associated with the class.
    """
    __tablename__ = 'classes'  # Specifies the name of the table in the database
    
    # Define the columns in the table
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the class
    class_name = db.Column(db.String(100), nullable=False)  # Name of the class
    class_code = db.Column(db.String(100), nullable=False, unique=True)  # Unique code for the class
    school_code = db.Column(db.String(100), nullable=False)  # Code identifying the school
    teachers = db.Column(db.String(100))  # A string to store the list of teachers associated with the class

    def __init__(self, class_name, class_code, school_code, teachers):
        """
        Constructor to initialize the Class object with required attributes.
        
        Args:
            class_name (str): The name of the class.
            class_code (str): The unique code of the class.
            school_code (str): The code of the school.
            teachers (str): A string representing the list of teachers assigned to the class.
        """
        self.class_name = class_name  # Set the name of the class
        self.class_code = class_code  # Set the unique class code
        self.school_code = school_code  # Set the school code
        self.teachers = teachers  # Set the list of teachers for this class (as a string)
