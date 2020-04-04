class Client(object):
    def __init__(self, queue, input, output):
        self._queue = queue
        self._input = input
        self._output = output

    async def read(self):
        item = await self._input()
        while(item):
            item = await self._input()

    async def write(self):
        item = await self._queue.get()
        while(item):
            await self._output.print(item)
            self._queue.task_done()
            item = await self._queue.get()

        self._queue.task_done()
