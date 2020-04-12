class Controller(object):
    def __init__(self, listener, command_queue, read_task):
        self._listener = listener
        self._command_queue = command_queue
        self._read_task = read_task

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
