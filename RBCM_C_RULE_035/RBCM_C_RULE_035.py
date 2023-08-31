import os, logging

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

def RBCM_C_RULE_035(filename):
    try:
        with open(filename, 'r', encoding='utf8') as file:
            lines = file.readlines()

        indentation_levels = []
        line_number = 0

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
                        logging.warning(f"Brace misalignment at line {line_number}")
                else:
                    logging.warning(f"Unmatched closing brace at line {line_number}")

    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    
    #c_file_path = r"C:\Users\LQR1COB\Downloads\c_files\RBCM_C_RULE_035\Au_FITM.c"
    c_file_path = r"C:\Users\LQR1COB\Downloads\c_files\Platform"
    c_files = []
    for root, dirs, files in os.walk(c_file_path):
        for file in files:
            if file.endswith(".c"):
                c_path = os.path.join(root, file)
                c_files.append(c_path)

    if c_files:  # If the path of the parent folder is given
        log_info(logger, "Check brace alignment in c files")
        for c_file in c_files:
            logger.info(f"Checking brace alignment in {c_file} ..... ")
            RBCM_C_RULE_035(c_file)

    else:  # If the path of the h file itself is given
        log_info(logger, "Check brace alignment in c files")
        logger.info(f"Checking brace alignment in {c_file_path} ..... ")
        RBCM_C_RULE_035(c_file_path)

print("Checking Completed")