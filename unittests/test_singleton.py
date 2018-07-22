import unittest
from typing import NamedTuple

from fenalib.repr_utils import addrepr
import fenalib.singleton as singleton

@addrepr
class Control:
    def __init__(self, a, b):
        self.a = a
        self.b = b

@addrepr
class RegularSingleton(singleton.Singleton):
    # only sets if the attributes exist
    def __init__(self, *args):
        if args:
            self.a = args[0]
            self.b = args[1]

class SingletonFromControl(singleton.Singleton, Control):
    pass

class ImmutableBase(NamedTuple):
    a: int
    b: int

class ImmutableSingleton(singleton.Singleton, ImmutableBase):
    pass


class TestSingleton(unittest.TestCase):
    def test_control(self):
        """
        Ensures the objects of the control and immutable base are different
        """
        c1 = Control(1, 2)
        c2 = Control(1, 2)
        self.assertNotEqual(id(c1), id(c2))

        i1 = ImmutableBase(1, 2)
        i2 = ImmutableBase(1, 2)
        self.assertNotEqual(id(i1), id(i2))

    def test_regular_singleton(self):
        """
        Ensures the objects of the singletons are the same
        """
        rs1 = RegularSingleton(1, 2)
        rs2 = RegularSingleton(3, 4)
        rs3 = RegularSingleton()

        self.assertTrue(id(rs1) == id(rs2) == id(rs3))
        self.assertEqual(rs1.a, 3)
        self.assertEqual(rs1.b, 4)

    def test_singleton_from_control(self):
        """
        Ensures the objects of the singletons that inherit from control
        are the same
        """
        sc1 = SingletonFromControl(1, 2)
        sc2 = SingletonFromControl(3, 4)

        with self.assertRaises(TypeError) as cm:
            SingletonFromControl()

        self.assertEqual(str(cm.exception), "__init__() missing 2 required positional arguments: 'a' and 'b'")
        self.assertEqual(id(sc1), id(sc2))
        self.assertEqual(sc1.a, 3)
        self.assertEqual(sc1.b, 4)

    def test_singleton_immutable(self):
        """
        Ensures that objects that inherit from a NamedTuple base and Singleton
        are still singletons
        """
        # final values are the first values given to them unlike the above
        is1 = ImmutableSingleton(1, 2)
        is2 = ImmutableSingleton(3, 4)
        is3 = ImmutableSingleton()

        self.assertTrue(id(is1) == id(is2) == id(is3))
        self.assertEqual(is1.a, 1)
        self.assertEqual(is1.b, 2)


