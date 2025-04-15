from app import db


class Class(db.Model):
    """
    Class model representing a class in the database.

    Attributes:
        id (int): Primary key of the class.
        class_name (str): The name of the class.
        class_code (str): The unique code identifying the class.
        school_code (str): The code of the school to which the class belongs.
        teachers (str): A string representing the list of teacher national codes associated with the class.
                        This could be replaced with a proper relationship in the future for better normalization.
    """
    __tablename__ = 'classes'  # Specifies the table name in the database

    # Define the columns in the table

    # Unique identifier for the class
    id = db.Column(db.Integer, primary_key=True)
    # Name of the class (required)
    class_name = db.Column(db.String(100), nullable=False)
    # Unique code for the class (required)
    class_code = db.Column(db.String(100), nullable=False, unique=True)
    # Code identifying the school (required)
    school_code = db.Column(db.String(100), nullable=False)
    # A string to store teacher national codes (required)
    teachers = db.Column(db.String(100), nullable=False)

    def __init__(self, class_name, class_code, school_code, teachers):
        """
        Constructor to initialize the Class object with required attributes.

        Args:
            class_name (str): The name of the class.
            class_code (str): The unique code of the class.
            school_code (str): The code of the school.
            teachers (str, optional): A string representing the list of teacher national codes assigned to the class.
                                      Defaults to None if no teachers are assigned initially.
        """
        self.class_name = class_name  # Set the name of the class
        self.class_code = class_code  # Set the unique class code
        self.school_code = school_code  # Set the school code
        self.teachers = teachers  # Set the list of teachers
