import asyncio
import sys

from fileserver.infra.async_console_output import AsyncConsoleOutput as Out


class Client(object):
    def __init__(self, queue, output=Out()):
        self._queue = queue
        self._output = output

    async def write(self):
        item = await self._queue.get()
        self._queue.task_done()
        while(item):
            await self._output.print(item)
            item = await self._queue.get()
