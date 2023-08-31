import re, os, logging
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

def RBCM_C_RULE_037(filename):
    try:
        lines = remove_comments(filename)

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
        logger.error(f"File not found: {filename}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

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
        log_info(logger, "Check presence of blocks after control flow statements in c files")
        for c_file in c_files:
            logger.info(f"Check presence of blocks after control flow statements in {c_file} ..... ")
            RBCM_C_RULE_037(c_file)

    else:  # If the path of the h file itself is given
        log_info(logger, "Check presence of blocks after control flow statements in c files")
        logger.info(f"Check presence of blocks after control flow statements in {c_file_path} ..... ")
        RBCM_C_RULE_037(c_file_path)

print("Checking Completed")