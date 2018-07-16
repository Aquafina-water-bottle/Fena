import re

_alpha = re.compile("[A-Za-z_]")
_json_number = re.compile(r"-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?")
_nbt_float = re.compile(r"-?(0|[1-9]\d*)(\.\d+)([eE][+-]?\d+)?")

def is_json_number(string):
    """
    json_number ::= ("-")? && INT && ("." && INT)? && (["e", "E"] && ["+", "-"] && INT)?
    Follwing the picture for a general json number:
        http://www.json.org/number.gif
    """
    return bool(re.fullmatch(_json_number, string))

def is_number(string):
    """
    Checks whether the string has a proper signed number format for minecraft

    Args:
        string

    Returns:
        bool

    Examples:
        >>> is_number("25.6")
        True
        >>> is_number("-25.6")
        True
        >>> is_number("0")
        True
        >>> is_number("1964")
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

def is_signed_int(num_str):
    """
    Args:
        num_str (str): The string that is checked to see if it represents a number

    Returns:
        bool

    Examples:
        >>> is_signed_int("25.6")
        False
        >>> is_signed_int("-25.6")
        False
        >>> is_signed_int("0")
        True
        >>> is_signed_int("1964")
        True
        >>> is_signed_int("-1964")
        True

        >>> is_signed_int("6e5")
        False
        >>> is_signed_int("1_964")
        False
        >>> is_signed_int("NaN")
        False
        >>> is_signed_int("None")
        False
        >>> is_signed_int("27j+5")
        False
        >>> is_signed_int("abcdefg")
        False
        >>> is_signed_int("12345abcdefg")
        False
        >>> is_signed_int("~26.3")
        False
        >>> is_signed_int("^26.3")
        False
    """
    # if the num_str is a digit, that means that there are no special characters within the num_str
    # therefore making it a nonneg int
    # to check if it is a signed integer, the string is checked for one "-" and then the rest being the format of a nonneg int

    assert isinstance(num_str, str)
    return num_str.isdigit() or (num_str.startswith("-") and num_str[1:].isdigit())

def is_nonneg_int(num_str):
    """
    Args:
        num_str (str): The string that is checked to see if it represents a nonneg integer

    Returns:
        bool

    Examples:
        >>> is_nonneg_int("25.6")
        False
        >>> is_nonneg_int("-25.6")
        False
        >>> is_nonneg_int("0")
        True
        >>> is_nonneg_int("1964")
        True
        >>> is_nonneg_int("-1964")
        False

        >>> is_nonneg_int("6e5")
        False
        >>> is_nonneg_int("1_964")
        False
        >>> is_nonneg_int("NaN")
        False
        >>> is_nonneg_int("None")
        False
        >>> is_nonneg_int("27j+5")
        False
        >>> is_nonneg_int("abcdefg")
        False
        >>> is_nonneg_int("12345abcdefg")
        False
        >>> is_nonneg_int("~26.3")
        False
        >>> is_nonneg_int("^26.3")
        False
    """

    assert isinstance(num_str, str)
    return num_str.isdigit()

def is_pos_int(num_str):
    """
    Args:
        num_str (str): The string that is checked to see if it represents a positive integer (not 0)

    Returns:
        bool

    Examples:
        >>> is_pos_int("25.6")
        False
        >>> is_pos_int("-25.6")
        False
        >>> is_pos_int("0")
        False
        >>> is_pos_int("1964")
        True
        >>> is_pos_int("-1964")
        False

        >>> is_pos_int("6e5")
        False
        >>> is_pos_int("1_964")
        False
        >>> is_pos_int("NaN")
        False
        >>> is_pos_int("None")
        False
        >>> is_pos_int("27j+5")
        False
        >>> is_pos_int("abcdefg")
        False
        >>> is_pos_int("12345abcdefg")
        False
        >>> is_pos_int("~26.3")
        False
        >>> is_pos_int("^26.3")
        False
    """

    assert isinstance(num_str, str)
    if num_str.isdigit():
        return int(num_str) != 0
    return False

if __name__ == "__main__":
    import doctest
    doctest.testmod()

