def generate_class_code(school_code:int, class_name:str):
    part1 = str(hex(school_code))[2:]
    
    part2 = ''
    for char in class_name:
        num = ord(char)
        part2 = part2 + str(num)
    part2 = str(hex(int(part2)))[2:]
    
    code = part1 + '#' + part2
    return code