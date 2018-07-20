"""
Utils to change the message of an exception
"""

def exc_add_msg(e: Exception, message: str, sep=" "):
    """
    Args:
        e (Exception): The exception to add a message to
        message (str): The message to be added to the exception

    Examples:
        >>> a
        Traceback (most recent call last):
            ...
        NameError: name 'a' is not defined

        >>> try:
        ...     a
        ... except NameError as e:
        ...     exc_add_msg(e, 'like at all')
        ...     raise
        Traceback (most recent call last):
            ...
        NameError: name 'a' is not defined like at all

        >>> try:
        ...     a
        ... except NameError as e:
        ...     exc_add_msg(e, ': pool is closed due to aids', sep='')
        ...     raise
        Traceback (most recent call last):
            ...
        NameError: name 'a' is not defined: pool is closed due to aids

        >>> try:
        ...     a
        ... except NameError as e:
        ...     exc_add_msg(e, 'lol', sep=' lolololololol ')
        ...     raise
        Traceback (most recent call last):
            ...
        NameError: name 'a' is not defined lolololololol lol
    """
    args = list(e.args)
    assert args, "You can only add a message if a message exists"
    args[-1] += sep + message
    e.args = tuple(args)


def exc_set_msg(e: Exception, message: str):
    """
    Args:
        e (Exception): The exception to set a message to
        message (str): The message to be set to the exception

    Examples:
        >>> try:
        ...     a
        ... except NameError as e:
        ...     exc_set_msg(e, 'something is not defined')
        ...     raise
        Traceback (most recent call last):
            ...
        NameError: something is not defined
    """
    e.args = (message,)


def test():
    try:
        a
    except NameError as e:
        import sys
        import traceback

        tb = sys.exc_info()[2]
        print("traceback 1:")
        print(traceback.format_exc())

        print("traceback 2:")
        traceback.print_tb(tb)

        print("traceback 3:")
        raise e
    # raise Exception().with_traceback(tb)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # test()


