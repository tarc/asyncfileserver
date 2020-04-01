import asyncio
import aiounittest

from asyncfileserver.infra.async_console_input import AsyncConsoleInput


class MockReader(object):
    def __init__(self, lines):
        self._lines = lines
        self._index = 0

    async def readline(self):
        await asyncio.sleep(0)

        if self._index >= len(self._lines):
            return b''

        item = self._lines[self._index]
        self._index = self._index + 1
        return item


class TestAsyncConsoleInput(aiounittest.AsyncTestCase):

    def get_event_loop(self):
        return asyncio.get_event_loop()

    async def test_read_line_input(self):
        singular_object = object()
        lines = [singular_object]
        reader = MockReader(lines)
        console = AsyncConsoleInput(reader)

        self.assertEqual(await console.input(), singular_object)
        self.assertEqual(await console.input(), b'')
