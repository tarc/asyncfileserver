import unittest

from asyncfileserver.model.data_view_formatter import DataViewFormatter


class TestDataViewFormatter(unittest.TestCase):
    def test_format(self):
        factory = DataViewFormatter()
        data = bytearray(b'\x0135=X\x01')
        instance = factory.format(data)

        self.assertEqual(f"{instance}", f"<DATA size: {len(data)}>")
