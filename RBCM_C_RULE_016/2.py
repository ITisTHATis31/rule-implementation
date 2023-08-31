import re

def remove_comments(line):
    # Remove inline comments
    line = re.sub(r'\/\/.*', '', line)

    # Remove block comments
    line = re.sub(r'\/\*.*?\*\/', '', line)

    return line.strip()

def check_executable_code_in_header(file_path):
    executable_keywords = ['class ', '@', 'main(', 'if ', 'else ', 'for', 'while', 'switch ', 'return ', 'print', 'scanf', 'fread', 'fwrite']
    found_executable_code = False

    with open(file_path, 'r') as file:
        lines = file.readlines()
        in_multiline_comment = False
        for line_number, line in enumerate(lines, start=1):
            original_line = line.strip()
            line = remove_comments(line)
            if in_multiline_comment:
                if '*/' in line:
                    in_multiline_comment = False
                continue

            if '/*' in line:
                in_multiline_comment = True
                continue

            for keyword in executable_keywords:
                pattern = re.escape(keyword)  # Escape the special characters in the keyword for regex
                if re.search(pattern, line):
                    print(f"Line {line_number}: '{original_line}' is considered executable due to the presence of keyword: '{keyword}'")
                    found_executable_code = True
    return found_executable_code

header_file_path = r"C:\Users\LQR1COB\Downloads\c_files\FIT_Wdg.h"

if check_executable_code_in_header(header_file_path):
    print("The header file contains executable code.")
else:
    print("The header file does not contain executable code.")
