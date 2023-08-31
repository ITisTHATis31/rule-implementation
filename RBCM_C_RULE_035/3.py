import re

def check_c_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        control_flow_keywords = ['if', 'else', 'switch', 'do', 'for', 'while']
        pattern_indices = []

        for idx, line in enumerate(lines):
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
                    print(f"Rule violation at line {start_idx + 1}: {lines[start_idx].strip()}")
            else:
                for idx in range(start_idx, start_idx + 5):
                    line = lines[idx]
                    if re.search(r'^\s*{', line):
                        break
                else:
                    print(f"Rule violation at line {start_idx + 1}: {lines[start_idx].strip()}")

        last_pattern_idx = pattern_indices[-1]
        for idx in range(last_pattern_idx + 1, min(last_pattern_idx + 5, len(lines))):
            line = lines[idx]
            if re.search(r'^\s*{', line):
                break
        else:
            print(f"Rule violation at line {last_pattern_idx + 1}: {lines[last_pattern_idx].strip()}")
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    c_file_path = r"C:\Users\LQR1COB\Downloads\c_files\RBCM_C_RULE_035\Au_FITM.c"
    check_c_file(c_file_path)