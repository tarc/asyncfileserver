class AsyncConsoleOutput(object):
    def __init__(self, writer):
        self._writer = writer

    async def print(self, data):
        if not isinstance(data, (str, bytes, bytearray, memoryview)):
            self._writer.write(str(data))
        else:
            self._writer.write(data)
        await self._writer.drain()
