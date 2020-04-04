class AskAnswerArbiter(object):
    def __init__(self, input, output, view_data_factory, confirm_command_factory):
        self._input = input
        self._output = output
        self._continue = False
        self._view_data_factory = view_data_factory
        self._confirm_command_factory = confirm_command_factory

    async def should_put(self, item):
        if self._continue:
            return True

        view_item = self._view_data_factory.create(item)
        await self._output.print(f"\n{view_item}\n> ")
        command = self._confirm_command_factory.create(await self._input.input())

        self._continue = command.go_on()
        return command.go_on() or command.yes()
