"""
Simple assert utils to make sure that an object matches some specified type

The main difference between using this function and using assert isinstance(...)
is that it provides a more in-depth error message
"""

def assert_type(checked_object, *valid_types, additional_message=None, optional=False):
    """
    Checks whether an object is an instance of any of the valid types

    Args:
        checked_object (any)
        valid_types (any)
        additional_message (str or None)
        optional (bool): Whether the object can be a None object or not

    Examples:
        >>> assert_type([], list, int)
        >>> assert_type(45, list, int)
        >>> assert_type("yep", list, int)
        Traceback (most recent call last):
            ...
        AssertionError: Expected type of 'yep' to be one of (<class 'list'>, <class 'int'>) but got <class 'str'>

        >>> assert_type((25,), list)
        Traceback (most recent call last):
            ...
        AssertionError: Expected type of (25,) to be <class 'list'> but got <class 'tuple'>
    """
    assert isinstance(additional_message, str) or additional_message is None
    assert isinstance(optional, bool)

    if not (isinstance(checked_object, valid_types) or (optional and checked_object is None)):
        if len(valid_types) == 1:
            checked_types_str = f"{valid_types[0]}"
        else:
            checked_types_str = f"one of {valid_types}"

        if optional:
            checked_types_str += " or None"

        full_message = f"Expected type of {checked_object!r} to be {checked_types_str} but got {type(checked_object)}"
        if additional_message is not None:
            full_message += f" {additional_message}"
        raise AssertionError(full_message)

def assert_list_types(checked_list, *valid_types):
    """
    Checks whether all objects in a list are instances of one of the valid types

    Args:
        checked_list (list)
        valid_types (any)

    Examples:
        >>> assert_list_types([1, 3, 2], int)
        >>> assert_list_types(["a", "b", "c"], str)
        >>> assert_list_types(["a", "b", "c"], int, str)
        >>> assert_list_types(["a", "b", "c"], int)
        Traceback (most recent call last):
            ...
        AssertionError: Expected type of 'a' to be <class 'int'> but got <class 'str'> in index 0 of list ['a', 'b', 'c']

        >>> assert_list_types([23, "b", 327.4], int, str)
        Traceback (most recent call last):
            ...
        AssertionError: Expected type of 327.4 to be one of (<class 'int'>, <class 'str'>) but got <class 'float'> in index 2 of list [23, 'b', 327.4]
    """
    for index, item in enumerate(checked_list):
        assert_type(item, *valid_types, additional_message=f"in index {index} of list {checked_list}")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
