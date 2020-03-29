class AsyncConsoleOutput(object):
    def __init__(self, writer):
        self._writer = writer

    async def print(self, data):
        self._writer.write(data)
        await self._writer.drain()
