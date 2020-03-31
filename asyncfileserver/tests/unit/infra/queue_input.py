import asyncio


class QueueInput(object):
    def __init__(self, queue: list):
        self._queue = queue
        self._index = 0

    async def input(self):
        await asyncio.sleep(0)

        if self._index >= len(self._queue):
            return b''

        item = self._queue[self._index]
        self._index = self._index + 1
        return item
