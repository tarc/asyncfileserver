from asyncfileserver.model.view_data import ViewData
from asyncfileserver.model.confirm_command import ConfirmCommand


class Arbiter(object):
    def __init__(self, input, output):
        self._input = input
        self._output = output
        self._continue = False

    async def should_put(self, item):
        if self._continue:
            return True

        view_item = ViewData(item)
        await self._output.print(f"\n{view_item}\n> ")
        command = ConfirmCommand(await self._input.input())

        self._continue = command.go_on()
        return command.go_on() or command.yes()
