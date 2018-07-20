import sys

"""
"""

def exc_add_msg(e: Exception, message: str) -> Exception:
    """
    Args:
        e (Exception): The exception to add a message to
        message (str): The message to be added to the exception

    Returns:
        Exception: The same as `e`
    """
    args = list(e.args)
    args[-1] += ' ' + message
    e.args = tuple(args)
    return e

def exc_set_msg(e: Exception, message: str) -> Exception:
    """
    Args:
        e (Exception): The exception to set a message to
        message (str): The message to be set to the exception

    Returns:
        Exception: The same as `e`
    """
    e.args = (message,)
    return e

if __name__ == "__main__":
    try:
        a
    except NameError as e:
        # print(exc_add_message(e, "bruh"))
        # raise exc_add_message(e, "bruh").with_traceback(e.__traceback__)
        # tb = sys.exc_info()[2]
        # raise exc_add_message(e, "bruh").with_traceback(tb)
        # e.args = ('hello',)
        # raise e.with_traceback(tb)
        # raise e
        raise exc_add_msg(e, 'just like your face')
    print('ye')
