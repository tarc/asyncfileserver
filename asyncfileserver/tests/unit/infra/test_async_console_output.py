import asyncio
import aiounittest
import uuid
import os

from asyncfileserver.infra.async_console_output import AsyncConsoleOutput


class MockWriter(object):
    def __init__(self, buffer):
        self._buffer = buffer

    def write(self, msg):
        self._buffer.append(msg)

    async def drain(self):
        await asyncio.sleep(0)


class Custom(object):
    def __init__(self, string):
        self._str = string

    def __str__(self):
        return self._str


class TestAsyncConsoleInput(aiounittest.AsyncTestCase):

    def get_event_loop(self):
        return asyncio.get_event_loop()

    async def test_print_object(self):
        lines = []
        writer = MockWriter(lines)
        console = AsyncConsoleOutput(writer)

        singular_object = object()
        await console.print(singular_object)
        self.assertEqual(lines, [str(singular_object)])

    async def test_print_custom_class(self):
        lines = []
        writer = MockWriter(lines)
        console = AsyncConsoleOutput(writer)

        unique_identifier = uuid.uuid4()
        singular_custom = Custom(str(unique_identifier))
        await console.print(singular_custom)
        self.assertEqual(lines, [str(unique_identifier)])

    async def test_print_bytearray(self):
        lines = []
        writer = MockWriter(lines)
        console = AsyncConsoleOutput(writer)

        random_bytes = os.urandom(10)
        singular_bytearray = bytearray(random_bytes)
        await console.print(singular_bytearray)
        self.assertEqual(lines, [bytearray(random_bytes)])

    async def test_print_str(self):
        lines = []
        writer = MockWriter(lines)
        console = AsyncConsoleOutput(writer)

        unique_identifier = uuid.uuid4()
        singular_str = str(unique_identifier)
        await console.print(singular_str)
        self.assertEqual(lines, [str(unique_identifier)])

    async def test_print_bytes(self):
        lines = []
        writer = MockWriter(lines)
        console = AsyncConsoleOutput(writer)

        random_bytes = os.urandom(10)
        singular_bytes = bytes(random_bytes)
        await console.print(singular_bytes)
        self.assertEqual(lines, [random_bytes])
