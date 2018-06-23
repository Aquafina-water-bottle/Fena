if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

from fenalib.config_data import ConfigData
from fenalib.token_classes import TypedToken
from fenalib.number_utils import is_number

config_data = ConfigData()

def is_coord(string):
    """
    Checks whether a string is a valid coordinate type

    Args:
        string (str)

    Returns:
        bool: Whether the token value can be a coordinate
    """
    if config_data.version == "1.12":
        return string and (string[0] in "~" and (len(string) == 1 or is_number(string[1:]))) or is_number(string)
    return string and (string[0] in "~^" and (len(string) == 1 or is_number(string[1:]))) or is_number(string)

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
            - if the length is 2, then it can only contain world coordinates
    """
    # records the supposed global coord type as either "relative" or "local", as to skip absolute

    overall_coord_type = None
    if not (2 <= len(tokens) <= 3):
        return False

    for token in tokens:
        if not is_coord_token(token):
            return False

        coord_type = get_token_coord_type(token)
        if coord_type in ("relative", "absolute"):
            coord_type = "world"

        if overall_coord_type is None:
            overall_coord_type = coord_type
        elif overall_coord_type != coord_type:
            return False

    if overall_coord_type == "local" and len(tokens) == 2:
        return False
    return True

if __name__ == "__main__":
    # test cases for this are under test_fena/ now
    pass