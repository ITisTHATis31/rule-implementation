import re, os
from parse import parse_comments_for_prototype
from logging_utils import setup_logging, get_logger, log_info

# Configure the logging for the main script
log_file = "C_Style_check.log"
setup_logging(log_file)
logger = get_logger(__name__)

def find_h_files(parent_folder):
    h_files = []
    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            if file.endswith(".h"):
                h_path = os.path.join(root, file)
                h_files.append(h_path)
    return h_files

def check_function_headers(file_path):

    with open(file_path, 'r', encoding='utf8') as file:
        h_lines = file.readlines()
    
    errors_found = False
    function_prototype_pattern = re.compile(r'\b\w+\b\s+\w+\s*\([^)]*\)\s*;', re.MULTILINE)
    function_prototypes = function_prototype_pattern.findall("".join(h_lines))
    #print(f"Found {len(function_prototypes)} function prototypes in the file.")
    #print(function_prototypes)

    if not function_prototypes:
        logger.info("No function prototypes found in the file.")
        return
    
    function_comments = {}  # Dictionary to store comments for each function prototype
    
    # Find the comments for each function prototype
    for function_prototype in function_prototypes:
        # Get the line number of the current function prototype
        line_number = None
        for idx, line in enumerate(h_lines):
            if function_prototype in line:
                line_number = idx
                break

        if line_number is None:
            logger.error(f"Function header for '{function_prototype}' not found in the file.")
            errors_found = True
            continue

        # Read lines in reverse from the function prototype's line until the line with 'FUNCTION' to extract comments before the function prototype
        comments = []
        function_found = False
        for line in reversed(h_lines[:line_number]):
            comments.insert(0, line.strip())  # Add the line to the comments list
            if 'FUNCTION:' in line:
                function_found = True
            if function_found and '/*' in line:
                break
        
        if not function_found:
            logger.error(f"Function header for '{function_prototype}' in {line_number+1} not found in the file.")
            errors_found = True
            continue

        # Join the comments to form a string and store them in the dictionary
        function_comments[function_prototype] = '\n'.join(comments)

        # Parse the comments for the current function prototype
        comments_dict = parse_comments_for_prototype(function_comments[function_prototype])
        #print(comments_dict)

        # Pattern to strip return type from the function prototype
        function_name = re.findall(r'^\s*\w+\s+(\w+)\s*\([^)]*\)', function_prototype)[0].strip()
        parameters = re.findall(r'^\s*\b\w+\b\s+\w+\s*\(([^)]*)\)\s*;$', function_prototype)[0].strip()
        return_type = re.sub(r'\b\w+\b\s*\([^)]*\)', '', function_prototype).strip().rstrip(';').rstrip(' ')
        
        #print({function_name}, {parameters}, {return_type})

        # Check if function name, return type, and parameters match the comments
        if 'FUNCTION' in comments_dict and function_name not in comments_dict['FUNCTION']:
            logger.error(f"Function name in header '{(comments_dict['FUNCTION'])}' is not matched with function name in prototype '{function_name}' in line {line_number+1}")
            errors_found = True

        if 'PARAM' not in comments_dict:
            logger.error(f"'PARAM' section is missing in function header for '{function_prototype}' in line {line_number+1}")
            errors_found = True

        elif 'PARAM' in comments_dict and parameters not in comments_dict['PARAM']:
            logger.error(f"Parameter in header '{(comments_dict['PARAM'])}' is not matched with parameters in prototype '{parameters}' in line {line_number+1}")
            errors_found = True

        if 'RETURN' not in comments_dict:
            logger.error(f"'RETURN' section is missing in function header for '{function_prototype}' in line {line_number+1}")
            errors_found = True

        if 'RETURN' in comments_dict and return_type not in comments_dict['RETURN']:
            logger.error(f"Return type in header: '{(comments_dict['RETURN'])}' is not matched with return type in prototype '{return_type}' in line {line_number+1}")
            errors_found = True

        if 'BRIEF' not in comments_dict:
            logger.error(f"'BRIEF' section is missing in function header for '{function_prototype}' in line {line_number+1}")
            errors_found = True

        # Check if 'BRIEF' section has some contents written
        if 'BRIEF' in comments_dict and not comments_dict['BRIEF']:
            logger.error(f"'BRIEF' section is empty in function header for '{function_prototype}' in line {line_number+1}")
            errors_found = True

    if not errors_found:
        logger.info(f"All function headers are valid and complete.")

if __name__ == "__main__":
    
    #h_file_path = r"C:\Users\LQR1COB\Downloads\c_files\Platform\Aurix.FIT_Manager\Au_FITM.h"
    h_file_path = r"C:\Users\LQR1COB\Downloads\c_files\Platform"
    h_files = find_h_files(h_file_path)

    if h_files:  # If the path of the parent folder is given
        log_info(logger, "Check function header prototype of global functions in h files")
        for h_file in h_files:
            logger.info(f"Checking function headers in {h_file} ..... ")
            check_function_headers(h_file)

    else:  # If the path of the h file itself is given
        log_info(logger, "Check function header prototype of global functions in h files")
        logger.info(f"Checking function headers in {h_file_path} ..... ")
        check_function_headers(h_file_path)

print("Checking Completed")