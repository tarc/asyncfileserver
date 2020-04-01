class AsyncConsoleInput(object):
    def __init__(self, reader):
        self._reader = reader

    async def input(self):
        line = await self._reader.readline()
        return line
