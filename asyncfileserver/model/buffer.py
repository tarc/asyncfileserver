class Buffer(object):
    def __init__(self, buffer=bytearray(), index=0):
        self._buffer = buffer
        self._index = index

    def extend(self, buffer):
        self._buffer.extend(buffer)