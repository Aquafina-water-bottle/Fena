r"""
Runs a quick script before pyexpander is run
Features:
    - replaces all \\ with \\\\
    - changes some syntax of pyexpander code to make it more elegant to work with for fena code

Syntax changes:

# general python code using $py() and macros using $macro(identifier) will be 0 indented
```
$py(
code = "unchanged"
)

$py:
    idk = []
    for x in range(15):
        idk.append(x*2)

!mfunc hello
    $py:
        somedict = {}
        for x in range(15):
            somedict[x] = "ayylmao"

$macro(edit_give_porkchops):
    say this is a macro

$macro(unchanged)
    say this is an unchanged macro
$endmacro
------ TO ------
$py(
code = "unchanged"
)

$py(
idk = []
for x in range(15):
    idk.append(x*2)
)

!mfunc hello
$py(
somedict = {}
for x in range(15):
    somedict[x] = "ayylmao"
)

$macro(edit_give_porkchops)
say this is a macro
$endmacro

$macro(unchanged)
    say this is an unchanged macro
$endmacro
```

# for loops and anything else with $keyword() and $endkeyword
$for(x in range(5)):
    !mfunc give_porkchop_$(x)
        give @s minecraft:porkchop $(x)

!mfunc give_porkchops
    $for(x in range(5)):
        @s[porkchop=$(x)] function give_porkchop_$(x)

    $for(_ in range(3))
    $("say unchanged code")
    $endfor

------ TO ------
$for(x in range(5))
!mfunc set_$(x)
    give @s minecraft:porkchop $(x)
$endfor

!mfunc give_porkchops
    $for(x in range(5))
    @s[porkchop=$(x)] function give_porkchop_$(x)
    $endfor

    $for(_ in range(3))
    $("say unchanged code")
    $endfor
```

```
$for(x in range(15)):


------ TO ------
"""

from enum import Enum, auto
import keyword

import assert_utils

# all python keywords
# PY_KEYWORDS = set(keyword.kwlist)

# taken straight from pyexpander/lib.py
# has round brackets at the end of the keywords

# cannot find certain keywords in documentation: "template", "subst", "pattern"
# "py", "template", "subst", "pattern", "default", "macro", "nonlocal", "extend", "extend_expr"
# CMD_KEYWORDS = {
#     "py", "default", "macro", "nonlocal", "extend", "extend_expr"
#     "if", "elif", "for", "for_begin", "while", "while_begin", "include", "include_begin",
#     }

# does not have round brackets at the end of the keywords
# PURE_CMD_KEYWORDS = {
#     "else", "endif", "endfor", "endwhile", "endmacro", "begin", "end"
#     }

class LineTypedToken(Enum):
    NORMAL = auto()
    MACRO_INDENT = auto()
    PY_INDENT = auto()
    KEYWORD_BEGIN_INDENT = auto()
    KEYWORD_END_INDENT = auto()

class LineToken:
    """
    line (str)
    line_type (LinedTypedToken)
    """
    def __init__(self, line, line_type):
        self.line = line
        self.line_type = line_type

class Lexer:
    pass


def parse_pre_expander(text):
    # 2 // -> 4 //// for entire text
    text.replace('\\\\', '\\\\\\\\')

if __name__ == "__main__":
    pass
    # print(PY_KEYWORDS)
    # print(CMD_KEYWORDS)
    # print(PURE_CMD_KEYWORDS)

    # 2 // -> 4 ////
    print('\\\\')
    print('\\\\\\\\')
