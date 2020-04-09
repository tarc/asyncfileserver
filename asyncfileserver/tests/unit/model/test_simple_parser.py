import unittest

from asyncfileserver.model.simple_parser import SimpleParser
from asyncfileserver.infra.pytrie import TrieFactory


class TestSimpleParser(unittest.TestCase):
    def test_parse_intersecting_commands(self):

        def AB(data):
            pass

        def A(data):
            pass

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

        command, size = parser.parse(b'\n')

        self.assertEqual(command, (A, b'A '))
        self.assertEqual(size, 1)
