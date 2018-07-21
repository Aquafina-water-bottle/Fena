"""
Utils to change the message of an exception
"""

__all__ = [
    "exc_add_msg",
    "exc_set_msg",
    ]

def exc_add_msg(e: Exception, message: str, sep=" "):
    """
    Args:
        e (Exception): The exception to add a message to
        message (str): The message to be added to the exception
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


