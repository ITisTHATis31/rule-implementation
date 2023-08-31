import re, os, logging
from parse import parse_comments_for_prototype
from multiline import remove_comments

# Configure the logging for the main script
log_file = "check.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")
logger = logging.getLogger(__name__)

def log_info(logger, rule_name):
    logger.info("==============================================================================================================================")
    # Log the rule name and the rule information
    logger.info("#"*75)
    logger.info(f" Rule : {rule_name}")
    logger.info(f"#"*75)

def RBCM_C_RULE_010(file_path):
    """

        Function name: RBCM_C_RULE_010

        Description: The RBCM_C_RULE_010 function performs a C style check for the correctness of 
        headers of the global function prototypes in source files. 

        :Usage example:

            :RBCM_C_RULE_010(Paths):
        // path of the repo or header file 
            
        :return: Log detail of the header file validation.

        """

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
    
    c_lines_without_comments = remove_comments(file_path)
    function_comments = {}  # Dictionary to store comments for each function
    previous_line_number = -1  # Initialize with a value that's definitely smaller than any line number
    
    # Find the comments for each function prototype
    for function in functions:

        try:
            function = re.sub(r'(\s*{\s*$)|((?<=\))[\s\n]+)', '', function)
            #print(function)
            function_name = re.findall(r'^\s*\w+\s+(\w+)\s*\([^)]*\)', function)[0].strip()
            parameters = re.findall(r'^\s*\b\w+\b\s+\w+\s*\(([^)]*)\)\s*', function)[0].strip()
            return_type = re.sub(r'\b\w+\b\s*\([^)]*\)', '', function).strip().rstrip(' ')
        
            #print({function_name}, {parameters}, {return_type})

            # Get the line number of the current function prototype
            line_number = None
            idx = 0
            while idx < len(c_lines_without_comments):
                line = c_lines_without_comments[idx]
                if function in line and idx > previous_line_number:
                    line_number = idx
                    break
                elif function_name in line and idx > previous_line_number:
                    line_number = idx
                    break
                idx += 1

            if line_number is not None:
                previous_line_number = line_number

            if line_number is None:
                #logger.error(f"Function header for '{function}' not found in the file.")
                logger.error(f"cannot find line number for '{function}' in the file.")
                errors_found = True
                continue

            # Read lines in reverse from the function's line until the line with 'FUNCTION' to extract comments before the function prototype
            comments = []
            function_found = False
            for line in reversed(c_lines[:line_number]):
                comments.insert(0, line.strip())  # Add the line to the comments list
                if function_name in line and 'FUNCTION:' in line:
                    function_found = True
                if function_found and '/*' in line:
                    break
        
            if not function_found:
                logger.error(f"Function header for '{function}' in {line_number+1} not found in the file.")
                errors_found = True
                continue

            # Join the comments to form a string and store them in the dictionary
            function_comments[function] = '\n'.join(comments)

            # Parse the comments for the current function
            comments_dict = parse_comments_for_prototype(function_comments[function])
            #print(comments_dict)

            # Check if function name, return type, and parameters match the comments
            if 'FUNCTION' in comments_dict and function_name not in comments_dict['FUNCTION']:
                logger.error(f"Function name in header '{(comments_dict['FUNCTION'])}' is not matched with function name in definition '{function_name}' in line {line_number+1}")
                errors_found = True

            if 'PARAM' not in comments_dict:
                logger.error(f"'PARAM' section is missing in function header for '{function}' in line {line_number+1}")
                errors_found = True

            elif 'PARAM' in comments_dict and parameters not in comments_dict['PARAM']:
                logger.error(f"Parameter in header '{(comments_dict['PARAM'])}' is not matched with parameters in definition '{parameters}' in line {line_number+1}")
                errors_found = True

            if 'RETURN' not in comments_dict:
                logger.error(f"'RETURN' section is missing in function header for '{function}' in line {line_number+1}")
                errors_found = True

            if 'RETURN' in comments_dict and return_type not in comments_dict['RETURN']:
                logger.error(f"Return type in header: '{(comments_dict['RETURN'])}' is not matched with return type in definition '{return_type}' in line {line_number+1}")
                errors_found = True

            if 'BRIEF' not in comments_dict:
                logger.error(f"'BRIEF' section is missing in function header for '{function}' in line {line_number+1}")
                errors_found = True

            # Check if 'BRIEF' section has some contents written
            if 'BRIEF' in comments_dict and not comments_dict['BRIEF']:
                logger.error(f"'BRIEF' section is empty in function header for '{function}' in line {line_number+1}")
                errors_found = True

        except Exception as e:
            print(f"Error processing function header for {function}")
            print(f"Error message: {e}")

    if not errors_found:
        logger.info(f"All function headers are valid and complete.")

if __name__ == "__main__":
    
    #c_file_path = r"C:\Users\LQR1COB\Downloads\c_files\Platform\Aurix.FIT_Manager\Au_FITM.c"
    c_file_path = r"C:\Users\LQR1COB\Downloads\c_files\Platform"
    c_files = []
    for root, dirs, files in os.walk(c_file_path):
        for file in files:
            if file.endswith(".c"):
                c_path = os.path.join(root, file)
                c_files.append(c_path)

    if c_files:  # If the path of the parent folder is given
        log_info(logger, "Check function header of global functions in c files")
        for c_file in c_files:
            logger.info(f"Checking function headers in {c_file} ..... ")
            RBCM_C_RULE_010(c_file)

    else:  # If the path of the h file itself is given
        log_info(logger, "Check function header of global functions in c files")
        logger.info(f"Checking function headers in {c_file_path} ..... ")
        RBCM_C_RULE_010(c_file_path)

print("Checking Completed")