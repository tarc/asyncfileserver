import asyncio


class Controller(object):
    def __init__(self, listener, command_queue, read_task, response_queue,
                 exception_formatter, error_output):
        self._listener = listener
        self._command_queue = command_queue
        self._read_task = read_task
        self._response_queue = response_queue
        self._exception_formatter = exception_formatter
        self._error_output = error_output

    async def open_command(self, data):
        await self._listener.listen()
        return "Finished starting."

    async def close_command(self, data):
        await self._listener.stop()
        return "Finished stopping."

    async def quit_command(self, data):
        await self._command_queue.put(None)
        if self._read_task != None:
            self._read_task.cancel()

        return "Quit"

    async def error_command(self, data):
        return "Error"

    async def control(self):
        command = await self._command_queue.get()
        while command != None:
            function, argument = command
            command_task = asyncio.create_task(function(argument))
            response_task = asyncio.create_task(self._respond(command_task))

            command = await self._command_queue.get()

        await self._response_queue.put(None)

    async def _respond(self, command_task):
        try:
            response_data = await command_task
            await self._response_queue.put(response_data)
        except Exception as e:
            formatted_exception = self._exception_formatter.format(e)
            asyncio.create_task(self._error_output.print(formatted_exception))
