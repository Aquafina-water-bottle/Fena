from fenalib.exception_utils import exc_add_msg

class Singleton:
    """
    Singleton class based off of:
        https://colab.research.google.com/drive/1eajT5Rl9tA-7RmSHMME54B81U5aSKSni#scrollTo=nfQZINGxuUdK

    Sets its own attributes based off of:
        https://stackoverflow.com/questions/2466191/set-attributes-from-dictionary-in-python

    """

    def __new__(cls, *args, **kwargs):
        attr_name = f"_{cls.__name__}"
        if not hasattr(cls, attr_name):
            try:
                attribute = super().__new__(cls, *args, **kwargs)
            except TypeError as e:
                exc_add_msg(e, f'with class {cls.__qualname__}')
                raise

            setattr(cls, attr_name, attribute)
        return getattr(cls, attr_name)

