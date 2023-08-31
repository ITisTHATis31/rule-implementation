import re

def check_c_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    control_flow_keywords = ['if', 'else', 'else if', 'switch', 'do', 'for', 'while']

    inside_block = False
    pattern_line = None  # Initialize pattern_line

    for idx, line in enumerate(lines):
        if not line.strip().startswith('#'):  # Skip #if and #else statements
            for keyword in control_flow_keywords:
                if re.search(fr'\b{keyword}\s*\(.*\)\s*[^{{]*$', line) or (keyword == 'else' and re.search(r'\belse\b', line)):
                    inside_block = True
                    pattern_line = idx + 1

        if inside_block and "{" in line:
            inside_block = False

        elif inside_block and "{" not in line:
            if idx >= pattern_line:
                if any(keyword in line for keyword in control_flow_keywords):
                    print(f"Rule violation at line {pattern_line}: {lines[pattern_line - 1].strip()}")
                    inside_block = False
         
if __name__ == "__main__":
    c_file_path = r"C:\Users\LQR1COB\Downloads\c_files\RBCM_C_RULE_035\Au_FITM.c"
    check_c_file(c_file_path)
