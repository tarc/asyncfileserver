import asyncio
import aiounittest

from asyncfileserver.infra.file import File
from asyncfileserver.tests.unit.model.fake_async_queue import FakeAsyncQueue


class ByteArrayFile(object):
    def __init__(self, buffer: bytearray):
        self._buffer = buffer
        self._index = 0

    async def read(self, size):
        read_size = min(size, len(self._buffer[self._index:]))
        end_index = self._index + read_size
        data = self._buffer[self._index:end_index]
        self._index = self._index + read_size
        return data


class TestFile(aiounittest.AsyncTestCase):

    def get_event_loop(self):
        return asyncio.get_event_loop()

    async def test_empty_file(self):
        queue = []
        async_queue = FakeAsyncQueue(queue)
        file = File(ByteArrayFile(bytearray(b"")), queue = async_queue)

        data = file.data()

        with self.assertRaises(StopAsyncIteration):
            await data.__anext__()

    async def test_read_buffer_size_lt_file_size_lt_queue_item_size(self):
        queue = []
        async_queue = FakeAsyncQueue(queue)
        file = File(ByteArrayFile(bytearray(b"\x01\x02\x03\x04\x05")),
                    queue=async_queue,
                    read_buffer_size=1, queue_item_size=6)
        items = []
        async for item in file.data():
            items.append(item)

        self.assertTrue(items == [bytearray(b"\x01\x02\x03\x04\x05")])

    async def test_read_buffer_size_lt_file_size_eq_queue_item_size(self):
        queue = []
        async_queue = FakeAsyncQueue(queue)
        file = File(ByteArrayFile(bytearray(b"\x01\x02\x03\x04\x05")),
                    queue=async_queue,
                    read_buffer_size=1, queue_item_size=5)
        items = []
        async for item in file.data():
            items.append(item)

        self.assertTrue(items == [bytearray(b"\x01\x02\x03\x04\x05")])

    async def test_read_buffer_size_lt_file_size_gt_queue_item_size(self):
        queue = []
        async_queue = FakeAsyncQueue(queue)
        file = File(ByteArrayFile(bytearray(b"\x01\x02\x03\x04\x05")),
                    queue=async_queue,
                    read_buffer_size=1, queue_item_size=4)
        result = [
            bytearray(b"\x01\x02\x03\x04"),
            bytearray(b"\x05")
        ]

        items = []

        async for item in file.data():
            items.append(item)

        self.assertTrue(items == result)

    async def test_read_buffer_size_eq_queue_item_size_lt_file_size(self):
        queue = []
        async_queue = FakeAsyncQueue(queue)
        file = File(ByteArrayFile(bytearray(b"\x01\x02\x03\x04\x05")),
                    queue=async_queue,
                    read_buffer_size=1, queue_item_size=1)
        result = [bytearray([i+1]) for i in range(5)]

        items = []

        async for item in file.data():
            items.append(item)

        self.assertTrue(items == result)

    async def test_file_size_lt_read_buffer_size_lt_queue_item_size(self):
        queue = []
        async_queue = FakeAsyncQueue(queue)
        file = File(ByteArrayFile(bytearray(b"\x01\x02\x03\x04\x05")),
                    queue=async_queue,
                    read_buffer_size=6, queue_item_size=7)
        items = []
        async for item in file.data():
            items.append(item)

        self.assertTrue(items == [bytearray(b"\x01\x02\x03\x04\x05")])

    async def test_file_size_lt_read_buffer_size_eq_queue_item_size(self):
        queue = []
        async_queue = FakeAsyncQueue(queue)
        file = File(ByteArrayFile(bytearray(b"\x01\x02\x03\x04\x05")),
                    queue=async_queue,
                    read_buffer_size=6, queue_item_size=6)
        items = []
        async for item in file.data():
            items.append(item)

        self.assertTrue(items == [bytearray(b"\x01\x02\x03\x04\x05")])

    async def test_file_size_lt_queue_item_size_lt_read_buffer_size(self):
        queue = []
        async_queue = FakeAsyncQueue(queue)
        file = File(ByteArrayFile(bytearray(b"\x01\x02\x03\x04\x05")),
                    queue=async_queue,
                    read_buffer_size=7, queue_item_size=6)
        items = []
        async for item in file.data():
            items.append(item)

        self.assertTrue(items == [bytearray(b"\x01\x02\x03\x04\x05")])

    async def test_file_size_eq_queue_item_size_lt_read_buffer_size(self):
        queue = []
        async_queue = FakeAsyncQueue(queue)
        file = File(ByteArrayFile(bytearray(b"\x01\x02\x03\x04\x05")),
                    queue=async_queue,
                    read_buffer_size=6, queue_item_size=5)
        items = []
        async for item in file.data():
            items.append(item)

        self.assertTrue(items == [bytearray(b"\x01\x02\x03\x04\x05")])

    async def test_queue_item_size_lt_file_size_lt_read_buffer_size(self):
        queue = []
        async_queue = FakeAsyncQueue(queue)
        file = File(ByteArrayFile(bytearray(b"\x01\x02\x03\x04\x05")),
                    queue=async_queue,
                    read_buffer_size=4, queue_item_size=1)
        result = [bytearray([i+1]) for i in range(5)]
        items = []
        async for item in file.data():
            items.append(item)

        self.assertTrue(items == result)

    async def test_queue_item_size_lt_file_size_eq_read_buffer_size(self):
        queue = []
        async_queue = FakeAsyncQueue(queue)
        file = File(ByteArrayFile(bytearray(b"\x01\x02\x03\x04\x05")),
                    queue=async_queue,
                    read_buffer_size=5, queue_item_size=1)
        result = [bytearray([i+1]) for i in range(5)]
        items = []
        async for item in file.data():
            items.append(item)

        self.assertTrue(items == result)

    async def test_queue_item_size_lt_read_buffer_size_lt_file_size(self):
        queue = []
        async_queue = FakeAsyncQueue(queue)
        file = File(ByteArrayFile(bytearray(b"\x01\x02\x03\x04\x05")),
                    queue=async_queue,
                    read_buffer_size=4, queue_item_size=1)
        result = [bytearray([i+1]) for i in range(5)]
        items = []
        async for item in file.data():
            items.append(item)

        self.assertTrue(items == result)

    async def test_queue_item_size_eq_read_buffer_size_lt_file_size(self):
        queue = []
        async_queue = FakeAsyncQueue(queue)
        file = File(ByteArrayFile(bytearray(b"\x01\x02\x03\x04\x05")),
                    queue=async_queue,
                    read_buffer_size=1, queue_item_size=1)
        result = [bytearray([i+1]) for i in range(5)]
        items = []
        async for item in file.data():
            items.append(item)

        self.assertTrue(items == result)

    async def test_read_without_consuming_queue(self):
        queue = []
        async_queue = FakeAsyncQueue(queue)
        file = File(ByteArrayFile(bytearray(b"\x01\x02\x03\x04\x05")),
                    queue=async_queue,
                    read_buffer_size=1, queue_item_size=1)

        result = [bytearray([i+1]) for i in range(5)]
        result.extend([None, None])

        await file.read()
        self.assertEqual(async_queue.how_many_tasks_done(), 0)

        async for item in file.data():
            pass
        self.assertEqual(async_queue.how_many_tasks_done(), 6)

        self.assertEqual(queue, result)
