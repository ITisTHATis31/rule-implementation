import re, os, logging
import ply.lex as lex

class logging_utils:

    def setup_logging(log_file):
        logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

    def get_logger(name):
        return logging.getLogger(name)

    def log_info(logger, rule_name, rule_info):
        logger.info("==============================================================================================================================")
        # Log the rule name and the rule information
        logger.info("#"*75)
        logger.info(f" Rule : {rule_name}, Rule Info : {rule_info}")
        logger.info(f"#"*75)

# Configure the logging for the main script
log_file = "C_Style_check.log"
logging_utils.setup_logging(log_file)
logger = logging_utils.get_logger(__name__)

class common:
    
    def find_header_files(parent_folder):
        header_files = []
        for root, dirs, files in os.walk(parent_folder):
            for file in files:
                if file.endswith(".h"):
                    header_file_path = os.path.join(root, file)
                    header_files.append(header_file_path)
        return header_files
        
    def find_c_files(parent_folder):
        c_files = []
        for root, dirs, files in os.walk(parent_folder):
            for file in files:
                if file.endswith(".c"):
                    c_file_path = os.path.join(root, file)
                    c_files.append(c_file_path)
        return c_files

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

    def parse_comments_for_prototype(self, prototype):
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

class RBCM_C_RULE_016():

    def __init__(self, file_path):
        self.file_path = file_path

    #getting file path as argument for checking_executable_code_in_header
    def check_executable_code_in_header(lines):
        """

            Function name: check_executable_code_in_header

            Description: The check_executable_code_in_header function performs a C style check for potential executable code in a list of header files. 
            The function validates by confirming non-executable codes in a header file.

            :Usage example:

                :check_executable_code_in_header(lines):
            // lines of the header file 
            
            :return: Log detail of the header file validation.

        """
        executable_keywords = [r'main\s*\(', r'for\s*\(', r'if\s*\(', 'else', 'while', 'break', 'continue', 'goto', 'switch ', 'return ']
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
            logger.warning(f"An error occurred during C Rule 016 execution: {e}")
            found_executable_code = False

        return found_executable_code
    
    def main_script(cls, file_path):

        header_files = common.find_header_files(file_path)

        if header_files:  # If the path of the parent folder is given
            logging_utils.log_info(logger, "RBCM_C_RULE_016", "Check executable code in header file")
            for header_file in header_files:
                logger.info(f"Checking {header_file} for executable code ..... ")
                lines_with_comments_removed = common.remove_comments(header_file)  # remove_comments returns a list
                found_code = RBCM_C_RULE_016.check_executable_code_in_header(lines_with_comments_removed)
                if found_code:
                    logger.info("The header file contains executable code.")
                else:
                    logger.info("The header file does not contain executable code.")

        else:  # If the path of the header file itself is given
            if file_path.endswith(".h"):
                logging_utils.log_info(logger, "RBCM_C_RULE_016", "Check executable code in header file")
                logger.info(f"Checking {file_path} for executable code ..... ")
                lines_with_comments_removed = common.remove_comments(file_path)  # remove_comments returns a list
                found_code = RBCM_C_RULE_016.check_executable_code_in_header(lines_with_comments_removed)
                if found_code:
                    logger.info("The header file contains executable code.")
                else:
                    logger.info("The header file does not contain executable code.")

class RBCM_C_RULE_035:

    def __init__(self, file_path):
        self.file_path = file_path

    def check_braces(file_path):
        """

            Function name: check_braces

            Description: The check_braces function performs a C style check for block statements, confirming if
            the opening and closing brackets are placed one below the other in the same column and in different rows 

            :Usage example:

                :check_braces(Paths):
            // path of the repo or c file 
            
            :return: Log detail of the c file validation.

        """
        try:
            with open(file_path, 'r', encoding='utf8') as file:
                lines = file.readlines()

            indentation_levels = []
            line_number = 0
            found_indentation = True

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
                            found_indentation = False
                    else:
                        logging.error(f"Unmatched closing brace at line {line_number}")
                        found_indentation = False

            if found_indentation:
                logging.info("All braces are aligned correctly")

        except FileNotFoundError:
            logging.warning(f"File not found: {file_path}")
        except Exception as e:
            logging.warning(f"An error occurred: {e}")

    def main_script(cls, file_path):
        c_files = common.find_c_files(file_path)

        if c_files:  # If the path of the parent folder is given
            logging_utils.log_info(logger, "RBCM_C_RULE_035", "Check brace alignment in c files")
            for c_file in c_files:
                logger.info(f"Checking brace alignment in {c_file} ..... ")
                RBCM_C_RULE_035.check_braces(c_file)

        else:  # If the path of the h file itself is given
            if file_path.endswith(".c"):
                logging_utils.log_info(logger, "RBCM_C_RULE_035", "Check brace alignment in c files")
                logger.info(f"Checking brace alignment in {file_path} ..... ")
                RBCM_C_RULE_035.check_braces(file_path)

class RBCM_C_RULE_037:

    def __init__(self, file_path):
        self.file_path = file_path
  
    def check_blocks(file_path):
        """

            Function name: check_blocks

            Description: The check_blocks function performs a C style check if control flow 
            statements (if, else, else if, switch, do, for, while, etc.) are always followed by a block. 

            :Usage example:

                :check_blocks(Paths):
            // path of the repo or c file 
            
            :return: Log detail of the c file validation.

        """
        try:
            lines = common.remove_comments(file_path)

            control_flow_keywords = ['if', 'else', 'switch', 'do', 'for', 'while']
            pattern_indices = []
            found_violation = False

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
                        found_violation = True
                else:
                    for idx in range(start_idx, start_idx + 5):
                        line = lines[idx]
                        if re.search(r'^\s*{', line):
                            break
                    else:
                        logger.error(f"Rule violation at line {start_idx + 1}: {lines[start_idx].strip()}")
                        found_violation = True

            last_pattern_idx = pattern_indices[-1]
            for idx in range(last_pattern_idx + 1, min(last_pattern_idx + 5, len(lines))):
                line = lines[idx]
                if re.search(r'^\s*{', line):
                    break

            else:
                logger.error(f"Rule violation at line {last_pattern_idx + 1}: {lines[last_pattern_idx].strip()}")
                found_violation = True
                
            if not found_violation:
                logger.info("All control flow statements are followed by a block.")

        except FileNotFoundError:
            logger.warning(f"File not found: {file_path}")
        except Exception as e:
            logger.warning(f"An error occurred: {e}")
    
    def main_script(cls, file_path):
        c_files = common.find_c_files(file_path)

        if c_files:  # If the path of the parent folder is given
            logging_utils.log_info(logger, "RBCM_C_RULE_037", "Check presence of blocks after control flow statements in c files")
            for c_file in c_files:
                logger.info(f"Check presence of blocks after control flow statements in {c_file} ..... ")
                RBCM_C_RULE_037.check_blocks(c_file)

        else:  # If the path of the h file itself is given
            if file_path.endswith(".c"):
                logging_utils.log_info(logger, "RBCM_C_RULE_037", "Check presence of blocks after control flow statements in c files")
                logger.info(f"Check presence of blocks after control flow statements in {file_path} ..... ")
                RBCM_C_RULE_037.check_blocks(file_path)

class RBCM_C_RULE_010:

    def __init__(self, file_path):
        self.file_path = file_path

    def check_function(file_path):
        """

            Function name: check_function

            Description: The check_function function performs a C style check for the correctness of 
            headers of the global function prototypes in c source files. 

            :Usage example:

                :check_function(Paths):
            // path of the repo or header file 
            
            :return: Log detail of the c file validation.

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
                comment_parser = CommentParser(r'C:\Users\LQR1COB\Downloads\c_files\RBCM_C_RULE_011\conf.cfg')
                comments_dict = comment_parser.parse_comments_for_prototype(function_comments[function])
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
                logger.warning(f"Error processing function header for {function}")
                logger.warning(f"Error message: {e}")

        if not errors_found:
            logger.info(f"All function headers are valid and complete.")

    def main_script(cls, file_path):
        c_files = common.find_c_files(file_path)

        if c_files:  # If the path of the parent folder is given
            logging_utils.log_info(logger, "RBCM_C_RULE_010", "Check function header of global functions in c files")
            for c_file in c_files:
                logger.info(f"Checking function headers in {c_file} ..... ")
                RBCM_C_RULE_010.check_function(c_file)

        else:  # If the path of the h file itself is given
            if file_path.endswith(".c"):
                logging_utils.log_info(logger, "RBCM_C_RULE_010", "Check function header of global functions in c files")
                logger.info(f"Checking function headers in {file_path} ..... ")
                RBCM_C_RULE_010.check_function(file_path)

class RBCM_C_RULE_011:

    def __init__(self, file_path):
        self.file_path = file_path

    def check_prototype(file_path):
        """

            Function name: check_prototype

            Description: The check_prototype function performs a C style check for the correctness of 
            headers of the global function prototypes in header files. 

            :Usage example:

                :check_prototype(Paths):
            // path of the repo or header file 
            
            :return: Log detail of the header file validation.

        """

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

            try:
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
                comment_parser = CommentParser(r'C:\Users\LQR1COB\Downloads\c_files\RBCM_C_RULE_011\conf.cfg')
                comments_dict = comment_parser.parse_comments_for_prototype(function_comments[function_prototype])
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

            except Exception as e:
                logger.warning(f"Error processing function header for {function_prototype}")
                logger.warning(f"Error message: {e}")

        if not errors_found:
            logger.info(f"All function headers are valid and complete.")

    def main_script(cls, file_path):
        h_files = common.find_header_files(file_path)

        if h_files:  # If the path of the parent folder is given
            logging_utils.log_info(logger, "RBCM_C_RULE_011", "Check function header of global functions in c files")
            for h_file in h_files:
                logger.info(f"Checking function headers in {h_file} ..... ")
                RBCM_C_RULE_011.check_prototype(h_file)

        else:  # If the path of the h file itself is given
            if file_path.endswith(".h"):
                logging_utils.log_info(logger, "RBCM_C_RULE_011", "Check function header of global functions in c files")
                logger.info(f"Checking function headers in {file_path} ..... ")
                RBCM_C_RULE_011.check_prototype(file_path)

if __name__ == "__main__":

    file_path = r"C:\Users\LQR1COB\Downloads\c_files\Platform"
    #file_path = r"C:\Users\LQR1COB\Downloads\c_files\Platform\Aurix.FIT_Manager\Au_FITM.c"
    #file_path = r"C:\Users\LQR1COB\Downloads\c_files\Platform\Aurix.FIT_Manager\Au_FITM.h"

    # check in .h files
    RBCM_C_RULE_016.main_script(RBCM_C_RULE_011, file_path)
    RBCM_C_RULE_011.main_script(RBCM_C_RULE_016, file_path)
    # check in .c files
    RBCM_C_RULE_010.main_script(RBCM_C_RULE_010, file_path)
    RBCM_C_RULE_035.main_script(RBCM_C_RULE_035, file_path)
    RBCM_C_RULE_037.main_script(RBCM_C_RULE_037, file_path)

print("Checking Completed")