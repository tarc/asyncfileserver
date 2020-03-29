import asyncio
import sys


class Client(object):
    def __init__(self, queue, output):
        self._queue = queue
        self._output = output

    async def write(self):
        item = await self._queue.get()
        self._queue.task_done()
        while(item):
            await self._output.print(item)
            item = await self._queue.get()
