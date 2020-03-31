import asyncio
import aiounittest

from asyncfileserver.model.confirm_put_queue import ConfirmPutQueue
from asyncfileserver.tests.unit.model.fake_async_queue import FakeAsyncQueue


class AllowAll(object):
    async def should_put(self, item):
        # Release control back to event loop to simulate more properly an async
        # call.
        await asyncio.sleep(0)

        return True


class AllowSome(object):
    def __init__(self, items):
        self._items = items
        self._index = 0

    async def should_put(self, item):
        await asyncio.sleep(0)

        if self._index >= len(self._items):
            return False

        if item == self._items[self._index]:
            self._index = self._index + 1
            return True

        return False


class TestConfirmPutQueue(aiounittest.AsyncTestCase):

    @staticmethod
    async def _compose_get_task_done(queue):
        item = await queue.get()
        queue.task_done()
        return item

    def get_event_loop(self):
        return asyncio.get_event_loop()

    async def test_allow_all_arbiter(self):
        allow_all = AllowAll()
        queue = []
        fake_queue = FakeAsyncQueue(queue)
        confirm_queue = ConfirmPutQueue(allow_all, fake_queue)

        singular_item = bytearray(b'')
        put_task = asyncio.create_task(confirm_queue.put(singular_item))
        get_task = asyncio.create_task(
            self._compose_get_task_done(confirm_queue))
        _, same_element = await asyncio.gather(put_task, get_task)

        self.assertEqual(same_element, b'')

    async def test_allow_some_elements(self):
        allowed_bytes = [bytes([i]) for i in (1, 3, 5, 7, 9)]
        allowed_bytearrays = [bytearray(i) for i in allowed_bytes]
        allow_some = AllowSome(allowed_bytearrays)
        queue = []
        fake_queue = FakeAsyncQueue(queue)
        confirm_queue = ConfirmPutQueue(allow_some, fake_queue)

        put_tasks = [asyncio.create_task(
            confirm_queue.put(bytearray([i]))) for i in range(10)]

        get_tasks = [asyncio.create_task(
            self._compose_get_task_done(confirm_queue)) for _ in range(5)]

        * results, = await asyncio.gather(* get_tasks, * put_tasks)

        self.assertEqual(results[0:5], allowed_bytes)
