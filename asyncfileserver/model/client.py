from asyncfileserver.model.buffer import Buffer


class Client(object):
    def __init__(self,
                 input, parser, command_queue,
                 response_queue, formatter, output,
                 read_buffer=Buffer()):
        self._input = input
        self._parser = parser
        self._command_queue = command_queue
        self._response_queue = response_queue
        self._formatter = formatter
        self._output = output

        self._read_buffer = read_buffer

    async def read(self):
        data = await self._input.read()
        while data:
            self._read_buffer.extend(data)
            command = self._command_parser.parse(self._read_buffer)
            while command:
                await self._command_queue.put(command)
                command = self._command_parser.parse(self._read_buffer)

            data = await self._input.read()

    async def write(self):
        item = await self._response_queue.get()
        data = self._formatter.format(item)
        while(data):
            await self._output.print(data)
            self._response_queue.task_done()
            item = await self._response_queue.get()
            data = self._formatter.format(item)

        self._response_queue.task_done()
