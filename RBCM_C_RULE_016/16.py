import re
from RBCM_C_RULE_016.multiline import remove_comments

#passing list as an argument to the function
def RBCM_C_RULE_016(lines):
    executable_keywords = ['main(', 'main (', 'for ', 'if ', 'else', 'while', 'break', 'continue', 'goto', 'switch ', 'return ', 'print', 'scanf', 'fread', 'fwrite']
    exclude_keywords = ['#ifndef', '#endif', '#if', '#else', r'^.*#error.*$', r'^.*#warning.*$']

    found_executable_code = False

    for line_number, line in enumerate(lines, start=1):
        # Check if the line contains #error or #warning directive
        if any(re.search(pattern, line) for pattern in exclude_keywords):
            continue

        for keyword in executable_keywords:
            pattern = re.escape(keyword)  # Escape the special characters in the keyword for regex
            if re.search(pattern, line):
                print(f"Line {line_number} is considered executable due to the presence of keyword: '{keyword}'")
                found_executable_code = True

    return found_executable_code

#file_path = r"C:\Users\LQR1COB\Downloads\c_files\16Error.h"
file_path = r"C:\Users\LQR1COB\Downloads\c_files\Platform\McAL.McuExtensions\McuExt_Version.h"
lines_with_comments_removed = remove_comments(file_path)  # remove_comments returns a list
found_code = RBCM_C_RULE_016(lines_with_comments_removed)

if found_code:
    print("The header file contains executable code.")
else:
    print("The header file does not contain executable code.")
