import asyncio

from asyncfileserver.model.buffer import Buffer


class Client(object):
    def __init__(self,
                 input, command_parser, command_queue,
                 response_queue, response_formatter, output):
        self._input = input
        self._command_parser = command_parser
        self._command_queue = command_queue
        self._response_queue = response_queue
        self._response_formatter = response_formatter
        self._output = output
        self._read_buffer = Buffer()
        self._pending_read = None

    async def _update_pending_read(self, coro):
        previous_pending_read = self._pending_read
        self._pending_read = asyncio.create_task(coro)
        result = await self._pending_read
        self._pending_read = previous_pending_read
        return result

    async def read(self):
        command_data = await self._update_pending_read(self._input.input())

        while command_data:
            self._read_buffer.extend(command_data)

            command, size = self._command_parser.parse(self._read_buffer.get())

            while size > 0:
                if command != None:
                    await self._update_pending_read(self._command_queue.put(command))

                self._read_buffer.advance(size)
                command, size = self._command_parser.parse(
                    self._read_buffer.get())

            command_data = await self._update_pending_read(self._input.input())

        await self._update_pending_read(self._command_queue.put(None))

    def cancel_pending_read(self):
        if self._pending_read != None and not self._pending_read.done():
            self._pending_read.cancel()

    async def write(self):
        data = await self._response_queue.get()
        while data != None:
            response = self._response_formatter.format(data)
            await self._output.print(response)
            self._response_queue.task_done()

            data = await self._response_queue.get()

        self._response_queue.task_done()

