from app.utils.generate_class_code import generate_class_code
from flask_login import current_user
import openpyxl


def add_students(path_to_xlsx, sheet_name, name_letter, family_letter, nc_letter, class_letter, pass_letter, available_classes, registered_national_codes):
    workbook = openpyxl.load_workbook(path_to_xlsx)

    try:
        sheet = workbook[sheet_name]
    except KeyError:
        return 'sheet_not_found'
    
    try:
        name_index = openpyxl.utils.column_index_from_string(name_letter)-1
        family_index = openpyxl.utils.column_index_from_string(family_letter)-1
        nc_index = openpyxl.utils.column_index_from_string(nc_letter)-1
        class_index = openpyxl.utils.column_index_from_string(class_letter)-1
        pass_index = openpyxl.utils.column_index_from_string(pass_letter)-1
    except ValueError:
        return 'bad_column_letter'
    
    # ===============================================

    problems = []

    for cell in sheet[name_letter]:
        if cell.row == 1: continue
        if not isinstance(cell.value, str):
            problems.append(['bad_format', cell.row, cell.column_letter])
    
    for cell in sheet[family_letter]:
        if cell.row == 1: continue
        if not isinstance(cell.value, str):
            problems.append(['bad_format', cell.row, cell.column_letter])
    
    nc_list = []
    for cell in sheet[nc_letter]:
        if cell.row == 1: continue
        if not isinstance(cell.value, int):
            problems.append(['bad_format', cell.row, cell.column_letter])
        if str(cell.value) in registered_national_codes or str(cell.value) in nc_list:
            problems.append(['duplicated_nc', cell.row, cell.column_letter ])
        nc_list.append(str(cell.value))
        
    for cell in sheet[class_letter]:
        if cell.row == 1: continue
        if (not isinstance(cell.value, str)) and (not isinstance(cell.value, int)):
            problems.append(['bad_format', cell.row, cell.column_letter])
        if not (str(cell.value) in available_classes):
            problems.append(['unknown_class', cell.row, cell.column_letter ])
        
    for cell in sheet[pass_letter]:
        if cell.row == 1: continue
        if not isinstance(cell.value, int):
            problems.append(['bad_format', cell.row, cell.column_letter])

    if problems != []:
        return problems
    # ===============================================

    students = []
    school_code = current_user.school_code
    for row in sheet.iter_rows(values_only=True, min_row=2):
        name = row[name_index]
        family = row[family_index]
        nc = row[nc_index]
        class_ = generate_class_code(school_code ,str(row[class_index]))
        password = row[pass_index] 

        students.append({'name':name, 'family':family, 'national_code':nc, 'class':class_, 'password':password})
    
    return students

def add_classes(path_to_xlsx, sheet_name, name_letter, available_classes):
    workbook = openpyxl.load_workbook(path_to_xlsx)

    try:
        sheet = workbook[sheet_name]
    except KeyError:
        return 'sheet_not_found'
    
    try:
        name_index = openpyxl.utils.column_index_from_string(name_letter)-1
    except ValueError:
        return 'bad_column_letter'
    
    names_list = []
    for cell in sheet[name_letter]:
        if cell.row == 1: continue
        if (not isinstance(cell.value, str)) and (not isinstance(cell.value, int)):
            problems.append(['bad_format', cell.row, cell.column_letter])
        if str(cell.value) in available_classes or str(cell.value) in names_list:
            return 'duplicated_name', cell.row, cell.column_letter 
        names_list.append(str(cell.value))
        
    classes = []
    for row in sheet.iter_rows(values_only=True, min_row=2):
        name = row[name_index]
        code = generate_class_code(current_user.school_code, str(name))
        classes.append({'name':str(name), 'code':code})

    return classes
