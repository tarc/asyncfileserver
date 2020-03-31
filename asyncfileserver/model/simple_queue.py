class SimpleQueue(object):
    def __init__(self, queue):
        self._queue = queue

    async def get(self) -> bytes:
        item: bytearray = await self._queue.get()
        return bytes(item) if item != None else None

    def task_done(self):
        self._queue.task_done()

    async def put(self, item: bytearray):
        await self._queue.put(item)
