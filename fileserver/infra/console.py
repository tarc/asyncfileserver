class Client(object):
    def __init__(self, queue, writing_buffer_size: int = 17):
        self._queue = queue
        self._buffer_size = writing_buffer_size

    async def write(self):
        pass