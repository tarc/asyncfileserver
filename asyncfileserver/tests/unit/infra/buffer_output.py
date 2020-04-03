class BufferOutput(object):
    def __init__(self, buffer: list):
        self._buffer = buffer

    async def print(self, data):
        self._buffer.append(data)
