from asyncfileserver.model.view_data import ViewData


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
        command = await self._input.input()
        self._continue = command == b"C\n"
        return self._continue or command == b"Y\n"
