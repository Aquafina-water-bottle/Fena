import re
import os
from typing import NamedTuple, Optional

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

from fenalib.assert_utils import assert_type
from fenalib.str_utils import decode_str

r"""
Runs a quick script before pyexpander is run
Features:
    - replaces all \\ with \\\\
    - changes some syntax of pyexpander code to make it more elegant to work with for fena code
    - removes all empty lines and comments (although a trailing newline is added)

Syntax changes:

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
!mfunc give_porkchop_$(x)
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
"""

KEYWORD_SURROUND = {
    "if": "$endif",
    "for": "$endfor",
    "while": "$endwhile",
    "for_begin": "$endfor",
    "while_begin": "$endwhile",
    "macro": "$endmacro",
}

LINESEP = "\n"

INDENT = "    "

class PrePyexpanderError(Exception):
    pass

class InvalidFileError(PrePyexpanderError):
    pass

class InvalidIndentError(PrePyexpanderError):
    pass

class Line(NamedTuple):
    """
    Attributes:
        string (str): A fully unindented string as the line
        indents (int): The number of indents that the string had
        line_number (int): The line number in the original file
        pyexp_keyword (Optional[str]): The pyexpander keyword if it has the proper syntax for pre-expander parsing
            - line starts with '$' and ends with ':'
        empty (bool): Whether the line should be considered for parsing indents or not
    """
    string: str
    line_number: int
    indents: int
    pyexp_keyword: Optional[str]
    empty: bool


def get_line_strings(text):
    """
    Generates all lines from a text (without the newline)
    """
    begin_index = 0
    for index, char in enumerate(text):
        if char == LINESEP:
            yield text[begin_index:index]
            begin_index = index + 1

rx_INDENT_WHITESPACE = re.compile(r'^\s*')  # gets left most whitespace
rx_PYEXP_KEYWORD = re.compile(r'[a-zA-Z]+')  # pyexpander keyword
def get_lines(text):
    """
    Generates Line objects from the text
    """
    for line_number, line_str in enumerate(get_line_strings(text)):

        # if it's a comment or empty line, the line is considered to be empty
        empty = (line_str.lstrip().startswith("#") or not line_str.strip())

        if empty:
            yield Line(line_str, line_number, indents=0, pyexp_keyword=None, empty=True)
            continue

        # checks for proper indentation as 4 spaces
        match = re.match(rx_INDENT_WHITESPACE, line_str)
        indent_str = "" if match is None else match.group()
        if "\t" in indent_str:
            raise InvalidIndentError(f"Line {line_number} with indentation of {indent_str!r} contains a tab space in line {line_str!r}")
        if indent_str.count(" ") % len(INDENT) != 0:
            raise InvalidIndentError(f"Line {line_number} with indentation of {indent_str!r} requires indentation with 4 spaces in line {line_str!r}")

        indents = indent_str.count(INDENT)
        unindented_str = line_str.lstrip()

        # checks if it contains a pyexpander keyword that should be parsed by indentation
        if unindented_str.startswith("$") and unindented_str.endswith(":"):
            # gets python keyword
            keyword = rx_PYEXP_KEYWORD.match(unindented_str, 1)
            if keyword is None:
                raise PrePyexpanderError(f"Line {line_number}: Expected a pyexpander keyword in line {line_str!r}")
            yield Line(unindented_str, line_number, indents, pyexp_keyword=keyword.group(), empty=False)
        elif unindented_str.startswith("$include(") and unindented_str.endswith(")"):
            file_path = unindented_str[len("$include("):-len(")")]
            yield Line(file_path, line_number, indents, pyexp_keyword="include", empty=False)
        else:
            yield Line(unindented_str, line_number, indents, pyexp_keyword=None, empty=False)


def finalize_line(line, dedents=0):
    """
    Indents the line given line indents minus the dedents, and removes the ending ":" if it exists
    """
    assert_type(line, Line)
    assert_type(dedents, int)
    total_indents = line.indents - dedents

    if total_indents < 0:
        raise InvalidIndentError(f"Invalid indentation for line {line} with dedents={dedents}")

    if line.pyexp_keyword is not None:
        line_str = line.string[:-1]
    else:
        line_str = line.string

    return indent_line(line_str, total_indents)

def indent_line(line_str, indents):
    """
    Indents the line given indents
    """
    assert_type(line_str, str)
    assert_type(indents, int)
    return (INDENT * indents) + line_str


class Parser:
    """
    Attributes:
        reached_eof (bool): True when the final line has been reached
        current_line (str or None): The current line from the iterator (None at the end)
        iterator (generator)
    """
    def __init__(self, text):
        self.reached_eof = False
        self.current_line = None
        self.iterator = get_lines(text)
        self.advance()

    def advance(self):
        previous_line = self.current_line
        self.current_line = next(self.iterator, None)

        if self.current_line is None:
            if self.reached_eof:
                raise PrePyexpanderError("Cannot advance past the last line")
            self.reached_eof = True

        return previous_line

    def parse_lines(self, required_indents=0, dedents=0):
        """
        Generates the properly parsed lines from the text
        Note that this is recursive

        Base case is when the line indent is less than the given indent
        """
        while not self.reached_eof:
            if self.current_line.empty:
                # yield self.advance().string
                self.advance()
                continue

            if self.current_line.indents < required_indents:
                # ends once the line has less indents
                return

            elif self.current_line.pyexp_keyword == "py":
                original_indents = self.current_line.indents
                yield finalize_line(self.advance(), dedents=original_indents) + "("
                yield from self.parse_lines(original_indents+1, original_indents+1)
                yield ")"

            elif self.current_line.pyexp_keyword == "macro":
                original_indents = self.current_line.indents
                yield finalize_line(self.advance(), dedents=original_indents)
                yield from self.parse_lines(original_indents+1, original_indents+1)
                yield KEYWORD_SURROUND["macro"]

            elif self.current_line.pyexp_keyword in ("for", "for_begin", "while", "while_begin"):
                original_indents = self.current_line.indents
                keyword = self.current_line.pyexp_keyword # redefine since 'self.current_line' will change
                yield finalize_line(self.advance(), dedents=dedents)
                yield from self.parse_lines(original_indents+1, dedents+1)
                yield indent_line(KEYWORD_SURROUND[keyword], original_indents-dedents)

            elif self.current_line.pyexp_keyword == "if":
                original_indents = self.current_line.indents
                yield finalize_line(self.advance(), dedents=dedents)
                yield from self.parse_lines(original_indents+1, dedents+1)

                while self.current_line.pyexp_keyword == "elif":
                    yield finalize_line(self.advance(), dedents=dedents)
                    yield from self.parse_lines(original_indents+1, dedents+1)

                if self.current_line.pyexp_keyword == "else":
                    yield finalize_line(self.advance(), dedents=dedents)
                    yield from self.parse_lines(original_indents+1, dedents+1)

                yield indent_line(KEYWORD_SURROUND["if"], original_indents-dedents)

            elif self.current_line.pyexp_keyword == "elif":
                raise PrePyexpanderError(f"Unexpected 'elif' (without accompanying 'if') in self.current_line {self.current_line}")

            elif self.current_line.pyexp_keyword == "else":
                raise PrePyexpanderError(f"Unexpected 'else' (without accompanying 'if') in self.current_line {self.current_line}")

            elif self.current_line.pyexp_keyword == "include":
                # override's pyexpander's "include" keyword
                file_path = decode_str(self.current_line.string)
                if not os.path.isfile(file_path):
                    raise InvalidFileError(f"{file_path!r} is not a valid file path")

                with open(file_path) as file:
                    parser = Parser(file.read())
                    yield from parser.parse_lines()
                    self.advance()

            elif self.current_line.pyexp_keyword is not None:
                raise PrePyexpanderError(f"Unexpected pyexpander keyword in self.current_line {self.current_line}")

            else:
                yield finalize_line(self.advance(), dedents=dedents)


def parse_pre_pyexpander(text):
    """
    Returns:
        Properly parsed text to be used by pyexpanxer
    """
    parser = Parser(text)
    # return list(parser.parse_lines())
    text = "\n".join(parser.parse_lines()) + "\n"

    # 2 // -> 4 //// for entire text
    # replaces after the parsing to make sure the $include() files are included
    text = text.replace('\\\\', '\\\\\\\\')
    return text

