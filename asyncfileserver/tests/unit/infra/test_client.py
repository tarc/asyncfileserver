import asyncio
import aiounittest
import aioconsole

from asyncfileserver.infra.console import Client


class BufferOutput(object):
    def __init__(self, buffer: list):
        self._buffer = buffer

    async def print(self, data):
        self._buffer.append(data)


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


class TestFile(aiounittest.AsyncTestCase):

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
