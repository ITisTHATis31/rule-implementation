import re, os
from logging_utils import setup_logging, get_logger, log_info
from multiline import remove_comments

# Configure the logging for the main script
log_file = "C_Style_check.log"
setup_logging(log_file)
logger = get_logger(__name__)

#find header files in the given parent folder
def find_header_files(parent_folder):
    header_files = []
    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            if file.endswith(".h"):
                header_path = os.path.join(root, file)
                header_files.append(header_path)
    return header_files

#getting file path as argument for checking_executable_code_in_header
def RBCM_C_RULE_016(lines):
    executable_keywords = [r'main\s*\(', r'for\s*\(', r'if\s*\(', 'else', 'while', 'break', 'continue', 'goto', 'switch ', 'return ', 'printf', 'scanf', 'fread', 'fwrite']
    exclude_keywords = ['#ifndef', '#endif', '#if', '#else', r'^.*#error.*$', r'^.*#warning.*$']

    found_executable_code = False

    try:
        for line_number, line in enumerate(lines, start=1):
            # Check if the line contains #error or #warning directive
            if any(re.search(pattern, line) for pattern in exclude_keywords):
                continue

            for keyword in executable_keywords:
                pattern = re.escape(keyword)  # Escape the special characters in the keyword for regex
                if re.search(pattern, line):
                    logger.error(f"Line {line_number} is considered executable due to the presence of keyword: '{keyword}'")
                    found_executable_code = True

    except Exception as e:
        logger.error(f"An error occurred during C Rule 016 execution: {e}")
        found_executable_code = False

    return found_executable_code
    
if __name__ == "__main__":
    parent_folder = r"C:\Users\LQR1COB\Downloads\c_files\Platform" 
    #parent_folder = r"C:\Users\LQR1COB\Downloads\c_files\dict"
    header_files = find_header_files(parent_folder)

    if len(header_files) == 0:
        logger.info("No header files found in the parent folder and its subdirectories.")
    else:
        log_info(logger, "RBCM_C_RULE_016", "Check executable code in header file")
        for header_file in header_files:
            logger.info(f"Checking {header_file} for executable code ..... ")
            lines_with_comments_removed = remove_comments(header_file)  # remove_comments returns a list
            found_code = RBCM_C_RULE_016(lines_with_comments_removed)
            if found_code:
                logger.info("The header file contains executable code.")
            else:
                logger.info("The header file does not contain executable code.")

print("Checking Completed")