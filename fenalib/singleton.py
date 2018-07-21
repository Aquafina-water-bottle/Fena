
class Singleton:
    def __new__(cls, *args, **kwargs):
        attr_name = f"_{cls.__name__}"
        if not hasattr(cls, attr_name):
            try:
                attribute = super().__new__(cls, *args, **kwargs)
            except TypeError as e:
                exc_add_msg(e, f'with class {cls.__qualname__}'
                raise

            setattr(cls, attr_name, attribute)
        return getattr(cls, attr_name)

