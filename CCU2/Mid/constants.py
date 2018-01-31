REPR = 0
VALUE = 1

# Token types

# operators
# most tokens are a tuple of repr, value
PLUS = ("plus", "+")
MINUS = ("minus", "-")
MULTIPLY = ("multiply", "*")
DIVIDE = ("division", "/")
ASSIGN = ("assign", "=")

OPERATORS = (PLUS, MINUS, MULTIPLY, DIVIDE, ASSIGN)

# delimiters
LPAREN = ("left bracket", "(")
RPAREN = ("right bracket", ")")
SEMICOLON = ("semicolon", ";")
DOT = ("dot", ".")
COLON = ("colon", ":")
COMMA = ("comma", ",")

DELIMITERS = (LPAREN, RPAREN, SEMICOLON, DOT, COLON, COMMA)

# comments
COMMENT_START = ("comment block start", "/*")
COMMENT_END = ("comment block end", "*/")
LINE_COMMENT = ("line comment", "//")

# type literals
INT_LITERAL = "int literal"
FLOAT_LITERAL = "float literal"
STR_LITERAL = "str literal"

# identifiers have to be specified with this type
IDENTIFIER = "identifier"

# indents and dedents
# indent is for all tab spaces or 4 " " at the beginning of a line
# dedent is for the removal of said spaces
INDENT = "indent"
DEDENT = "dedent"

# these won't be used for their repr, but just for their values
# note that only tab indents are being supported right now
TAB_INDENT = "\t"

# keywords
INT_TYPE = ("int keyword", "int")
FLOAT_TYPE = ("float keyword", "float")
STR_TYPE = ("str keyword", "str")
BOOL_TYPE = ("bool keyword", "bool")
VOID_TYPE = ("void keyword", "void")

TRUE_CONST = ("true keyword const", "true")
FALSE_CONST = ("true keyword const", "false")
NULL_CONST = ("null keyword const", "null")

FOR = ("for keyword", "for")
WHILE = ("while keyword", "while")
BREAK = ("break keyword", "break")
CONTINUE = ("continue keyword", "continue")
IF = ("if keyword", "if")
ELIF = ("elif keyword", "elif")
ELSE = ("else keyword", "else")
PASS = ("pass keyword", "pass")

CMP_STMT_KEYWORDS = (FOR, WHILE, IF, ELIF, ELSE)
STMT_KEYWORDS = (BREAK, CONTINUE, PASS)
VAR_DECL_TYPE = (INT_TYPE, FLOAT_TYPE, STR_TYPE, BOOL_TYPE)
RETURN_TYPE = (INT_TYPE, FLOAT_TYPE, STR_TYPE, BOOL_TYPE, VOID_TYPE)
VAR_CONSTS = (TRUE_CONST, FALSE_CONST, NULL_CONST)

ALL_KEYWORDS = CMP_STMT_KEYWORDS + STMT_KEYWORDS + RETURN_TYPE + VAR_CONSTS

# other
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
EOF = "end of file"
NEWLINE = ("newline", "\n")

