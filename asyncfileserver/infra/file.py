import asyncio
import aiofiles


class File(object):

    def __init__(self, file,
                 read_buffer_size: int = 2048,
                 queue=asyncio.Queue(), queue_item_size: int = 91):
        self._file = file
        self._buffer_size = read_buffer_size
        self._queue = queue
        self._queue_item_size = queue_item_size
        self._buffer_index = 0
        self._buffer = bytearray()

    async def data(self):
        read = asyncio.create_task(self.read())
        item = await self._queue.get()
        while item:
            yield item
            self._queue.task_done()
            item = await self._queue.get()

        self._queue.task_done()
        await read

    async def read(self):
        while await self._read():
            while await self._append():
                pass
            self._buffer = self._buffer[self._buffer_index:]
            self._buffer_index = 0

        if self._remaining_buffer_size() > 0:
            await self._queue.put(self._buffer[self._buffer_index:])

        await self._queue.put(None)

    async def _read(self):
        chunk = await self._file.read(self._buffer_size)
        self._buffer.extend(chunk)
        return chunk

    def _remaining_buffer_size(self):
        return len(self._buffer) - self._buffer_index

    async def _append(self):
        if self._remaining_buffer_size() >= self._queue_item_size:
            end_index = self._buffer_index + self._queue_item_size
            item = bytearray(self._buffer[self._buffer_index:end_index])
            await self._queue.put(item)
            self._buffer_index = self._buffer_index + self._queue_item_size
            return True
        return False
