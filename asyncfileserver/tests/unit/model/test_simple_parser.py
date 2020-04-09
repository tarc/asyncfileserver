import unittest

from asyncfileserver.model.simple_parser import SimpleParser
from asyncfileserver.infra.pytrie import TrieFactory


class TestSimpleParser(unittest.TestCase):
    def test_parse_one_command_prefix_of_the_other(self):

        AB = object()
        A = object()

        tag_commands = [
            b'AB',
            b'A',
        ]
        commands = [
            AB,
            A
        ]

        def error(data):
            return None

        parser = SimpleParser(tag_commands, commands, error, TrieFactory())

        command, size = parser.parse(b'A')

        self.assertIsNone(command)
        self.assertEqual(size, 0)

        command, size = parser.parse(b'A ')

        self.assertIsNone(command)
        self.assertEqual(size, 2)

        command, size = parser.parse(b'\nAB')

        self.assertEqual(command, (A, b'A '))
        self.assertEqual(size, 1)

        command, size = parser.parse(b'AB\r')

        self.assertIsNone(command)
        self.assertEqual(size, 3)

        command, size = parser.parse(b'\nAB')

        self.assertEqual(command, (AB, b'AB\r'))
        self.assertEqual(size, 1)

        command, size = parser.parse(b'AB')

        self.assertIsNone(command)
        self.assertEqual(size, 0)

        command, size = parser.parse(b'ABA')

        self.assertIsNone(command)
        self.assertEqual(size, 3)

        command, size = parser.parse(b'\r')

        self.assertIsNone(command)
        self.assertEqual(size, 1)

        command, size = parser.parse(b'A AB A AB\nA')

        self.assertEqual(command, (error, b'ABA'))
        self.assertEqual(size, 10)
