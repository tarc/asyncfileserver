import asyncio
import sys

from fileserver.infra.async_console_output import AsyncConsoleOutput as Out


class Client(object):
    def __init__(self, queue, output=Out(),
                 writing_buffer_size: int = 17):
        self._queue = queue
        self._buffer_size = writing_buffer_size
        self._output = output

    async def write(self):
        pass
        #await self._output.print(data)
