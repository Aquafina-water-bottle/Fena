class Singleton:
    def __new__(cls, *args, **kwargs):
        attr_name = f"_{cls.__name__}"
        if not hasattr(cls, attr_name):
            try:
                attribute = super().__new__(cls, *args, **kwargs)
            except TypeError as e:
                import sys
                tb = sys.exc_info()[2]
                message = f'{e.args[0]} with class {cls.__qualname__}'
                raise TypeError(message).with_traceback(tb)

            setattr(cls, attr_name, attribute)
        return getattr(cls, attr_name)

