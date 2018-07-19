class Singleton:
    def __new__(cls, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Ensures they are the same class
        """
        attribute = f"_{cls.__name__}"
        if not hasattr(cls, attribute):
            setattr(cls, attribute, super().__new__(cls))
        print(cls, attribute)
        return getattr(cls, attribute)

