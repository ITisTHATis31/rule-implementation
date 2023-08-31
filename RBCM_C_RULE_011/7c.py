import re, os
from parse import parse_comments_for_prototype
from logging_utils import setup_logging, get_logger, log_info

# Configure the logging for the main script
log_file = "check.log"
setup_logging(log_file)
logger = get_logger(__name__)

def find_c_files(parent_folder):
    c_files = []
    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            if file.endswith(".c"):
                c_path = os.path.join(root, file)
                c_files.append(c_path)
    return c_files

def check_function_headers(file_path):

    with open(file_path, 'r', encoding='utf8') as file:
        c_lines = file.readlines()
    
    errors_found = False  
    function_definition_pattern = re.compile(r'\b\w+\b\s+\w+\s*\([^)]*\)\s*{', re.MULTILINE)
    functions = function_definition_pattern.findall("".join(c_lines))
    # Remove functions that start with 'else if'
    functions = [func for func in functions if not func.startswith('else if')]
    #print(f"Found {len(functions)} functions in the file.")
    #print(functions)

    if not functions:
        logger.info("No function found in the file.")
        return
    
    function_comments = {}  # Dictionary to store comments for each function prototype
    
    # Find the comments for each function prototype
    for function in functions:
        # Get the line number of the current function prototype
        line_number = None
        for idx, line in enumerate(c_lines):
            function = function.rstrip('{')
            if function in line:
                line_number = idx
                break

        if line_number is None:
            logger.error(f"Function header for '{function}' not found in the file.")
            errors_found = True
            continue

        # Read lines in reverse from the function prototype's line until the line with 'FUNCTION' to extract comments before the function prototype
        comments = []
        function_found = False
        for line in reversed(c_lines[:line_number]):
            comments.insert(0, line.strip())  # Add the line to the comments list
            if 'FUNCTION' in line:
                function_found = True
            if function_found and '/*' in line:
                break
        
        if not function_found:
            logger.error(f"Function header for '{function}' in {line_number+1} not found in the file.")
            errors_found = True
            continue

        # Join the comments to form a string and store them in the dictionary
        function_comments[function] = '\n'.join(comments)

        # Parse the comments for the current function prototype
        comments_dict = parse_comments_for_prototype(function_comments[function])
        #print(comments_dict)

        # Pattern to strip return type from the function prototype
        function_name = re.sub(r'^\s*\w+\s+', '', function).rstrip('\n')
        parameters = re.findall(r'^\s*\b\w+\b\s+\w+\s*\(([^)]*)\)\s*', function)[0].strip()
        return_type = re.sub(r'\b\w+\b\s*\([^)]*\)', '', function).strip().rstrip(' ')
        
        #print({function_name}, {parameters}, {return_type})

        
        # Check if function name, return type, and parameters match the comments
        if 'FUNCTION' in comments_dict and function_name not in comments_dict['FUNCTION']:
            logger.error(f"Function name in header '{(comments_dict['FUNCTION'])}' is not matched with function name in definition '{function_name}' in line {line_number+1}")
            errors_found = True

        if 'PARAM' in comments_dict and parameters not in comments_dict['PARAM']:
            logger.error(f"Parameter in header '{(comments_dict['PARAM'])}' is not matched with parameters in definition '{parameters}' in line {line_number+1}")
            errors_found = True

        if 'RETURN' in comments_dict and return_type not in comments_dict['RETURN']:
            logger.error(f"Return type in header: '{(comments_dict['RETURN'])}' is not matched with return type in definition '{return_type}' in line {line_number+1}")
            errors_found = True

        # Check if 'BRIEF' section has some contents written
        if 'BRIEF' in comments_dict and not comments_dict['BRIEF']:
            logger.error(f"'BRIEF' section is empty in function header for '{function}' in line {line_number+1}")
            errors_found = True

    if not errors_found:
        logger.info(f"All function headers are valid and complete.")

if __name__ == "__main__":
    
    #c_file_path = r"C:\Users\LQR1COB\Downloads\c_files\Platform\Aurix.FIT_Manager\Au_FITM.c"
    c_file_path = r"C:\Users\LQR1COB\Downloads\c_files\Platform"
    c_files = find_c_files(c_file_path)

    if c_files:  # If the path of the parent folder is given
        log_info(logger, "Check function header of global functions in c files")
        for c_file in c_files:
            logger.info(f"Checking function headers in {c_file} ..... ")
            check_function_headers(c_file)

    else:  # If the path of the h file itself is given
        log_info(logger, "Check function header of global functions in c files")
        logger.info(f"Checking function headers in {c_file_path} ..... ")
        check_function_headers(c_file_path)

print("Checking Completed")