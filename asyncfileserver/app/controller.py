import asyncio
from asyncfileserver.model.command_token import CommandToken


class Controller(object):


    def __init__(self, listener, command_queue, client, response_queue,
                 exception_formatter, error_output):
        self._listener = listener
        self._command_queue = command_queue
        self._client = client
        self._response_queue = response_queue
        self._exception_formatter = exception_formatter
        self._error_output = error_output

        self._tokenToCommand = {
            CommandToken.Open: self.open_command,
            CommandToken.Close: self.close_command,
            CommandToken.Quit: self.quit_command,
            CommandToken.Error: self.error_command
        }

    async def open_command(self, data):
        await self._listener.listen()
        return "Finished starting."

    async def close_command(self, data):
        await self._listener.stop()
        return "Finished stopping."

    async def quit_command(self, data):
        await self._command_queue.put(None)
        self._client.cancel_pending_read()

        return "Quit"

    async def error_command(self, data):
        return "Error"

    async def control(self):
        command = await self._command_queue.get()
        while command != None:
            token, argument = command
            function = self._tokenToCommand[token]
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
