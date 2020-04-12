import asyncio
from contextlib import asynccontextmanager


class Listener(object):

    def __init__(self, server_factory):
        self._server_factory = server_factory
        self._server = None

    async def listen(self):
        self._server = await self._server_factory.get()
        await self._server.start_serving()

    async def stop(self):
        self._server.close()
        await self._server.wait_closed()
        self._server = None

    async def close(self):
        if self._server != None:
            await self.stop()


@asynccontextmanager
async def listen(server_factory):
    listener = None
    try:
        listener = Listener(server_factory)
        yield listener
    finally:
        if listener != None:
            await listener.close()
