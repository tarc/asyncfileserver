import unittest

from asyncfileserver.model.confirm_command_factory import ConfirmCommandFactory

class TestConfirmCommandFactory(unittest.TestCase):
    def test_create(self):
        factory = ConfirmCommandFactory()
        instance = factory.create(bytearray(b'Y\n'))

        self.assertFalse(instance.go_on())
        self.assertTrue(instance.yes())