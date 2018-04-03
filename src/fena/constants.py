
# contains type and value
TYPE = 0
VALUE = 1
PLUS = ("plus", "+")
MINUS = ("minus", "-")
EQUALS = ("equals", "=")
TEST = ("test", "?")
RESET = ("reset", "reset")
ENABLE = ("enable", "enable")
JOIN = ("join", "join")
EMPTY = ("empty", "empty")
LEAVE = ("leave", "leave")
DETECT = ("detect", "detect")
IFBLOCK = ("ifblock", "ifblock")

# simple tokens because they all have a set value
SIMPLE_TOKENS = (PLUS, MINUS, EQUALS, TEST, RESET, ENABLE, JOIN, EMPTY, LEAVE, DETECT, IFBLOCK)

# only type
SELECTOR = "selector"
INT = "int"
FLOAT = "float"
COORD = "coord"
COORDS = "coords"
DATATAG = "datatag"
STRING = "string"
COMMAND = "command"
LEADING_COMMAND = "leading command"
COMMENT = "comment"

# post statements
PATH = ("path", "path")
MFUNC = ("mfunc", "mfunc")

# other
STATEMENT = ("statement", "!")
INDENT = ("indent", "    ")
DEDENT = ("dedent", "dedent")
NEWLINE = ("newline", "\n")
EOF = ("EOF", None)

# config data
COMMANDS = "commands"
LEADING_COMMANDS = "leadingCommands"
PLUGIN_CONFLICT_COMMANDS = "pluginConflictCommands"
SELECTOR_TYPES = "selectorTypes"
SELECTOR_VARIABLES = "selectorVariables"
CONFIG_OPTIONS = (COMMANDS, LEADING_COMMANDS, PLUGIN_CONFLICT_COMMANDS, SELECTOR_TYPES, SELECTOR_VARIABLES)
