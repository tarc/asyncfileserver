class Arbiter(object):
    def __init__(self, input, output):
        self._input = input
        self._output = output

    async def should_put(self, item):
        await self._output.print(item)
        command = await self._input.input()
        return command == b"Y\n"
