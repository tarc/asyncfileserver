import asyncio
import aiounittest
import aioconsole

from fileserver.infra.console import Client


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
        element = self._elements[self._index]
        self._index = self._index + 1
        return element


class TestFile(aiounittest.AsyncTestCase):

    def get_event_loop(self):
        return asyncio.get_event_loop()

    async def test_simple_output(self):
        single_element = object()
        queue = FixedElementsQueue([single_element])

        output_elements = []
        output = BufferOutput(output_elements)

        client = Client(queue, output)

        await client.write()
        self.assertEqual(output.buffer[0], single_element)
