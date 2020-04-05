class Listener(object):
    def __init__(self, server_factory):
        self._server_factory = server_factory
        self._server = None

    async def listen(self):
        self._server = await self._server_factory.get()
        await self._server.serve_forever()

    async def stop(self):
        self._server.close()
        await self._server.wait_close()
