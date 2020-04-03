import unittest

from asyncfileserver.model.view_data_factory import ViewDataFactory


class TestViewDataFactory(unittest.TestCase):
    def test_create(self):
        factory = ViewDataFactory()
        data = bytearray(b'\x0135=X\x01')
        instance = factory.create(data)

        self.assertEqual(f"{instance}", f"<DATA size: {len(data)}>")
