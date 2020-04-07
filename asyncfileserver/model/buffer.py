class Buffer(object):
    def __init__(self, buffer=bytearray()):
        self._buffer = buffer

    def extend(self, buffer):
        self._buffer.extend(buffer)

    def get(self):
        return bytes(self._buffer)

    def advance(self, size):
        self._buffer = self._buffer[size:]
