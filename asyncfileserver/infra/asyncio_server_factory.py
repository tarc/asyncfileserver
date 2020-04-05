import asyncio


class ServerFactory(object):
    def __init__(self, address, port, start_client,
                 loop=asyncio.get_event_loop()):
        self._address = address
        self._port = port
        self._start_client = start_client
        self._loop = loop

    async def get(self):
        def factory():
            reader = asyncio.StreamReader(loop=self._loop)
            protocol = asyncio.StreamReaderProtocol(reader, self._start_client,
                                                    loop=self._loop)
            return protocol

        return await self._loop.create_server(factory,
                                              host=self._address,
                                              port=self._port,
                                              start_serving=False)
