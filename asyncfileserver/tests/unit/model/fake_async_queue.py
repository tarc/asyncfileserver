import asyncio


class FakeAsyncQueue(object):
    def __init__(self, queue: list):
        self._queue = queue
        self._count_task_done = 0

    async def put(self, item):
        self._queue.append(item)

    async def get(self):

        # Release control back to event loop. This is needed because for
        # File.data() to work properly it must get a chance to read the file
        # before getting a item from the queue.
        await asyncio.sleep(0)

        return self._queue[self._count_task_done]

    def task_done(self):
        self._count_task_done = self._count_task_done + 1

    def how_many_tasks_done(self) -> int:
        return self._count_task_done
