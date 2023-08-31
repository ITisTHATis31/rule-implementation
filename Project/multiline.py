import re

def remove_comments(file_path):
    # Read content from the file
    with open(file_path, 'r', encoding='utf8') as file:
        content = file.read()

    # Define the regex pattern for multi-line comments (/* ... */)
    multiline_pattern = r'/\*.*?\*/'
    # Define the regex pattern for inline comments (// ...)
    inline_pattern = r'//.*?(?=\n|$)'

    # Replace characters in multi-line comments with spaces and adjust new line characters
    updated_content = re.sub(multiline_pattern, lambda match: ' ' * len(match.group(0)) + '\n' * (match.group(0).count('\n')), content, flags=re.DOTALL)
    # Replace characters in inline comments with spaces
    updated_content = re.sub(inline_pattern, lambda match: ' ' * len(match.group(0)), updated_content)

    temp = updated_content.split('\n')
    return temp

    # Write the updated content back to the same file
    #with open(file_path, 'w') as file:
        #file.write(updated_content)

# Example usage
#file_path = r"C:\Users\LQR1COB\Downloads\c_files\dict\FIT_Wdg copy 2.h"
#remove_comments(file_path)
