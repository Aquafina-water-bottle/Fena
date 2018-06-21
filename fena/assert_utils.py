"""
Simple assert utils to make sure that an object matches some specified type
or the items in an iterable match some specified type

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
        #full_message = f"Expected type of {type(checked_object)} to be {checked_types_str} but got {type(checked_object)}"
        if additional_message is not None:
            full_message += f" {additional_message}"
        raise AssertionError(full_message)

def assert_iterable_types(checked_iterable, *valid_types, duplicate_key=None):
    """
    Checks whether all objects in a iterable are instances of one of the valid types

    Args:
        checked_iterable (iterable)
        valid_types (any)
        duplicate_key (None or callable): A function to give the value to check for duplicates
            Note that if you want to detect duplicates with itself, just do `duplicate_key=lambda x: x`
            If the option is None, no duplicate checking will be done

    Examples:
        >>> assert_iterable_types([1, 3, 2], int)
        >>> assert_iterable_types(["a", "b", "c"], str)
        >>> assert_iterable_types(("a", "b", "c"), int, str)
        >>> assert_iterable_types(["a", "b", "c"], int)
        Traceback (most recent call last):
            ...
        AssertionError: Expected type of 'a' to be <class 'int'> but got <class 'str'> in index 0 of iterable ['a', 'b', 'c']

        >>> assert_iterable_types([23, "b", 327.4], int, str)
        Traceback (most recent call last):
            ...
        AssertionError: Expected type of 327.4 to be one of (<class 'int'>, <class 'str'>) but got <class 'float'> in index 2 of iterable [23, 'b', 327.4]

        >>> assert_iterable_types([23, "b", 327.4], int, str, duplicate_key=lambda x: x)
        Traceback (most recent call last):
            ...
        AssertionError: Expected type of 327.4 to be one of (<class 'int'>, <class 'str'>) but got <class 'float'> in index 2 of iterable [23, 'b', 327.4]

        >>> assert_iterable_types(("a", "b", "c"), str, duplicate_key=lambda x: x)
        >>> assert_iterable_types(("a", "b", "a"), str, duplicate_key=lambda x: x)
        Traceback (most recent call last):
            ...
        AssertionError: Found a duplicate of 'a' in 'a'

        >>> assert_iterable_types(["123", "142", "225"], str, duplicate_key=lambda x: x[0])
        Traceback (most recent call last):
            ...
        AssertionError: Found a duplicate of '1' in '142'
    """
    for index, item in enumerate(checked_iterable):
        assert_type(item, *valid_types, additional_message=f"in index {index} of iterable {checked_iterable}")

    # checks for duplicates
    if duplicate_key is not None:
        assert callable(duplicate_key), "The duplicate key must be a function"

        # uses a set because only the containment of an item matters
        found_objects = set()

        # iterates through each checked object to see if its within the found objects
        for checked_object in checked_iterable:
            result_object = duplicate_key(checked_object)
            # assert result_object not in found_objects, f"Found a duplicate of {result_object!r} in iterable {checked_iterable}"
            assert result_object not in found_objects, f"Found a duplicate of {result_object!r} in {result_object}"
            found_objects.add(result_object)

def assert_list_types(checked_list, *valid_types, **kwargs):
    assert_type(checked_list, list)
    assert_iterable_types(checked_list, *valid_types, **kwargs)

def assert_tuple_types(checked_tuple, *valid_types, **kwargs):
    assert_type(checked_tuple, tuple)
    assert_iterable_types(checked_tuple, *valid_types, **kwargs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
