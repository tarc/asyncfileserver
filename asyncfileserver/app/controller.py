class Controller(object):
    def __init__(self, listener):
        self._listener = listener

    async def open_command(self, data):
        await self._listener.listen()
        return "Finished starting."

    async def close_command(self, data):
        await self._listener.stop()
        return "Finished stopping."
