import re

def remove_comments(line):
    # Remove inline comments
    line = re.sub(r'\/\/.*', '', line)

    # Remove block comments
    line = re.sub(r'\/\*.*?\*\/', '', line)

    return line.strip()
