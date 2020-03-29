class ConfirmPutQueue(object):
    def __init__(self, arbiter):
        self._arbiter = arbiter

    async def get(self) -> bytes:
        item: bytearray = await self._queue.get()
        return bytes(item) if item else None

    def task_done(self):
        self._queue.task_done()

    async def put(self, item: bytearray):
        await self._queue.put(item)

