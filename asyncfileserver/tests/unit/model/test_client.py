import asyncio
import aiounittest
import aioconsole

from asyncfileserver.model.client import Client
from ..infra.buffer_output import BufferOutput


class FixedElementsQueue(object):
    def __init__(self, elements):
        self._elements = elements
        self._index = 0

    async def get(self):
        if self._index >= len(self._elements):
            return None

        element = self._elements[self._index]

        return element

    def task_done(self):
        self._index = self._index + 1

    def how_many_tasks_done(self) -> int:
        return self._index


class TestConsoleClient(aiounittest.AsyncTestCase):

    def get_event_loop(self):
        return asyncio.get_event_loop()

    async def test_simple_output(self):
        singular_element = object()
        queue = FixedElementsQueue([singular_element])

        output_elements = []
        output = BufferOutput(output_elements)

        client = Client(queue, output)

        await client.write()
        self.assertEqual(output_elements[0], singular_element)
        self.assertEqual(queue.how_many_tasks_done(), 2)
