import re

def extract_control_flow_statements(filename):
    with open(filename, 'r') as file:
        content = file.read()

    pattern = r'\b(if|else|else if|while|for|switch)\s*\([^)]*\)\s*(:|\{)'

    control_flow_statements = re.findall(pattern, content, re.DOTALL)

    return control_flow_statements

if __name__ == "__main__":
    c_file_path = r"C:\Users\LQR1COB\Downloads\c_files\RBCM_C_RULE_035\Au_FITM.c"
    statements = extract_control_flow_statements(c_file_path)
    for idx, statement in enumerate(statements):
        print(f"Control Flow Statement {idx + 1}: {statement[0]} {statement[1]}")
