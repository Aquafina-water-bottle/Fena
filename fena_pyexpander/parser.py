"""
Implement the parser for pyexpander, whatever the parser is ffs
We use '\n' as line separator and rely on python's built in line end conversion to '\n' on all platforms.

Note that under ~/.pylintrc, the following exists under [MESSAGES CONTROL]:
disable=
    attribute-defined-outside-init,
    duplicate-code,
    fixme,
    invalid-name,
    missing-docstring,
    protected-access,
    too-few-public-methods,
    line-too-long,
    wrong-import-position,
    trailing-newlines
"""

import re
from bisect import bisect_right
from typing import List, Tuple
from collections import namedtuple

# mrw I have to import stuff from the fena library because it's actually too damn useful
if __name__ == "__main__":
    import sys
    sys.path.append("..")

from fenalib.assert_utils import assert_type
from fenalib.repr_utils import addrepr

# These are now CONSTANT like how global variables should be
LINESEP = "\n"
LINESEP_LEN = len(LINESEP)


RowColBase = namedtuple("RowColBase", ["row", "column"])
class RowCol(RowColBase):
    """
    NamedTuple to keep the functionality of indexing and immutablility
    while giving it a nice repr and str
    """
    def __str__(self):
        return f"row={self.row}, column={self.column}"


@addrepr
class IndexedString:
    """
    Gets the row column information from a string

    Attributes:
        string (str): The string that the row and column will be calculated from
        _positions (List[int]): List of positions of the line separator

    Examples:
        >>> txt='''01234
        ... 67
        ... 9abcd'''
        >>> l = IndexedString(txt)

        >>> l.rowcol(0)
        RowCol(row=1, column=1)
        >>> l.rowcol(1)
        RowCol(row=1, column=2)
        >>> l.rowcol(4)
        RowCol(row=1, column=5)
        >>> l.rowcol(5)
        RowCol(row=1, column=6)
        >>> l.rowcol(6)
        RowCol(row=2, column=1)
        >>> l.rowcol(7)
        RowCol(row=2, column=2)
        >>> l.rowcol(8)
        RowCol(row=2, column=3)
        >>> l.rowcol(9)
        RowCol(row=3, column=1)
        >>> l.rowcol(13)
        RowCol(row=3, column=5)
        >>> l.rowcol(14)
        RowCol(row=3, column=6)
        >>> l.rowcol(16)
        RowCol(row=3, column=8)

        >>> l._positions
        [0, 6, 9]
    """

    def __init__(self, string: str):
        self.string: str = string
        self._positions: List[int] = None

    def _get_positions(self):
        """
        Calculate and remember positions where lines begin.
        """
        pos_after_linesep = 0
        line_number = 1
        self._positions = [0]

        if LINESEP not in self.string:
            # no line seperator was found, so stops the function immediately
            return

        while True:
            # look for the standard line separator in the string (which is guaranteed to exist at least once)
            pos_of_linesep = self.string.find(LINESEP, pos_after_linesep)
            pos_after_linesep = pos_of_linesep + LINESEP_LEN

            # -1 if the str.find method cannot find anything
            if pos_of_linesep == -1:
                break

            line_number += 1
            self._positions.append(pos_after_linesep)

    def rowcol(self, pos: int) -> RowCol:
        """
        calculate (row, column) from a string position.
        """
        if self._positions is None:
            self._get_positions()

        # note that the index core
        index = bisect_right(self._positions, pos) - 1
        off = self._positions[index]

        row = index + 1
        column = pos - off + 1
        return RowCol(row, column)

    def __str__(self):
        if len(self.string) > 100:
            return f"IndexedString[string={self.string[:100]!r}...]"
        return f"IndexedString[string={self.string!r}]"


class ParseException(Exception):
    """
    The general Exception in this module.
    """

    def __init__(self, value: str, rowcol=None):
        super().__init__(value, rowcol)
        self.value = value
        self.rowcol = rowcol

    def __str__(self):
        if self.rowcol is not None:
            # return "%s line %d, col %d" % (self.value, self.rowcol[0], self.rowcol[1])
            return f"{self.value} at {self.rowcol}"

        return str(self.value)


# python identifier
rx_PY_IDENTIFIER = re.compile(r'([A-Za-z_][\w\.]*)$')

# comma separated value
# allows any whitespace between commas
rx_CSV = re.compile(r'\s*,\s*')

def scan_py_identifier_list(csv: str) -> List[str]:
    """
    Scan a list of python identifiers.

    Examples:
        >>> scan_py_identifier_list("a,b")
        ['a', 'b']

        >>> scan_py_identifier_list("a,b.d, c")
        ['a', 'b.d', 'c']

        >>> scan_py_identifier_list("a,b.d, c&")
        Traceback (most recent call last):
            ...
        ParseException: Invalid python identifier 'c&' in ['a', 'b.d', 'c&']
    """

    # all the values inside a CSV string
    identifiers = re.split(rx_CSV, csv)

    # checks for valid identifiers inside the CSV
    for identifier in identifiers:
        if rx_PY_IDENTIFIER.match(identifier) is None:
            raise ParseException(f"Invalid python identifier {identifier!r} in {identifiers}")

    return identifiers


# python in statement regex
rx_PY_IN_STMT = re.compile(r'^\s*(.*?)\s*\b(in)\b\s*(.*?)\s*$')

def scan_py_in_stmt(in_stmt: str) -> Tuple[str, str, str]:
    """
    Scan a python "in" statement to retrieve its component tokens

    Returns:
        tuple: LHS, 'in', RHS

    Examples:
        >>> scan_py_in_stmt(" (a,b) in k.items() ")
        ('(a,b)', 'in', 'k.items()')

        >>> scan_py_in_stmt(" a,b   in    k ")
        ('a,b', 'in', 'k')

        >>> scan_py_in_stmt("a in k")
        ('a', 'in', 'k')

        >>> scan_py_in_stmt("a ni k")
        Traceback (most recent call last):
            ...
        ParseException: Invalid python 'in' expression 'a ni k'

        >>> scan_py_in_stmt("a in")
        Traceback (most recent call last):
            ...
        ParseException: Invalid python 'in' expression 'a in' because of an empty group in ('a', 'in', '')

        >>> scan_py_in_stmt("in k")
        Traceback (most recent call last):
            ...
        ParseException: Invalid python 'in' expression 'in k' because of an empty group in ('', 'in', 'k')
    """
    match = rx_PY_IN_STMT.match(in_stmt)
    if match is None:
        raise ParseException(f"Invalid python 'in' expression {in_stmt!r}")

    # groups are separated by r'\b'
    # https://docs.python.org/3/library/re.html#re.match.group
    groups = match.groups()
    for group in groups:
        # detects an empty string
        if not group:
            raise ParseException(f"Invalid python 'in' expression {in_stmt!r} because of an empty group in {groups}")

    return groups


# r'\w' = r'[a-zA-Z0-9_]'
rx_CURLY_BRACKETS = re.compile(r'\{[A-Za-z_]\w*\}')

def parse_curly_brackets(indexed_str: IndexedString, pos: int) -> Tuple[int, int]:
    """
    Parse an identifier in curly brackets.

    Args:
        pos (int): Expected position of the curly bracket

    Returns:
        Tuple: position of the beginning and end of the curly brackets

    Examples:
        >>> def test(string, pos):
        ...     indexed_str = IndexedString(string)
        ...     (a, b) = parse_curly_brackets(indexed_str, pos)
        ...     return string[a:b]

        >>> test(r'{abc}', 0)
        '{abc}'

        >>> test(r'{ab8c}', 0)
        '{ab8c}'

        >>> test(r'{c}', 0)
        '{c}'

        >>> test(r'{}', 0)
        Traceback (most recent call last):
            ...
        ParseException: Expected an identifier enclosed in curly brackets at row=1, column=1

        >>> test(r'{abc', 0)
        Traceback (most recent call last):
            ...
        ParseException: Expected an identifier enclosed in curly brackets at row=1, column=1

        >>> test(r'x{ab8c}', 1)
        '{ab8c}'
    """
    assert_type(indexed_str, IndexedString)
    match = rx_CURLY_BRACKETS.match(indexed_str.string, pos)

    if match is None:
        raise ParseException("Expected an identifier enclosed in curly brackets", rowcol=indexed_str.rowcol(pos))

    return (pos, match.end())


STRING_QUOTES = r'|'.join((r'"""', r"'''", r'"', r"'"))
STRING_BEGINS = r'u|r|f|rf|fr|'  # allows no beginning
rx_STRING_LITERAL_START = re.compile(f'({STRING_BEGINS})({STRING_QUOTES})')

def parse_string_literal(indexed_str: IndexedString, pos: int) -> Tuple[int, int]:
    r"""
    Parse a python string literal.

    Returns:
        Tuple: position of the beginning and end of the quotes
            - note that the ending position is the index of the first character AFTER the string

    Examples:
        >>> def test(st, pos):
        ...     indexed_str = IndexedString(st)
        ...     (a, b) = parse_string_literal(indexed_str, pos)
        ...     print(st[a:b])

        >>> test(r'"abc"', 0)
        "abc"

        >>> test("'''ab'c'd'''", 0)
        '''ab'c'd'''

        >>> test("'''ab'cd''''", 0)
        '''ab'cd'''

        >>> test(r'u"abc"', 0)
        u"abc"

        Note that 'x' is an ignored character due to the position
        >>> test(r'xu"abc"', 1)
        u"abc"

        >>> test(r'xr"abc"', 1)
        r"abc"

        >>> test(r'xr"ab\\"c"', 1)
        r"ab\\"

        >>> test(r'xf"ab\"c"', 1)
        f"ab\"c"

        Invalid starting 'x'
        >>> test(r'xf"ab\"c"', 0)
        Traceback (most recent call last):
            ...
        ParseException: Expected start of string at row=1, column=1

        Invalid endings
        >>> test(r'"ab', 0)
        Traceback (most recent call last):
            ...
        ParseException: End of string not found at row=1, column=1

        >>> test(r"'''ab'", 0)
        Traceback (most recent call last):
            ...
        ParseException: End of string not found at row=1, column=1

        >>> test(r'"ab\"', 0)
        Traceback (most recent call last):
            ...
        ParseException: End of string not found at row=1, column=1
    """
    assert_type(indexed_str, IndexedString)
    string = indexed_str.string
    match = rx_STRING_LITERAL_START.match(string, pos)

    if match is None:
        raise ParseException("Expected start of string", rowcol=indexed_str.rowcol(pos))

    # note that for groups, group(1) gets the first element since group(0) gets the full match
    prefix = match.group(1)
    starter = match.group(2) # """ or ''' or " or '
    calc_start_pos = pos + len(prefix) + len(starter)
    # print(f"indexed_str={indexed_str}, calc_start_pos={calc_start_pos}, regex={rx_STRING_LITERAL_START}")
    # print(f"prefix={prefix!r}, starter={starter!r}, groups={match.groups()}")

    # looks for the end of a string
    while True:
        ending_quote_pos = string.find(starter, calc_start_pos)
        # if calc_start_pos>len(string), ending_quote_pos is also -1
        if ending_quote_pos == -1:
            raise ParseException("End of string not found", rowcol=indexed_str.rowcol(pos))

        if string[ending_quote_pos-1] == "\\":

            # maybe escaped quote char
            # uses try/except because of the ask forgiveness instead of permission python style
            # https://stackoverflow.com/questions/12265451/ask-forgiveness-not-permission-explain
            try:
                # makes sure that the character before the '\' is not another '\'
                # only then it is an escaped quote char
                if string[ending_quote_pos-2] != "\\":
                    calc_start_pos = ending_quote_pos + 1
                    continue
            except IndexError:
                # traceback usage: https://docs.python.org/3/library/exceptions.html#BaseException
                # removes the "During handling of the above exception, another exception occurred:" message
                tb = sys.exc_info()[2]
                raise ParseException("End of string not found", rowcol=indexed_str.rowcol(pos)).with_traceback(tb)
        break

    if len(starter) == 1:
        # simple single quoted string
        return (pos, ending_quote_pos+1)
    elif len(starter) == 3:
        # triple quoted string
        return (pos, ending_quote_pos+3)
    else:
        raise ParseException("Unknown default case")


def parse_comment(indexed_str: IndexedString, pos: int) -> Tuple[int, int]:
    r"""
    Parses a python comment

    Returns:
        Tuple: position of the beginning and end of the quotes
            - note that the ending position is the index of the newline after the comment

    Examples:
        >>> import os
        >>> def test(st, pos):
        ...     indexed_str = IndexedString(st)
        ...     (a, b) = parse_comment(indexed_str, pos)
        ...     print(repr(st[a:b]))

        >>> test("#abc", 0)
        '#abc'

        >>> test("#abc\nef", 0)
        '#abc\n'

        >>> test("#abc\r\nef", 0)
        '#abc\r\n'

        >>> test("xy#abc", 2)
        '#abc'

        >>> test("xy#abc\nef", 2)
        '#abc\n'

        >>> test("xy#abc\nef", 3)
        Traceback (most recent call last):
            ...
        ParseException: Expected the start of a comment at row=1, column=4
    """
    assert_type(indexed_str, IndexedString)
    string = indexed_str.string

    if string[pos] != "#":
        raise ParseException("Expected the start of a comment", rowcol=indexed_str.rowcol(pos))

    pos_of_linesep = string.find(LINESEP, pos + 1)

    # no line separator meaning the rest of the line is just one comment
    if pos_of_linesep == -1:
        return (pos, len(string))

    return (pos, pos_of_linesep + LINESEP_LEN)


# ?: in regex is a non-capturing group
# rx_CodePart = re.compile(r'''((?:UR|Ur|uR|ur|r|u|R|U|)(?:"""|''' + """'''""" + r'''|'|")|#|\(|\))''')
rx_CODE_PART = re.compile(rf'((?:{STRING_BEGINS})(?:{STRING_QUOTES})|#|\(|\))')

def parse_code(indexed_str: IndexedString, pos: int) -> Tuple[int, int]:
    r"""
    Parse python code, it MUST start with a '('.

    Here are some examples:

    >>> def test(st, pos):
    ...     indexed_str = IndexedString(st)
    ...     (a, b) = parse_code(indexed_str, pos)
    ...     print(st[a:b])

    >>> test(r'a+b)', 0)
    Traceback (most recent call last):
        ...
    ParseException: Expected the start of a round bracket expression at row=1, column=1

    >>> test(r'(a+b)', 0)
    (a+b)

    >>> test(r'(a+(b*c))', 0)
    (a+(b*c))

    >>> test(r'(a+(b*c)+")")', 0)
    (a+(b*c)+")")

    >>> test(r"(a+(b*c)+''')''')", 0)
    (a+(b*c)+''')''')

    >>> test(r"(a+(b*c)+''')'''+# comment )\n)", 0)
    Traceback (most recent call last):
        ...
    ParseException: Expected the end of a round bracket expression at row=1, column=1

    Note that the following is correct since after the comment, there's a bracket
    >>> test("(a+(b*c)+''')'''+# comment )\n)", 0)
    (a+(b*c)+''')'''+# comment )
    )
    """
    assert_type(indexed_str, IndexedString)
    string = indexed_str.string

    if string[pos] != "(":
        raise ParseException("Expected the start of a round bracket expression", rowcol=indexed_str.rowcol(pos))
    calc_start_pos = pos + 1

    while True:
        match = rx_CODE_PART.search(string, calc_start_pos)

        if match is None:
            raise ParseException("Expected the end of a round bracket expression", rowcol=indexed_str.rowcol(pos))
        matched_begin_value = match.group(1)

        if matched_begin_value == "#":
            # a comment
            calc_start_pos = parse_comment(indexed_str, match.start())[1]
            continue

        if matched_begin_value == "(":
            # an inner bracket
            calc_start_pos = parse_code(indexed_str, match.start())[1]
            continue

        if matched_begin_value == ")":
            return (pos, match.start() + 1)

        # from here it must be a string literal
        calc_start_pos = parse_string_literal(indexed_str, match.start())[1]
        continue

@addrepr
class ParsedItem:
    """
    Base class of parsed items
    """
    def __init__(self, indexed_str: IndexedString, start: int, end: int):
        assert_type(indexed_str, IndexedString)
        self.indexed_str = indexed_str
        self.start = start
        self.end = end

    @property
    def string(self) -> str:
        """
        Gets the string that represents the ParsedItem.
        """
        return self.indexed_str.string[self.start:self.end+1]

    def rowcol(self, pos=None) -> RowCol:
        """
        Calculates (row, column) from a string position.
        """
        if pos is None:
            pos = self.start()
        return indexed_str.rowcol(pos)

class ParsedLiteral(ParsedItem):
    """class of a parsed literal.

    A literal is a substring in the input that shouldn't be modified by
    pyexpander.
    """
    def __init__(self, indexed_str, start, end):
        ParsedItem.__init__(self, indexed_str, start, end)

class ParsedComment(ParsedItem):
    """class of a parsed comment.

    A comment in pyexpander starts with '$#'.
    """
    def __init__(self, indexed_str, start, end):
        ParsedItem.__init__(self, indexed_str, start, end)

class ParsedVar(ParsedItem):
    """class of a parsed variable.

    A variable in pyexpander has the form "$(identifier)".
    """
    def __init__(self, indexed_str, start, end):
        ParsedItem.__init__(self, indexed_str, start, end)

class ParsedEval(ParsedItem):
    """class of an pyexpander expression.

    A pyexpander expression has the form "$(expression)" e.g. "$(a+1)". This is
    different from ParsedVar where the string within the brackets is a simple
    identifier.
    """
    def __init__(self, indexed_str, start, end):
        ParsedItem.__init__(self, indexed_str, start, end)

class ParsedPureCommand(ParsedItem):
    """class of a pyexpander command without arguments.

    A pure command has the form "$name". Such a command has no arguments which
    would be enclosed in round brackets immediately following the name.
    """
    def __init__(self, indexed_str, start, end):
        ParsedItem.__init__(self, indexed_str, start, end)

class ParsedCommand(ParsedItem):
    """class of a pyexpander command with arguments.

    A command has the form "$name(argument1, argument2, ...)".
    """
    def __init__(self, indexed_str, start, end, ident):
        ParsedItem.__init__(self, indexed_str, start, end)
        self.ident= ident
    def args(self):
        """return the arguments of the command."""
        return self.string()
    def __str__(self):
        return "('%s', %s, %s, %s)" % (self.__class__.__name__, \
               self.positions(), repr(self.string()), \
               repr(self.ident))
    def __repr__(self):
        return "%s(%s, %s, %s, %s)" % (self.__class__.__name__, \
                repr(self._idxst), repr(self._start), repr(self._end), \
                repr(self.ident))


rx_DollarFollows= re.compile(r'([A-Za-z_]\w*|\(|\{|#)')

def parseDollar(indexed_str, pos):
    r"""parse things that follow a dollar.

    Here are some examples:

    >>> def test(st, pos):
    ...   indexed_str= IndexedString(st)
    ...   (p, elm)= parseDollar(indexed_str, pos)
    ...   print("Parsed: %s" % elm)
    ...   print("rest of string:%s" % st[p:])
    ...
    >>> test("$abc", 0)
    Parsed: ('ParsedPureCommand', (1, 3), 'abc')
    rest of string:
    >>> test("$abc%&/", 0)
    Parsed: ('ParsedPureCommand', (1, 3), 'abc')
    rest of string:%&/
    >>> test("$abc(2*3)", 0)
    Parsed: ('ParsedCommand', (5, 7), '2*3', 'abc')
    rest of string:
    >>> test(" $abc(2*sin(x))", 1)
    Parsed: ('ParsedCommand', (6, 13), '2*sin(x)', 'abc')
    rest of string:
    >>> test(" $abc(2*sin(x))bn", 1)
    Parsed: ('ParsedCommand', (6, 13), '2*sin(x)', 'abc')
    rest of string:bn
    >>> test(" $# a comment\nnew line", 1)
    Parsed: ('ParsedComment', (3, 13), ' a comment\n')
    rest of string:new line
    >>> test("$(abc)", 0)
    Parsed: ('ParsedVar', (2, 4), 'abc')
    rest of string:
    >>> test("$(abc*2)", 0)
    Parsed: ('ParsedEval', (2, 6), 'abc*2')
    rest of string:
    >>> test(" $(2*x(y))abc", 1)
    Parsed: ('ParsedEval', (3, 8), '2*x(y)')
    rest of string:abc
    """
    if not isinstance(indexed_str, IndexedString):
        raise TypeError("indexed_str par wrong: %s" % repr(indexed_str))
    st= indexed_str.st()
    if st[pos]!="$":
        raise ParseException("'$' expected at", rowcol=indexed_str.rowcol(pos))
    m= rx_DollarFollows.match(st, pos+1)
    if m is None:
        raise ParseException("unexpected characters after '$' at", rowcol=indexed_str.rowcol(pos))
    matched= m.group(1)
    if matched=="#":
        # an expander comment
        (a, b)= parse_comment(indexed_str, pos+1)
        elm= ParsedComment(indexed_str, a+1, b-1)
        return (b, elm)
    if matched=="(":
        # pylint: disable= redefined-variable-type
        (a, b)= parse_code(indexed_str, pos+1)
        m_ident= rx_pyIdent.match(st, a+1, b-1)
        if m_ident is not None:
            elm= ParsedVar(indexed_str, a+1, b-2)
        else:
            elm= ParsedEval(indexed_str, a+1, b-2)
        return (b, elm)
    if matched=="{":
        # a purecommand enclosed in "{}" brackets
        (a, b)= parse_curly_brackets(indexed_str, pos+1)
        elm= ParsedPureCommand(indexed_str, a+1, b-2)
        return (b, elm)
    # from here: a purecommand or a command
    try:
        nextchar= st[m.end()]
    except IndexError as _:
        nextchar= None
    if nextchar=="(":
        (a, b)= parse_code(indexed_str, m.end())
        elm= ParsedCommand(indexed_str, a+1, b-2, matched)
        return (b, elm)
    elm= ParsedPureCommand(indexed_str, pos+1, m.end()-1)
    return (m.end(), elm)

def parseBackslash(indexed_str, pos):
    r"""parses a backslash.

    >>> import os
    >>> def test(st, pos):
    ...     indexed_str= IndexedString(st)
    ...     (p, elm)= parseBackslash(indexed_str, pos)
    ...     print("Parsed: %s" % elm)
    ...     print("rest of string:%s" % repr(st[p:]))
    
    >>> test(r"\abc", 0)
    Parsed: ('ParsedLiteral', (0, 0), '\\')
    rest of string:'abc'
    >>> test("\\", 0)
    Parsed: ('ParsedLiteral', (0, 0), '\\')
    rest of string:''
    >>> test("\\\rab", 0)
    Parsed: None
    rest of string:'ab'
    >>> test("\\\rab", 0)
    Parsed: ('ParsedLiteral', (0, 0), '\\')
    rest of string:'\rab'
    >>> test("\\\rab", 0)
    Parsed: ('ParsedLiteral', (0, 0), '\\')
    rest of string:'\rab'
    >>> test("\\\nab", 0)
    Parsed: ('ParsedLiteral', (0, 0), '\\')
    rest of string:'\nab'
    >>> test("\\\nab", 0)
    Parsed: None
    rest of string:'ab'
    >>> test("\\\nab", 0)
    Parsed: ('ParsedLiteral', (0, 0), '\\')
    rest of string:'\nab'
    >>> test("\\\r\nab", 0)
    Parsed: None
    rest of string:'\nab'
    >>> test("\\\r\nab", 0)
    Parsed: ('ParsedLiteral', (0, 0), '\\')
    rest of string:'\r\nab'
    >>> test("\\\r\nab", 0)
    Parsed: None
    rest of string:'ab'
    """
    # backslash found
    if not isinstance(indexed_str, IndexedString):
        raise TypeError("indexed_str par wrong: %s" % repr(indexed_str))
    st= indexed_str.st()
    if st[pos]!="\\":
        raise ParseException("backslash expected at", rowcol=indexed_str.rowcol(pos))
    l_= len(st)
    if pos+1>=l_:
        # no more characters
        elm= ParsedLiteral(indexed_str, pos, pos)
        return (pos+1, elm)
    else:
        # at least one more character
        nextchar= st[pos+1]
        if nextchar=="\\":
            elm= ParsedLiteral(indexed_str, pos, pos)
            return (pos+2, elm)
        if nextchar=="$":
            elm= ParsedLiteral(indexed_str, pos+1, pos+1)
            return (pos+2, elm)
        if pos+LINESEP_LEN>=l_:
            # not enough characters for LINESEP
            elm= ParsedLiteral(indexed_str, pos, pos)
            return (pos+1, elm)
        else:
            for i in range(LINESEP_LEN):
                if st[pos+1+i]!=LINESEP[i]:
                    # no line separator follows
                    elm= ParsedLiteral(indexed_str, pos, pos)
                    return (pos+1, elm)
            return(pos+LINESEP_LEN+1, None)

rx_top= re.compile(r'(\$|\\)')
def parseAll(indexed_str, pos):
    r"""parse everything.

    >>> def test(st, pos):
    ...     indexed_str= IndexedString(st)
    ...     pprint(parseAll(indexed_str, pos))
    ...

    >>> test("abc", 0)
    ('ParsedLiteral', (0, 2), 'abc')
    >>> test("abc$xyz", 0)
    ('ParsedLiteral', (0, 2), 'abc')
    ('ParsedPureCommand', (4, 6), 'xyz')
    >>> test("abc${xyz}efg", 0)
    ('ParsedLiteral', (0, 2), 'abc')
    ('ParsedPureCommand', (5, 7), 'xyz')
    ('ParsedLiteral', (9, 11), 'efg')
    >>> test("abc$xyz(2*4)", 0)
    ('ParsedLiteral', (0, 2), 'abc')
    ('ParsedCommand', (8, 10), '2*4', 'xyz')
    >>> test("abc$(2*4)ab", 0)
    ('ParsedLiteral', (0, 2), 'abc')
    ('ParsedEval', (5, 7), '2*4')
    ('ParsedLiteral', (9, 10), 'ab')
    >>> test("abc\\$(2*4)ab", 0)
    ('ParsedLiteral', (0, 2), 'abc')
    ('ParsedLiteral', (4, 4), '$')
    ('ParsedLiteral', (5, 11), '(2*4)ab')
    >>> test("ab$func(1+2)\\\nnew line", 0)
    ('ParsedLiteral', (0, 1), 'ab')
    ('ParsedCommand', (8, 10), '1+2', 'func')
    ('ParsedLiteral', (14, 21), 'new line')
    >>> test("ab$func(1+2)\nnew line", 0)
    ('ParsedLiteral', (0, 1), 'ab')
    ('ParsedCommand', (8, 10), '1+2', 'func')
    ('ParsedLiteral', (12, 20), '\nnew line')
    >>> test("ab$(xyz)(56)", 0)
    ('ParsedLiteral', (0, 1), 'ab')
    ('ParsedVar', (4, 6), 'xyz')
    ('ParsedLiteral', (8, 11), '(56)')

    >>> test(r'''
    ... Some text with a macro: $(xy)
    ... an escaped dollar: \$(xy)
    ... a macro within letters: abc${xy}def
    ... a pyexpander command structure:
    ... $if(a=1)
    ... here
    ... $else
    ... there
    ... $endif
    ... now a continued\
    ... line
    ... from here:$# the rest is a comment
    ... now an escaped continued\\
    ... line
    ... ''', 0)
    ('ParsedLiteral', (0, 24), '\nSome text with a macro: ')
    ('ParsedVar', (27, 28), 'xy')
    ('ParsedLiteral', (30, 49), '\nan escaped dollar: ')
    ('ParsedLiteral', (51, 51), '$')
    ('ParsedLiteral', (52, 83), '(xy)\na macro within letters: abc')
    ('ParsedPureCommand', (86, 87), 'xy')
    ('ParsedLiteral', (89, 124), 'def\na pyexpander command structure:\n')
    ('ParsedCommand', (129, 131), 'a=1', 'if')
    ('ParsedLiteral', (133, 138), '\nhere\n')
    ('ParsedPureCommand', (140, 143), 'else')
    ('ParsedLiteral', (144, 150), '\nthere\n')
    ('ParsedPureCommand', (152, 156), 'endif')
    ('ParsedLiteral', (157, 172), '\nnow a continued')
    ('ParsedLiteral', (175, 189), 'line\nfrom here:')
    ('ParsedComment', (192, 214), ' the rest is a comment\n')
    ('ParsedLiteral', (215, 238), 'now an escaped continued')
    ('ParsedLiteral', (239, 239), '\\')
    ('ParsedLiteral', (241, 246), '\nline\n')
    """
    if not isinstance(indexed_str, IndexedString):
        raise TypeError("indexed_str par wrong: %s" % repr(indexed_str))
    st= indexed_str.st()
    parselist=[]
    l= len(st)
    while True:
        if pos>=l:
            return parselist
        m= rx_top.search(st, pos)
        if m is None:
            parselist.append(ParsedLiteral(indexed_str, pos, len(st)-1))
            return parselist
        if m.start()>pos:
            parselist.append(ParsedLiteral(indexed_str, pos, m.start()-1))
        if m.group(1)=="\\":
            (p, elm)= parseBackslash(indexed_str, m.start())
            if elm is not None:
                parselist.append(elm)
            pos= p
            continue
        # from here it must be a dollar sign
        (pos, elm)= parseDollar(indexed_str, m.start())
        parselist.append(elm)
        continue

def pprint(parselist):
    """pretty print a parselist."""
    for elm in parselist:
        print(str(elm))

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    def test(st, pos):
        indexed_str = IndexedString(st)
        (a, b) = parse_code(indexed_str, pos)
        return st[a:b]

    result = test("(a+(b*c)+''')'''+# comment )\n)", 0)
    print(repr(result))

