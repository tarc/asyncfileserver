import aioconsole

class AsyncConsoleOutput(object):
    async def print(self, data):
        await aioconsole.aprint(data)
