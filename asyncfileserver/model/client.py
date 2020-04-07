from asyncfileserver.model.buffer import Buffer


class Client(object):
    def __init__(self,
                 input, command_parser, command_queue,
                 response_queue, response_formatter, output,
                 read_buffer=Buffer()):
        self._input = input
        self._command_parser = command_parser
        self._command_queue = command_queue
        self._response_queue = response_queue
        self._response_formatter = response_formatter
        self._output = output

        self._read_buffer = read_buffer

    async def read(self):
        data = await self._input.input()
        while data:
            self._read_buffer.extend(data)
            command, size = self._command_parser.parse(self._read_buffer.get())
            while size > 0:
                if command != None:
                    await self._command_queue.put(command)
                self._read_buffer.advance(size)
                command, size = self._command_parser.parse(
                    self._read_buffer.get())

            data = await self._input.input()

        await self._command_queue.put(None)

    async def write(self):
        item = await self._response_queue.get()
        data = self._response_formatter.format(item)
        while(data):
            await self._output.print(data)
            self._response_queue.task_done()
            item = await self._response_queue.get()
            data = self._response_formatter.format(item)

        self._response_queue.task_done()
