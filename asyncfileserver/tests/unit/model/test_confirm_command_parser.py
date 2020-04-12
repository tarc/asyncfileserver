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

    def test_some_iterations(self):
        parser = ConfirmCommandParser()
        instance, index = parser.parse(b'y')

        self.assertEqual(index, 0)
        self.assertIsNone(instance)

        instance, index = parser.parse(b'yl')

        self.assertEqual(index, 2)
        self.assertIsNone(instance)

        instance, index = parser.parse(b'y\n')

        self.assertEqual(index, 2)
        self.assertEqual(instance, ConfirmCommand(b'YL', True))

        instance, index = parser.parse(b'c')

        self.assertEqual(index, 0)
        self.assertEqual(instance, None)

        instance, index = parser.parse(b'C\n')

        self.assertEqual(index, 2)
        self.assertEqual(instance, ConfirmCommand(b'C'))

        instance, index = parser.parse(b'\n')

        self.assertEqual(index, 1)
        self.assertEqual(instance, ConfirmCommand(b'\n', True))

    def test_some_iterations_r(self):
        parser = ConfirmCommandParser()
        instance, index = parser.parse(b'y')

        self.assertEqual(index, 0)
        self.assertIsNone(instance)

        instance, index = parser.parse(b'yl')

        self.assertEqual(index, 2)
        self.assertIsNone(instance)

        instance, index = parser.parse(b'y\r\n')

        self.assertEqual(index, 3)
        self.assertEqual(instance, ConfirmCommand(b'YL', True))

        instance, index = parser.parse(b'c')

        self.assertEqual(index, 0)
        self.assertEqual(instance, None)

        instance, index = parser.parse(b'C\r\n')

        self.assertEqual(index, 3)
        self.assertEqual(instance, ConfirmCommand(b'C'))

        instance, index = parser.parse(b'C\r\r\n')

        self.assertEqual(index, 4)
        self.assertEqual(instance, ConfirmCommand(b'C'))

        instance, index = parser.parse(b'\r')

        self.assertEqual(index, 1)
        self.assertEqual(instance, None)

        instance, index = parser.parse(b'\n')

        self.assertEqual(index, 1)
        self.assertEqual(instance, ConfirmCommand(b'\r', True))

        instance, index = parser.parse(b'\r\n')

        self.assertEqual(index, 2)
        self.assertEqual(instance, ConfirmCommand(b'\r', True))

        instance, index = parser.parse(b'12345\r\r\r\n')

        self.assertEqual(index, 9)
        self.assertEqual(instance, ConfirmCommand(b'1', True))
