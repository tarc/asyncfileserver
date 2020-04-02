import re


class ConfirmCommand(object):
    _pattern = re.compile(b'\W')

    def __init__(self, data: bytearray):
        self._data = self._format(data)

    def go_on(self):
        return self._data == b"C"

    def yes(self):
        return self._data == b"Y"

    def _format(self, data):
        upper = data.upper()
        return re.sub(self._pattern, b'', upper) 
