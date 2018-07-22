import unittest
import logging
import os

from io import StringIO as StringIOBase

import fenalib.logging_setup as logging_setup

class StringIO(StringIOBase):
    def clear(self):
        """
        Generally clears the stringio
        This was gotten from https://stackoverflow.com/a/32001771

        Note that I actually have to clear it so I don't have to set another stream

        Args:
            sio (StringIO)

        Returns:
            str: The cleared value
        """
        value = self.getvalue()
        self.truncate(0)
        self.seek(0)
        return value

class TestLoggingSetup(unittest.TestCase):
    def test_logging_setup(self):
        # clears the log file if it exists
        debug_info_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fenalib", "log", "debug_info.log")
        try:
            os.remove(debug_info_path)
        except FileNotFoundError:
            pass

        # creates default handler
        string_io = StringIO()
        logging.basicConfig(stream=string_io)
        logging.warning("test begin")
        self.assertEqual(string_io.clear(), "WARNING:root:test begin\n")

        # creates expected handler
        logging_setup.setup_logging()
        logging.warning("test after setup logging")
        self.assertRegex(string_io.clear(), r'\[\d+:\d+:\d+] \[<NO FILE>/WARNING\]: test after setup logging')

        # sets the file name
        logging_setup.format_file_name("test_logging_setup.py")
        logging.warning("test after file name setup")
        self.assertRegex(string_io.clear(), r'\[\d+:\d+:\d+] \[test_logging_setup.py/WARNING\]: test after file name setup')

        # checks the log file for the correct output
        with open(debug_info_path) as file:
            self.assertRegex(file.readline(), r'\[\d+/\d+/\d+ \d+:\d+:\d+\] \[<NO FILE>/DEBUG\]: Logger has been set up')
            self.assertRegex(file.readline(), r'\[\d+/\d+/\d+ \d+:\d+:\d+\] \[<NO FILE>/WARNING\]: test after setup logging')
            self.assertRegex(file.readline(), r'\[\d+/\d+/\d+ \d+:\d+:\d+\] \[test_logging_setup.py/WARNING\]: test after file name setup')
            self.assertEqual(file.readline(), '')
            file.close()

