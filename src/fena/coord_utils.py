import re

from token_types import TokenType

_alpha = re.compile("[A-Za-z_]")

def is_number(string):
    """
    Checks whether the string has a proper number format for minecraft

    Args:
        string

    Returns:
        bool

    Examples:
        >>> is_number("25.6")
        True
        >>> is_number("-1964")
        True

        >>> is_number("6e5")
        False
        >>> is_number("1_964")
        False
        >>> is_number("NaN")
        False
        >>> is_number("None")
        False
        >>> is_number("27j+5")
        False
        >>> is_number("abcdefg")
        False
        >>> is_number("12345abcdefg")
        False
        >>> is_number("~26.3")
        False
        >>> is_number("^26.3")
        False
    """

    try:
        float(string)
    except ValueError:
        return False

    # checks whether there is an alphabetical value is inside the number
    if re.search(_alpha, string) is not None:
        return False
    return True
    

def is_coord(string):
    """
    Checks whether a string is a valid coordinate type

    Args:
        string (str)

    Returns:
        bool: Whether the token value can be a coordinate
    """
    return string and (string[0] in "~^" and is_number(string[1:])) or is_number(string)

def is_coord_token(token):
    """
    Checks whether a singular token is a coordinate

    Args:
        token (Token)

    Returns:
        bool: Whether the token value can be a coordinate
    """
    return is_coord(token.value)

def get_coord_type(coord):
    """
    This assumes the given coordinate is indeed a coord type

    Args:
        coord (str)

    Returns:
        str ("relative", "local", "absolute"): The coordinate type
    """
    coord_dict = {"^": "local", "~": "relative"}
    return coord_dict.get(coord[0], "absolute")

def get_token_coord_type(token):
    return get_coord_type(token.value)

def are_coords(*tokens):
    """
    Checks whether a group of tokens:
        - Have a length of 2 or 3 tokens
        - Have the same type (local, or world (absolute and relative) coordinates)
    """
    # records the supposed global coord type as either "relative" or "local", as to skip absolute

    overall_coord_type = None
    if not (2 <= len(tokens) <= 3):
        return False

    for token in tokens:
        if not is_coord_token(token) or not token.matches(TokenType.COORD):
            return False

        coord_type = get_token_coord_type(token)
        if coord_type in ("relative", "absolute"):
            coord_type = "world"

        if overall_coord_type is None:
            overall_coord_type = coord_type
        elif overall_coord_type != coord_type:
            return False

    return True

if __name__ == "__main__":
    def test(string, *functions):
        print("string={}".format(repr(string)), *(("{}={}".format(function.__name__, repr(function(string)))) for function in functions), sep=", ")

    def test_number(string):
        return test(string, is_number, is_coord)

    def test_coord_type(string):
        return test(string, get_coord_type)

    test_number("25.6")
    test_number("6e5")
    test_number("-1964")
    test_number("1_964")
    test_number("NaN")
    test_number("None")
    test_number("27j+5")
    test_number("abcdefg")
    test_number("12345abcdefg")
    test_number("~26.3")
    test_number("^26.3")

    print()
    test_coord_type("25.6")
    test_coord_type("-1964")
    test_coord_type("~26.3")
    test_coord_type("^26.3")

    print()
    from token_position import TokenPosition
    from lexical_token import Token
    from token_types import TokenType
    position = TokenPosition(row=1, column=5, char_pos=3)
    coord1 = Token(position, TokenType.COORD, value="25.6")
    coord2 = Token(position, TokenType.COORD, value="^25.6")
    coord3 = Token(position, TokenType.COORD, value="~25.6")

    print(are_coords(coord1, coord1, coord1)) # true
    print(are_coords(coord2, coord2, coord2)) # true
    print(are_coords(coord3, coord3, coord3)) # true
    print(are_coords(coord1, coord3, coord3)) # true because relative and world
    print(are_coords(coord2, coord1, coord2)) # false because all must be local
    print(are_coords(coord2, coord1, coord3)) # false because all different
    print(are_coords(coord2, coord2, coord3)) # false because all must be local