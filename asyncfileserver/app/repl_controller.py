import asyncio


class Controller(object):
    def __init__(self,
                 input, command_parser,
                 output, response_formatter,
                 error, exception_formatter,
                 start_command, stop_command, quit_command, error_command):
        self._input = input
        self._command_parser = command_parser
        self._output = output
        self._response_formatter = response_formatter
        self._error_output = error
        self._exception_formatter = exception_formatter
        self._start = start_command
        self._stop = stop_command
        self._quit = quit_command
        self._error = error_command

    async def control(self):
        command_data = await self._input.input()
        command_tag = self._command_parser.parse(command_data)

        while command_tag:
            command_task = asyncio.create_task(self._invoke(command_tag))
            response_task = asyncio.create_task(self._respond(command_task))

            command_data = await self._input.input()
            command_tag = self._command_parser.parse(command_data)

    async def _invoke(self, command_tag):
        if command_tag.start():
            return await self._start()
        elif command_tag.stop():
            return await self._stop()
        elif command_tag.quit():
            return await self._quit()
        elif command_tag.error():
            return await self._error()

    async def _respond(self, command_task):
        data = None
        try:
            data = await command_task
        except Exception as e:
            error = self._exception_formatter.format(e)
            await self._error_output.print(error)

        response = self._response_formatter.format(data)
        await self._output.print(response)
