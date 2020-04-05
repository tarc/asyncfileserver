class AskAnswerArbiter(object):
    def __init__(self, input, output, data_view_formatter, confirm_command_parser):
        self._input = input
        self._output = output
        self._continue = False
        self._data_view_formatter = data_view_formatter
        self._confirm_command_parser = confirm_command_parser

    async def should_put(self, item):
        if self._continue:
            return True

        view_item = self._data_view_formatter.format(item)
        await self._output.print(f"\n{view_item}\n> ")
        command = self._confirm_command_parser.parse(await self._input.input())

        self._continue = command.go_on()
        return command.go_on() or command.yes()
