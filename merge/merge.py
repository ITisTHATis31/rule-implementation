import re, pathlib, logging
import ply.lex as lex

class logging_utils:

    def setup_logging(log_file):
        logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

    def get_logger(name):
        return logging.getLogger(name)

    def log_info(logger, rule_name, rule_info):
        # Log the rule name and the rule information
        logger.info(f"Rule : {rule_name}, Rule Info : {rule_info}")

# Configure the logging for the main script
log_file = "C_Style_check.log"
logging_utils.setup_logging(log_file)
logger = logging_utils.get_logger(__name__)

class common:
    
    def find_files(path):
        """

            Function name: find_files

            Description: The find_files function takes a path as input and returns a list of ".h" and ".c" files inside a directory or folder.

            :Usage example:

                :find_files(Path):
            // path of the directory or header file or c file
            
            :return: List of ".h" and ".c" files inside a directory or folder.

        """
        test_files=[]
        if ".c" not in path and ".h" not in path:
            desktop = pathlib.Path(path)    
            for file_path in desktop.rglob("*"):
                if file_path.suffix in {'.c', '.h'}:
                    test_files.append(file_path)
        elif ".c" in path or ".h" in path:
            test_files.append(path)
        return test_files

    def remove_comments(file_path):
        """

            Function name: remove_comments

            Description: The remove_comments function read the contents of the file and remove single line comments as well as
            multiline comments and return the result as a list.

            :Usage example:

                :remove_comments(Path):
            // path of the c source file or header file
            
            :return: Lines of the given file without comments as a list.

        """
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

class CommentParser:
    def __init__(self, config_file_path):
        self.tags = self.read_config(config_file_path)
        self.multiline_comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)
        self.tokens = [tag.upper() for tag in self.tags] + ['ERROR']
        self.lexer = lex.lex(module=self)
    
    def read_config(self, config_file_path):
        with open(config_file_path) as config_file:
            return [tag.strip().upper() for tag in config_file]
        
    def t_FUNCTION(self, t):
        r'FUNCTION:'
        return t

    def t_BRIEF(self, t):
        r'\\brief\b'
        return t

    def t_PARAM(self, t):
        r'\\param\b'
        return t

    def t_RETURN(self, t):
        r'\\return'
        return t

    def t_PRE(self, t):
        r'\\pre\b'
        return t

    def t_POST(self, t):
        r'\\post\b'
        return t

    def t_ATTENTION(self, t):
        r'\\attention\b'
        return t

    def t_TODO(self, t):
        r'\\todo\b'
        return t

    def t_error(self, t):
        t.type = 'ERROR'
        t.value = t.value[1:]  # Remove the backslash character
        t.lexer.skip(1)

    def parse_comments(self, prototype):
        """

            Function name: parse_comments

            Description: The parse_comments function takes a string as input and returns a dictionary of the contents of the function headers
            such as function name, brief description, parameters, return type, preconditions, postconditions, attention, and todo.

            :Usage example:

                :parse_comments(string):
            // string of function headers
            
            :return: Dictionary of the contents of the function headers.

        """
        comments = {}
        matches = re.finditer(self.multiline_comment, prototype)

        for match in matches:
            comment = match.group(1).strip()
            self.lexer.input(comment)

            for tok in self.lexer:
                if tok.type in self.tags:
                    content_start = tok.lexpos + len(tok.value)
                    content = comment[content_start:].strip()
                    content = content.replace('\n*', '')
                    content = re.sub(r'\s+', ' ', content)
                    content = content.replace('*', '')
                    next_tag_pos = content.find('\\')
                    if next_tag_pos != -1:
                        content = content[:next_tag_pos].strip()
                    else:
                        content = content.split('\n', 1)[0].strip()
                    if tok.type == 'FUNCTION':
                        if re.search(r'^\s*\w+\s+(\w+)\s*\([^)]*\)', content):
                            content = re.findall(r'(\w+)\s*\([^)]*\)', content)[0].strip()
                    comments[tok.type] = content

        return comments

def RBCM_C_RULE_016(file_path):
    """

        Function name: RBCM_C_RULE_016

        Description: The RBCM_C_RULE_016 function performs a C style check for potential executable code in a list of header files. 
        The function validates by confirming non-executable codes in a header file.

        :Usage example:

            :RBCM_C_RULE_016(Path):
        // path of the header file
            
        :return: Log detail of the header file validation.

    """
    if str(file_path).endswith(".h"):

        logging_utils.log_info(logger, "RBCM_C_RULE_016", "Check executable code in header file")

        executable_keywords = [r'main\s*\(', r'for\s*\(', r'if\s*\(', 'else', 'while', 'break', 'continue', 'goto', 'switch ', 'return ']
        exclude_keywords = ['#ifndef', '#endif', '#if', '#else', r'^.*#error.*$', r'^.*#warning.*$']

        #found_executable_code = False
        lines_with_comments_removed = common.remove_comments(file_path)  # remove_comments returns a list

        try:
            for line_number, line in enumerate(lines_with_comments_removed, start=1):
                # Check if the line contains #error or #warning directive
                if any(re.search(pattern, line) for pattern in exclude_keywords):
                    continue

                for keyword in executable_keywords:
                    pattern = re.escape(keyword)  # Escape the special characters in the keyword for regex
                    if re.search(pattern, line):
                        logger.error(f"Line {line_number} is considered executable due to the presence of keyword: '{keyword}'")
                        found_executable_code = True

            #if found_executable_code:
                #logger.info("The header file contains executable code.")
            #else:
                #logger.info("The header file does not contain executable code.")

        except Exception as e:
            logger.warning(f"An error occurred during C Rule 016 execution: {e}")

def RBCM_C_RULE_035(file_path):
    """

        Function name: RBCM_C_RULE_035

        Description: The RBCM_C_RULE_035 function performs a C style check for block statements, confirming if
        the opening and closing brackets are placed one below the other in the same column and in different rows 

        :Usage example:

            :RBCM_C_RULE_035(Path):
        // path of the c file 
            
        :return: Log detail of the c file validation.

    """
    if str(file_path).endswith(".c"):

        logging_utils.log_info(logger, "RBCM_C_RULE_035", "Check brace alignment in c files")

        try:
            with open(file_path, 'r', encoding='utf8') as file:
                lines = file.readlines()

            indentation_levels = []
            line_number = 0
            #found_indentation = True

            for line in lines:
                line_number += 1
                stripped_line = line.strip()

                if stripped_line.startswith('{'):
                    indentation_levels.append(len(line) - len(line.lstrip()))
                elif stripped_line.startswith('}'):
                    if indentation_levels:
                        expected_indentation = indentation_levels.pop()
                        actual_indentation = len(line) - len(line.lstrip())
                        if actual_indentation != expected_indentation:
                            logging.error(f"Brace misalignment at line {line_number}")
                            #found_indentation = False
                    else:
                        logging.error(f"Unmatched closing brace at line {line_number}")
                        #found_indentation = False

            #if found_indentation:
                #logging.info("All braces are aligned correctly")

        except FileNotFoundError:
            logging.warning(f"File not found: {file_path}")
        except Exception as e:
            logging.warning(f"An error occurred: {e}")

def RBCM_C_RULE_037(file_path):
    """

        Function name: RBCM_C_RULE_037

        Description: The RBCM_C_RULE_037 function performs a C style check if control flow 
        statements (if, else, else if, switch, do, for, while, etc.) are always followed by a block. 

        :Usage example:

            :RBCM_C_RULE_037(Path):
        // path of the c file 
            
        :return: Log detail of the c file validation.

    """
    if str(file_path).endswith(".c"):

        logging_utils.log_info(logger, "RBCM_C_RULE_037", "Check presence of blocks after control flow statements in c files")

        try:
            lines = common.remove_comments(file_path)

            control_flow_keywords = ['if', 'else', 'switch', 'do', 'for', 'while']
            pattern_indices = []

            for idx, line in enumerate(lines):
                if not line.strip().startswith('#'):  # Skip #if and #else statements
                    for keyword in control_flow_keywords:
                        block = re.search(fr'\b{keyword}\s*\(.*\)\s*[^{{]*$', line) or (keyword == 'else' and re.search(r'\belse\b', line))
                        if block and idx not in pattern_indices:
                            pattern_indices.append(idx)

            if not pattern_indices:
                return

            for i in range(len(pattern_indices) - 1):
                start_idx = pattern_indices[i]
                end_idx = pattern_indices[i + 1]

                found_brace = False
                if end_idx - start_idx < 5:
                    for idx in range(start_idx, end_idx):
                        line = lines[idx]
                        if re.search(r'^\s*{', line):
                            found_brace = True
                            break

                    if not found_brace:
                        logger.error(f"Rule violation at line {start_idx + 1}: {lines[start_idx].strip()}")
                        
                else:
                    for idx in range(start_idx, start_idx + 5):
                        line = lines[idx]
                        if re.search(r'^\s*{', line):
                            break
                    else:
                        logger.error(f"Rule violation at line {start_idx + 1}: {lines[start_idx].strip()}")

            last_pattern_idx = pattern_indices[-1]
            for idx in range(last_pattern_idx + 1, min(last_pattern_idx + 5, len(lines))):
                line = lines[idx]
                if re.search(r'^\s*{', line):
                    break

            else:
                logger.error(f"Rule violation at line {last_pattern_idx + 1}: {lines[last_pattern_idx].strip()}")

        except FileNotFoundError:
            logger.warning(f"File not found: {file_path}")
        except Exception as e:
            logger.warning(f"An error occurred: {e}")

def RBCM_C_RULE_010(file_path):
    """

        Function name: RBCM_C_RULE_010

        Description: The RBCM_C_RULE_010 function performs a C style check for the correctness of 
        headers of the global function prototypes in c source files. 

        :Usage example:

            :RBCM_C_RULE_010(Path):
        // path of the c file 
            
        :return: Log detail of the c file validation.

    """
    if str(file_path).endswith(".c"):

        logging_utils.log_info(logger, "RBCM_C_RULE_010", "Check function header of global functions in c files")
      
        with open(file_path, 'r', encoding='utf8') as file:
            c_lines = file.readlines()
    
        #errors_found = False  
        function_definition_pattern = re.compile(r'\b\w+\b\s+\w+\s*\([^)]*\)\s*{', re.MULTILINE)
        functions = function_definition_pattern.findall("".join(c_lines))
        # Remove functions that start with 'else if'
        functions = [func for func in functions if not func.startswith('else if')]
        #print(f"Found {len(functions)} functions in the file.")
        #print(functions)

        if not functions:
            #logger.info("No function found in the file.")
            return
    
        c_lines_without_comments = common.remove_comments(file_path)
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
                    #errors_found = True
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
                    #errors_found = True
                    continue

                # Join the comments to form a string and store them in the dictionary
                function_comments[function] = '\n'.join(comments)

                # Parse the comments for the current function
                comment_parser = CommentParser(r'C:\Users\LQR1COB\Downloads\c_files\RBCM_C_RULE_011\conf.cfg')
                comments_dict = comment_parser.parse_comments(function_comments[function])
                #print(comments_dict)

                # Check if function name, return type, and parameters match the comments
                if 'FUNCTION' in comments_dict and function_name not in comments_dict['FUNCTION']:
                    logger.error(f"Function name in header '{(comments_dict['FUNCTION'])}' is not matched with function name in definition '{function_name}' in line {line_number+1}")
                    #errors_found = True

                if 'PARAM' not in comments_dict:
                    logger.error(f"'PARAM' section is missing in function header for '{function}' in line {line_number+1}")
                    #errors_found = True

                elif 'PARAM' in comments_dict and parameters not in comments_dict['PARAM']:
                    logger.error(f"Parameter in header '{(comments_dict['PARAM'])}' is not matched with parameters in definition '{parameters}' in line {line_number+1}")
                    #errors_found = True

                if 'RETURN' not in comments_dict:
                    logger.error(f"'RETURN' section is missing in function header for '{function}' in line {line_number+1}")
                    #errors_found = True

                if 'RETURN' in comments_dict and return_type not in comments_dict['RETURN']:
                    logger.error(f"Return type in header: '{(comments_dict['RETURN'])}' is not matched with return type in definition '{return_type}' in line {line_number+1}")
                    #errors_found = True

                if 'BRIEF' not in comments_dict:
                    logger.error(f"'BRIEF' section is missing in function header for '{function}' in line {line_number+1}")
                    #errors_found = True

                # Check if 'BRIEF' section has some contents written
                if 'BRIEF' in comments_dict and not comments_dict['BRIEF']:
                    logger.error(f"'BRIEF' section is empty in function header for '{function}' in line {line_number+1}")
                    #errors_found = True

            except Exception as e:
                logger.warning(f"Error processing function header for {function}")
                logger.warning(f"Error message: {e}")

        #if not errors_found:
            #logger.info(f"All function headers are valid and complete.")

def RBCM_C_RULE_011(file_path):
    """

        Function name: RBCM_C_RULE_011

        Description: The RBCM_C_RULE_011 function performs a C style check for the correctness of 
        headers of the global function prototypes in header files. 

        :Usage example:

            :RBCM_C_RULE_011(Path):
        // path of the header file 
            
        :return: Log detail of the header file validation.

    """
    if str(file_path).endswith(".h"):

        logging_utils.log_info(logger, "RBCM_C_RULE_011", "Check function header of global functions in h files")
        
        with open(file_path, 'r', encoding='utf8') as file:
            h_lines = file.readlines()
    
        #errors_found = False
        function_prototype_pattern = re.compile(r'\b\w+\b\s+\w+\s*\([^)]*\)\s*;', re.MULTILINE)
        function_prototypes = function_prototype_pattern.findall("".join(h_lines))
        #print(f"Found {len(function_prototypes)} function prototypes in the file.")
        #print(function_prototypes)

        if not function_prototypes:
            #logger.info("No function prototypes found in the file.")
            return
    
        function_comments = {}  # Dictionary to store comments for each function prototype
    
        # Find the comments for each function prototype
        for function_prototype in function_prototypes:

            try:
                # Get the line number of the current function prototype
                line_number = None
                for idx, line in enumerate(h_lines):
                    if function_prototype in line:
                        line_number = idx
                        break

                if line_number is None:
                    logger.error(f"Function header for '{function_prototype}' not found in the file.")
                    #errors_found = True
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
                    #errors_found = True
                    continue

                # Join the comments to form a string and store them in the dictionary
                function_comments[function_prototype] = '\n'.join(comments)

                # Parse the comments for the current function prototype
                comment_parser = CommentParser(r'C:\Users\LQR1COB\Downloads\c_files\RBCM_C_RULE_011\conf.cfg')
                comments_dict = comment_parser.parse_comments(function_comments[function_prototype])
                #print(comments_dict)

                # Pattern to strip return type from the function prototype
                function_name = re.findall(r'^\s*\w+\s+(\w+)\s*\([^)]*\)', function_prototype)[0].strip()
                parameters = re.findall(r'^\s*\b\w+\b\s+\w+\s*\(([^)]*)\)\s*;$', function_prototype)[0].strip()
                return_type = re.sub(r'\b\w+\b\s*\([^)]*\)', '', function_prototype).strip().rstrip(';').rstrip(' ')
        
                #print({function_name}, {parameters}, {return_type})

                # Check if function name, return type, and parameters match the comments
                if 'FUNCTION' in comments_dict and function_name not in comments_dict['FUNCTION']:
                    logger.error(f"Function name in header '{(comments_dict['FUNCTION'])}' is not matched with function name in prototype '{function_name}' in line {line_number+1}")
                    #errors_found = True

                if 'PARAM' not in comments_dict:
                    logger.error(f"'PARAM' section is missing in function header for '{function_prototype}' in line {line_number+1}")
                    #errors_found = True

                elif 'PARAM' in comments_dict and parameters not in comments_dict['PARAM']:
                    logger.error(f"Parameter in header '{(comments_dict['PARAM'])}' is not matched with parameters in prototype '{parameters}' in line {line_number+1}")
                    #errors_found = True

                if 'RETURN' not in comments_dict:
                    logger.error(f"'RETURN' section is missing in function header for '{function_prototype}' in line {line_number+1}")
                    #errors_found = True

                if 'RETURN' in comments_dict and return_type not in comments_dict['RETURN']:
                    logger.error(f"Return type in header: '{(comments_dict['RETURN'])}' is not matched with return type in prototype '{return_type}' in line {line_number+1}")
                    #errors_found = True

                if 'BRIEF' not in comments_dict:
                    logger.error(f"'BRIEF' section is missing in function header for '{function_prototype}' in line {line_number+1}")
                    #errors_found = True

                # Check if 'BRIEF' section has some contents written
                if 'BRIEF' in comments_dict and not comments_dict['BRIEF']:
                    logger.error(f"'BRIEF' section is empty in function header for '{function_prototype}' in line {line_number+1}")
                    #errors_found = True

            except Exception as e:
                logger.warning(f"Error processing function header for {function_prototype}")
                logger.warning(f"Error message: {e}")

        #if not errors_found:
            #logger.info(f"All function headers are valid and complete.")

if __name__ == "__main__":

    #path = r"C:\Users\LQR1COB\Downloads\c_files\AurixSafetyStartup"
    #path = r"C:\Users\LQR1COB\Downloads\c_files\RegisterMonitor"
    path = r"C:\Users\LQR1COB\Downloads\c_files\AurixSafetyManager"
    #path = r"C:\Users\LQR1COB\Downloads\c_files\Platform"
    #path = r"C:\Users\LQR1COB\Downloads\c_files\Platform\Aurix.FIT_Manager\Au_FITM.c"
    #path = r"C:\Users\LQR1COB\Downloads\c_files\Platform\Aurix.FIT_Manager\Au_FITM.h"

    test_files = common.find_files(path)
    
    for file_path in test_files:
        logger.info(f"Checking {file_path} ..... ")
        # check in .h files
        RBCM_C_RULE_016(file_path)
        RBCM_C_RULE_011(file_path)
        # check in .c files
        RBCM_C_RULE_010(file_path)
        RBCM_C_RULE_035(file_path)
        RBCM_C_RULE_037(file_path)
        logger.info("==============================================================================================================================")

print("Checking Completed")