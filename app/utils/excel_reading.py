from app.utils.generate_class_code import generate_class_code
from flask_login import current_user
import openpyxl
from datetime import time

def add_students(path_to_xlsx, sheet_name, name_letter, family_letter, nc_letter, class_letter, pass_letter, available_classes, registered_national_codes):
    """
    Adds students from an Excel file to the database, verifying the format and preventing duplicates.
    
    Args:
        path_to_xlsx (str): Path to the Excel file containing student data.
        sheet_name (str): Name of the sheet in the Excel file.
        name_letter (str): Column letter for student names.
        family_letter (str): Column letter for student family names.
        nc_letter (str): Column letter for student national codes.
        class_letter (str): Column letter for class codes.
        pass_letter (str): Column letter for student passwords.
        available_classes (list): List of valid class codes.
        registered_national_codes (list): List of national codes already registered in the system.
    
    Returns:
        list or str: A list of student dictionaries if the data is valid, or an error message or list of problems.
    """
    
    # Load the workbook and sheet
    workbook = openpyxl.load_workbook(path_to_xlsx)

    try:
        sheet = workbook[sheet_name]
    except KeyError:
        return 'sheet_not_found'  # Return error if sheet is not found
    
    # Get the column indices for each required field
    try:
        name_index = openpyxl.utils.column_index_from_string(name_letter)-1
        family_index = openpyxl.utils.column_index_from_string(family_letter)-1
        nc_index = openpyxl.utils.column_index_from_string(nc_letter)-1
        class_index = openpyxl.utils.column_index_from_string(class_letter)-1
        pass_index = openpyxl.utils.column_index_from_string(pass_letter)-1
    except ValueError:
        return 'bad_column_letter'  # Return error if an invalid column letter is provided
    
    # ===============================================

    problems = []

    # Check that the student names and families are in string format
    for cell in sheet[name_letter]:
        if cell.row == 1: continue
        if not isinstance(cell.value, str):
            problems.append(['bad_format', cell.row, cell.column_letter])
    
    for cell in sheet[family_letter]:
        if cell.row == 1: continue
        if not isinstance(cell.value, str):
            problems.append(['bad_format', cell.row, cell.column_letter])
    
    # Check that national codes are integers and ensure they are not duplicated
    nc_list = []
    for cell in sheet[nc_letter]:
        if cell.row == 1: continue
        if not isinstance(cell.value, int):
            problems.append(['bad_format', cell.row, cell.column_letter])
        if str(cell.value) in registered_national_codes or str(cell.value) in nc_list:
            problems.append(['duplicated_nc', cell.row, cell.column_letter])
        nc_list.append(str(cell.value))
        
    # Check that class codes are valid and exist in the available classes list
    for cell in sheet[class_letter]:
        if cell.row == 1: continue
        if (not isinstance(cell.value, str)) and (not isinstance(cell.value, int)):
            problems.append(['bad_format', cell.row, cell.column_letter])
        if not (str(cell.value) in available_classes):
            problems.append(['unknown_class', cell.row, cell.column_letter])
        
    # Check that passwords are integers
    for cell in sheet[pass_letter]:
        if cell.row == 1: continue
        if not isinstance(cell.value, int):
            problems.append(['bad_format', cell.row, cell.column_letter])

    # If there are any problems, return them
    if problems != []:
        return problems
    # ===============================================

    students = []
    school_code = current_user.school_code

    # Iterate through the rows and create student entries
    for row in sheet.iter_rows(values_only=True, min_row=2):
        name = row[name_index]
        family = row[family_index]
        nc = row[nc_index]
        class_ = generate_class_code(school_code ,str(row[class_index]))
        password = row[pass_index]

        students.append({'name': name, 'family': family, 'national_code': nc, 'class': class_, 'password': password})
    
    return students

def add_classes(path_to_xlsx, sheet_name, name_letter, available_classes):
    """
    Adds class data from an Excel file and checks for duplicates and format errors.

    Args:
        path_to_xlsx (str): Path to the Excel file containing class data.
        sheet_name (str): Name of the sheet in the Excel file.
        name_letter (str): Column letter for class names.
        available_classes (list): List of class codes already available in the system.

    Returns:
        list or str: A list of class dictionaries if the data is valid, or an error message or list of problems.
    """

    # Load the workbook and sheet
    workbook = openpyxl.load_workbook(path_to_xlsx)

    try:
        sheet = workbook[sheet_name]
    except KeyError:
        return 'sheet_not_found'  # Return error if sheet is not found
    
    # Get the column index for class names
    try:
        name_index = openpyxl.utils.column_index_from_string(name_letter)-1
    except ValueError:
        return 'bad_column_letter'  # Return error if an invalid column letter is provided
    
    problems = []
    names_list = []

    # Check that the class names are either strings or integers and that they are unique
    for cell in sheet[name_letter]:
        if cell.row == 1: continue
        if (not isinstance(cell.value, str)) and (not isinstance(cell.value, int)):
            problems.append(['bad_format', cell.row, cell.column_letter])
        if str(cell.value) in available_classes or str(cell.value) in names_list:
            problems.append(['duplicated_name', cell.row, cell.column_letter])
        names_list.append(str(cell.value))

    # If there are any problems, return them
    if problems != []:
        return problems

    classes = []

    # Iterate through the rows and create class entries
    for row in sheet.iter_rows(values_only=True, min_row=2):
        name = row[name_index]
        code = generate_class_code(current_user.school_code, str(name))
        classes.append({'name': str(name), 'code': code})

    return classes

def schedule_extraction(path_to_xlsx, sheet_name, check_day, str_time):

    workbook = openpyxl.load_workbook(path_to_xlsx)
    check_time = time.fromisoformat(str_time)

    try:
        sheet = workbook[sheet_name]
    except KeyError:
        return 'sheet_not_found'
    
    for row_idx, row in enumerate(sheet.iter_rows(values_only=True, min_row=2)):
        if row[0].lower() == check_day.lower():
            for column in sheet.iter_cols(values_only=True, min_col=2):
                content = str(column[0]).split('-')
                start_time = time.fromisoformat(content[0])
                end_time = time.fromisoformat(content[1])

                if start_time <= check_time <= end_time:
                    return column[row_idx+1]
                