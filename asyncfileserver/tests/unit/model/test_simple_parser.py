import unittest
from unittest.mock import MagicMock

from asyncfileserver.model.simple_parser import SimpleParser


class TestSimpleParser(unittest.TestCase):

    @staticmethod
    def t_f(d): return lambda k: d[k]

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

        is_prefix_of_some_key = TestSimpleParser.t_f({
            b'A': True,
            b'A ': False,
            b'\nAB': False,
            b'AB\r': False,
            b'AB': True,
            b'ABA': False,
            b'\r': False,
            b'A AB A AB\nA': False
        })

        longest_key_prefix_of = TestSimpleParser.t_f({
            b'A': (b'A', A),
            b'A ': (b'A', A),
            b'\nAB': None,
            b'AB\r': (b'AB', AB),
            b'AB':  (b'AB', AB),
            b'ABA': (b'AB', AB),
            b'\r': None,
            b'A AB A AB\nA': (b'A', A),
        })

        trie = MagicMock(is_prefix_of_some_key=is_prefix_of_some_key,
                         longest_key_prefix_of=longest_key_prefix_of)

        trie_factory = MagicMock()
        trie_factory.get = MagicMock(return_value=trie)

        parser = SimpleParser(tag_commands, commands, error, trie_factory)

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

        is_prefix_of_some_key = TestSimpleParser.t_f({
            b'AB': True,
            b'ABDE': False,
            b'\r\nABC\r\n': False,
            b'ABC\r\n': False
        })

        longest_key_prefix_of = TestSimpleParser.t_f({
            b'AB': None,
            b'ABDE': (b'ABD', ABD),
            b'\r\nABC\r\n': None,
            b'ABC\r\n': (b'ABC', ABC)
        })

        trie = MagicMock(is_prefix_of_some_key=is_prefix_of_some_key,
                         longest_key_prefix_of=longest_key_prefix_of)

        trie_factory = MagicMock()
        trie_factory.get = MagicMock(return_value=trie)

        parser = SimpleParser(tag_commands, commands, error, trie_factory)

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

        is_prefix_of_some_key = TestSimpleParser.t_f({
            b'': True,
            b'CBA': False,
            b'\n': False,
            b'ABE ABC ABD\r': False
        })

        longest_key_prefix_of = TestSimpleParser.t_f({
            b'': None,
            b'CBA': None,
            b'\n': None,
            b'ABE ABC ABD\r': None
        })

        trie = MagicMock(is_prefix_of_some_key=is_prefix_of_some_key,
                         longest_key_prefix_of=longest_key_prefix_of)

        trie_factory = MagicMock()
        trie_factory.get = MagicMock(return_value=trie)

        parser = SimpleParser(tag_commands, commands, error, trie_factory)

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
