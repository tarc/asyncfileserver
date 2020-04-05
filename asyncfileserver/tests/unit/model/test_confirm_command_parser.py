import unittest

from asyncfileserver.model.confirm_command_parser import ConfirmCommandParser

class TestConfirmCommandParser(unittest.TestCase):
    def test_create(self):
        parser = ConfirmCommandParser()
        instance = parser.parse(bytearray(b'Y\n'))

        self.assertFalse(instance.go_on())
        self.assertTrue(instance.yes())