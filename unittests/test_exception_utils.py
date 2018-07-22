import unittest

import fenalib.exception_utils as exc_utils

class TestExceptionUtils(unittest.TestCase):
    def name_error(self):
        with self.assertRaises(NameError) as cm:
            a  # pylint: disable=undefined-variable, pointless-statement
        return cm.exception

    def div_by_zero_error(self):
        with self.assertRaises(ZeroDivisionError) as cm:
            1/0  # pylint: disable=pointless-statement

        return cm.exception

    def test_control(self):
        e = self.name_error()
        self.assertEqual(str(e), "name 'a' is not defined")

        e = self.div_by_zero_error()
        self.assertEqual(str(e), "division by zero")

    def test_exc_add_msg(self):
        e = self.name_error()
        exc_utils.exc_add_msg(e, "like at all")
        self.assertEqual(str(e), "name 'a' is not defined like at all")

        exc_utils.exc_add_msg(e, "although at least 'e' is defined", sep=", ")
        self.assertEqual(str(e), "name 'a' is not defined like at all, although at least 'e' is defined")

    def test_exc_set_msg(self):
        e = self.div_by_zero_error()
        exc_utils.exc_set_msg(e, "this is what happens when you do /kill @e")
        self.assertEqual(str(e), "this is what happens when you do /kill @e")

