import asyncio
import aiounittest

from asyncfileserver.infra.async_console_output import AsyncConsoleOutput


class MockWriter(object):
    def __init__(self, buffer):
        self._buffer = buffer

    def write(self, msg):
        self._buffer.append(msg)

    async def drain(self):
        await asyncio.sleep(0)


class TestAsyncConsoleInput(aiounittest.AsyncTestCase):

    def get_event_loop(self):
        return asyncio.get_event_loop()

    async def test_write_line_output(self):
        lines = []
        writer = MockWriter(lines)
        console = AsyncConsoleOutput(writer)

        singular_object = object()
        await console.print(singular_object)
        self.assertEqual(lines, [singular_object])
