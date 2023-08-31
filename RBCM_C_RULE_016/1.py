import re
from RBCM_C_RULE_016.multiline import remove_comments

#passing list as an argument to the function
def RBCM_C_RULE_016(lines):
    executable_keywords = ['main(', 'if ', 'else ', 'for', 'do', 'while', 'break', 'continue', 'goto', 'switch ', 'return ', 'print', 'scanf', 'fread', 'fwrite'] 
    found_executable_code = False

    for line_number, line in enumerate(lines, start=1):
        original_line = line.strip()
        for keyword in executable_keywords:
            pattern = re.escape(keyword)  # Escape the special characters in the keyword for regex
            if re.search(pattern, line):
                print(f"Line {line_number}: '{original_line}' is considered executable due to the presence of keyword: '{keyword}'")
                found_executable_code = True

    return found_executable_code

file_path = r"C:\Users\LQR1COB\Downloads\c_files\16Error.h"
lines_with_comments_removed = remove_comments(file_path)  # remove_comments returns a list
found_code = RBCM_C_RULE_016(lines_with_comments_removed)

#def check_executable_code_in_header(file_path):
 #   executable_keywords = ['main(', 'if ', 'else ', 'for', 'do', 'while', 'break', 'continue', 'goto', 'switch ', 'return ', 'print', 'scanf', 'fread', 'fwrite']
  #  found_executable_code = False

   # remove_comments(file_path)

    #with open(file_path, 'r') as file:
     #   lines = file.readlines()
      #  for line_number, line in enumerate(lines, start=1):
       #     original_line = line.strip()
        #    for keyword in executable_keywords:
         #       pattern = re.escape(keyword)  # Escape the special characters in the keyword for regex
          #      if re.search(pattern, line):
           #         print(f"Line {line_number}: '{original_line}' is considered executable due to the presence of keyword: '{keyword}'")
            #        found_executable_code = True
    #return found_executable_code

if found_code:
    print("The header file contains executable code.")
else:
    print("The header file does not contain executable code.")
