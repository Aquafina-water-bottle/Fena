from typing import NamedTuple
from collections import namedtuple

"""
http://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html
http://jfine-python-classes.readthedocs.io/en/latest/decorators.html

Syntax of a decorator on a class:
    @decorator
    class A:
        ...
    a = A()

is equal to
    class A:
        ...
    a = decorator(A)
"""

def addrepr(cls):
    """
    Decorator meant to be used on classes to set a __repr__ method
    that contains all variables of the classes

    Examples:
        >>> @addrepr
        ... class A:
        ...     def __init__(self, a, b, c):
        ...         self.a = a
        ...         self.b = b
        ...         self.c = c

        >>> a = A("1", 2, (3, "4"))
        >>> repr(a)
        "A[a='1', b=2, c=(3, '4')]"

        >>> @addrepr
        ... class B(NamedTuple):
        ...     hue: int
        ...     saturation: float
        ...     lightness: float

        >>> b = B(5, 3.5, 7.6)
        >>> repr(b)
        "B[hue=5, saturation=3.5, lightness=7.6]"
    """
    def __repr__(self):
        # `type(self)` is used instead of `cls` because `cls` only refers to the most parent object if inherited
        # while `type(self)` guarantees to get the class name of the current class
        class_name = type(self).__name__

        variables = []
        try:
            object_dict = vars(self)
        except TypeError:
            # possibly NamedTuple
            object_dict = dict(self._asdict())

        for variable, value in object_dict.items():
            variables.append(f"{variable}={value!r}")
        variables_str = ", ".join(variables)

        return f"{class_name}[{variables_str}]"

    # sets the __repr__ method as the defined __repr__ because methods can be defined outside classes
    # take that 1st year university test questions
    cls.__repr__ = __repr__

    # returns itself because of decorator(class) syntax
    return cls

if __name__ == "__main__":
    # import doctest
    # doctest.testmod()

    @addrepr
    class B(NamedTuple):
        hue: int
        saturation: float
        lightness: float

    b = B(1, 2.3, 4.5)
    print(b)




