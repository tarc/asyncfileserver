import asyncio
import aiounittest
import aioconsole
import os

from asyncfileserver.model.client import Client
from ..infra.buffer_output import BufferOutput
from ..infra.queue_input import QueueInput
from .fake_async_queue import FakeAsyncQueue


class NullInput(object):
    async def input(self):
        return None


class NullOutput(object):
    async def print(self):
        return None


class NullParser(object):
    pass


class IdentityFormatter(object):
    def format(self, item):
        return item


class IdentityParser(object):
    def parse(self, item):
        return item, len(item)


class NullFormatter(object):
    def format(self, item):
        pass


class NullQueue(object):
    async def get(self):
        pass

    async def put(self, elem):
        pass

    def task_done(self):
        pass


class TestConsoleClient(aiounittest.AsyncTestCase):

    def get_event_loop(self):
        return asyncio.get_event_loop()

    async def test_simple_empty_output_queue(self):
        queue = FakeAsyncQueue([None])

        output_elements = []
        output = BufferOutput(output_elements)

        client = Client(NullInput(), NullParser(), NullQueue(),
                        queue, IdentityFormatter(), output)

        await asyncio.gather(client.write(), client.read())
        self.assertEqual(output_elements, [])
        self.assertEqual(queue.how_many_tasks_done(), 1)

    async def test_simple_output(self):
        singular_element = object()
        queue = FakeAsyncQueue([singular_element, None])

        output_elements = []
        output = BufferOutput(output_elements)

        client = Client(NullInput(), NullParser(), NullQueue(),
                        queue, IdentityFormatter(), output)

        await asyncio.gather(client.write(), client.read())
        self.assertEqual(output_elements[0], singular_element)
        self.assertEqual(queue.how_many_tasks_done(), 2)

    async def test_many_elements_output(self):
        queue = [bytearray(os.urandom(10)) for _ in range(20)]
        queue.append(None)
        response_queue = FakeAsyncQueue(queue)

        output_elements = []
        output = BufferOutput(output_elements)

        client = Client(NullInput(), NullParser(), NullQueue(),
                        response_queue, IdentityFormatter(), output)

        await asyncio.gather(client.write(), client.read())
        self.assertEqual(queue, output_elements + [None])
        self.assertEqual(response_queue.how_many_tasks_done(), len(queue))

    async def test_empty_input(self):
        input_list = []
        input = QueueInput(input_list)

        queue = []
        async_queue = FakeAsyncQueue(queue)

        client = Client(input, IdentityParser(), async_queue,
                        NullQueue(), NullFormatter(), NullOutput())

        await asyncio.gather(client.write(), client.read())
        self.assertEqual(queue, input_list + [None])


    async def test_many_elements_input(self):
        input_list = [bytearray(os.urandom(10)) for _ in range(10)]
        input = QueueInput(input_list)

        queue = []
        async_queue = FakeAsyncQueue(queue)

        client = Client(input, IdentityParser(), async_queue,
                        NullQueue(), NullFormatter(), NullOutput())

        await asyncio.gather(client.write(), client.read())
        self.assertEqual(queue, input_list + [None])
