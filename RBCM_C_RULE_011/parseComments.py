import re
import ply.lex as lex

# Read tags from the config file
with open(r'C:\Users\LQR1COB\Downloads\c_files\RBCM_C_RULE_011\conf.cfg') as config_file:
    tags = [tag.strip().upper() for tag in config_file]
#print(tags)

# Regular expression to match multiline comments
multiline_comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)

# Lexer tokens
tokens = [tag.upper() for tag in tags] + ['ERROR']
#print(tokens)

# Lexer rules for each tag
def t_FUNCTION(t):
    r'FUNCTION:'
    return t

def t_BRIEF(t):
    r'\\brief\b'
    return t

def t_PARAM(t):
    r'\\param\b'
    return t

def t_RETURN(t):
    r'\\return\b'
    return t

def t_PRE(t):
    r'\\pre\b'
    return t

def t_POST(t):
    r'\\post\b'
    return t

def t_ATTENTION(t):
    r'\\attention\b'
    return t

def t_TODO(t):
    r'\\todo\b'
    return t

# Lexer rule for error handling
def t_error(t):
    t.type = 'ERROR'
    t.value = t.value[1:]  # Remove the backslash character
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def parse_comments_for_prototype(prototype):
    comments = {}
    #print(prototype)
    matches = re.finditer(multiline_comment, prototype)

    for match in matches:
        comment = match.group(1).strip()
        lexer.input(comment)

        # Extract the tags and their content from the comment
        for tok in lexer:
            if tok.type in tags:
                content_start = tok.lexpos + len(tok.value)
                content = comment[content_start:].strip()
                if tok.type in ['BRIEF','PRE','POST','ATTENTION','TODO']:
                    content = content.replace('\n*', '')
                    # Strip following content after the first tag
                    next_tag_pos = content.find('\\')
                    if next_tag_pos != -1:
                        content = content[:next_tag_pos].strip()
                else:
                    content = content.split('\n', 1)[0].strip()
                comments[tok.type] = content

    return comments
