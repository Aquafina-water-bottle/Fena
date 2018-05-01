def coroutine(func):
    """
    Used as a decorator for all coroutines in a parser to prime the coroutine
    """
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return start