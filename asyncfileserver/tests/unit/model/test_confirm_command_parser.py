import unittest

from asyncfileserver.model.confirm_command_parser import ConfirmCommandParser
from asyncfileserver.model.confirm_command import ConfirmCommand

class TestConfirmCommandParser(unittest.TestCase):
    def test_single_char_eol(self):
        parser = ConfirmCommandParser()
        instance, index = parser.parse(b'y\n')

        self.assertEqual(index, 2)
        self.assertFalse(instance.go_on())
        self.assertTrue(instance.yes())

    def test_single_char(self):
        parser = ConfirmCommandParser()
        instance, index = parser.parse(b'y')

        self.assertEqual(index, 0)
        self.assertIsNone(instance)

    def test_incomplete_cmd_and_then_complete(self):
        parser = ConfirmCommandParser()
        instance, index = parser.parse(b'y')

        self.assertEqual(index, 0)
        self.assertIsNone(instance)

        instance, index = parser.parse(b'y ')

        self.assertEqual(index, 2)
        self.assertIsNone(instance)

        instance, index = parser.parse(b'\n')

        self.assertEqual(index, 1)
        self.assertEqual(instance, ConfirmCommand(b'Y'))
