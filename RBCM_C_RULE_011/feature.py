import re
import ply.lex as lex

# List of tags to extract from comments
tags = ['FUNCTION', 'BRIEF', 'PARAM', 'RETURN', 'PRE', 'POST', 'ATTENTION', 'TODO']

# Regular expression to match multiline comments
multiline_comment = r'/\*(.*?)\*/'

# Lexer tokens
tokens = [tag.upper() for tag in tags] + ['ERROR']

# Lexer rules for each tag
def t_FUNCTION(t):
    r'FUNCTION:'
    return t

def t_BRIEF(t):
    r'\\BRIEF\b'
    return t

def t_PARAM(t):
    r'\\PARAM\b'
    return t

def t_RETURN(t):
    r'\\RETURN\b'
    return t

def t_PRE(t):
    r'\\PRE\b'
    return t

def t_POST(t):
    r'\\POST\b'
    return t

def t_ATTENTION(t):
    r'\\ATTENTION\b'
    return t

def t_TODO(t):
    r'\\TODO\b'
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
    matches = re.finditer(multiline_comment, prototype, re.DOTALL)

    for match in matches:
        comment = match.group(1).strip()
        lexer.input(comment)

        # Extract the tags and their content from the comment
        for tok in lexer:
            if tok.type in tags:
                content_start = tok.lexpos + len(tok.value)
                content = comment[content_start:].strip()
                if tok.type == 'BRIEF':
                    content = content.replace('\n', '')
                    # Strip following content after the first tag
                    next_tag_pos = content.find('\\')
                    if next_tag_pos != -1:
                        content = content[:next_tag_pos].strip()
                else:
                    content = content.split('\n', 1)[0].strip()
                    
                comments[tok.type] = content

    return comments

# Test example
prototype = """
/**
 *  FUNCTION:   Au_FITM_MainFunction_ASIL(void)
 */
/*! \BRIEF This is the ASIL runnable mapped to 100ms task and it switches to different
 *         functions depending on the core ID.
 *  \PARAM void
 *  \RETURN void
 *  \PRE None
 *  \POST None
 *  \ATTENTION None
 *  \TODO None
 *
 *
 */"""

parsed_comments = parse_comments_for_prototype(prototype)
print(parsed_comments)

