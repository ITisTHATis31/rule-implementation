from comment_parser import comment_parser

# Parse the comments from the function prototype
comments = comment_parser.extract_comments(r'C:\Users\LQR1COB\Downloads\c_files\RBCM_C_RULE_011\Au_FITM.h',mime='text/x-c')

print(comments)

