import unittest

from asyncfileserver.model.simple_parser import SimpleParser
from asyncfileserver.infra.pytrie import TrieFactory


class TestSimpleParser(unittest.TestCase):
    def test_parse_one_command_prefix_of_the_other(self):

        AB = object()
        A = object()
        error = object()

        tag_commands = [
            b'AB',
            b'A',
        ]
        commands = [
            AB,
            A
        ]

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

    def test_parse_intersecting_commands(self):

        ABC = object()
        ABD = object()
        error = object()

        tag_commands = [
            b'ABC',
            b'ABD',
        ]
        commands = [
            ABC,
            ABD
        ]

        parser = SimpleParser(tag_commands, commands, error, TrieFactory())

        command, size = parser.parse(b'AB')

        self.assertIsNone(command)
        self.assertEqual(size, 0)

        command, size = parser.parse(b'ABDE')

        self.assertIsNone(command)
        self.assertEqual(size, 4)

        command, size = parser.parse(b'\r\nABC\r\n')

        self.assertEqual(command, (error, b'ABDE'))
        self.assertEqual(size, 2)

        command, size = parser.parse(b'ABC\r\n')

        self.assertEqual(command, (ABC, b'ABC\r'))
        self.assertEqual(size, 5)

    def test_parse_empty_string_then_non_matching_data(self):

        ABC = object()
        ABD = object()
        error = object()

        tag_commands = [
            b'ABC',
            b'ABD',
        ]
        commands = [
            ABC,
            ABD
        ]

        parser = SimpleParser(tag_commands, commands, error, TrieFactory())

        command, size = parser.parse(b'')

        self.assertIsNone(command)
        self.assertEqual(size, 0)

        command, size = parser.parse(b'CBA')

        self.assertIsNone(command)
        self.assertEqual(size, 3)

        command, size = parser.parse(b'')

        self.assertIsNone(command)
        self.assertEqual(size, 0)

        command, size = parser.parse(b'\n')

        self.assertEqual(command, (error, b'CBA'))
        self.assertEqual(size, 1)

        command, size = parser.parse(b'')

        self.assertIsNone(command)
        self.assertEqual(size, 0)

        command, size = parser.parse(b'ABE ABC ABD\r')

        self.assertIsNone(command)
        self.assertEqual(size, 12)

        command, size = parser.parse(b'')

        self.assertIsNone(command)
        self.assertEqual(size, 0)

        command, size = parser.parse(b'\n')

        self.assertEqual(command, (error, b'ABE ABC ABD\r'))
        self.assertEqual(size, 1)
