import asyncio
import aiounittest

from asyncfileserver.model.simple_queue import SimpleQueue
from ..model.fake_async_queue import FakeAsyncQueue


class TestSimpleQueue(aiounittest.AsyncTestCase):

    @staticmethod
    async def _compose_get_task_done(queue):
        item = await queue.get()
        queue.task_done()
        return item

    def get_event_loop(self):
        return asyncio.get_event_loop()

    async def test_single_empty_bytearray(self):
        queue = []
        fake_queue = FakeAsyncQueue(queue)
        confirm_queue = SimpleQueue(fake_queue)

        singular_item = bytearray(b'')
        put_task = asyncio.create_task(confirm_queue.put(singular_item))
        get_task = asyncio.create_task(
            self._compose_get_task_done(confirm_queue))
        _, same_element = await asyncio.gather(put_task, get_task)

        self.assertEqual(same_element, b'')

    async def test_get_and_put_simultaneously(self):
        queue = []
        fake_queue = FakeAsyncQueue(queue)
        confirm_queue = SimpleQueue(fake_queue)

        put_tasks = [asyncio.create_task(
            confirm_queue.put(bytearray([i]))) for i in range(10)]

        get_tasks = [asyncio.create_task(
            self._compose_get_task_done(confirm_queue)) for _ in range(10)]

        * results, = await asyncio.gather(* get_tasks, * put_tasks)

        self.assertEqual(results[0:len(get_tasks)], queue)
