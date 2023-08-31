import os

def find_header_files(parent_folder):
    header_files = []
    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            if file.endswith(".h"):
                header_path = os.path.join(root, file)
                header_files.append(header_path)
    return header_files