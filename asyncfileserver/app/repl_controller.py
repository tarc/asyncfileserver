import asyncio

from asyncfileserver.model.buffer import Buffer


class Controller(object):
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

    async def read(self):
        command_data = await self._input.input()

        while command_data:
            self._read_buffer.extend(command_data)

            command, size = self._command_parser.parse(self._read_buffer.get())

            while size > 0:
                if command != None:
                    await self._command_queue.put(command)

                self._read_buffer.advance(size)
                command, size = self._command_parser.parse(
                    self._read_buffer.get())

            command_data = await self._input.input()

        await self._command_queue.put(None)

    async def write(self):
        data = await self._response_queue.get()
        while data != None:
            response = self._response_formatter.format(data)
            await self._output.print(response)

            data = await self._response_queue.get()
