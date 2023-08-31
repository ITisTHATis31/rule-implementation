import re

def remove_comments(line):
    # Remove inline comments
    line = re.sub(r'\/\/.*', '', line)
    
    # Remove block comments
    line = re.sub(r'\/\*.*\*\/', '', line)
    
    return line.strip()

def check_executable_code_in_header(file_path):
    executable_patterns = [
        (r'def\s', 'Function definition'),
        (r'class\s', 'Class definition'),
        (r'@\w+', 'Decorator'),
        (r'main\(', 'Main function'),
        (r'if\s', 'If statement'),
        (r'else\s', 'Else statement'),
        (r'for\s', 'For loop'),
        (r'while\s', 'While loop'),
        (r'switch\s', 'Switch statement'),
        (r'return\s', 'Return statement'),
        (r'=\s', 'Assignment statement'),
        (r'\+\s', 'Addition operation'),
        (r'-\s', 'Subtraction operation'),
        (r'\*\s', 'Multiplication operation'),
        (r'/\s', 'Division operation'),
        (r'%\s', 'Modulus operation'),
        (r'print', 'Print statement'),
        (r'scanf', 'Input statement'),
        (r'fread', 'File read operation'),
        (r'fwrite', 'File write operation')
    ]

    executable_regex = re.compile('|'.join(f'({pattern})' for pattern, _ in executable_patterns))

    with open(file_path, 'r') as file:
        lines = file.readlines()
        violations = []
        for line_number, line in enumerate(lines, start=1):
            original_line = line.strip()
            line = remove_comments(line)
            match = executable_regex.search(line)
            if match:
                pattern = next(pattern for pattern, _ in executable_patterns if match.group())
                violations.append((line_number, original_line, pattern))
    
    if violations:
        for line_number, line, pattern in violations:
            print(f"Line {line_number}: '{line}' is considered executable due to {pattern}.")
        return True
    else:
        return False

header_file_path = r"C:\Users\LQR1COB\Downloads\c_files\FIT_Wdg.h"

if check_executable_code_in_header(header_file_path):
    print("The header file contains executable code.")
else:
    print("The header file does not contain any executable code.")
