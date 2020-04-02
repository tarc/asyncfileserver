import asyncio
import aiofiles
from aioconsole.stream import create_standard_streams
from exitstatus import ExitStatus

from asyncfileserver import __version__

from asyncfileserver.infra.file import File
from asyncfileserver.model.client import Client
from asyncfileserver.infra.async_console_input import AsyncConsoleInput
from asyncfileserver.infra.async_console_output import AsyncConsoleOutput
from asyncfileserver.model.ask_answer_arbiter import AskAnswerArbiter as Arbiter
from asyncfileserver.model.confirm_put_queue import ConfirmPutQueue
from asyncfileserver.model.view_data_factory import ViewDataFactory
from asyncfileserver.model.confirm_command_factory import ConfirmCommandFactory


async def main(file_name: str) -> int:
    async with aiofiles.open(file_name, "rb") as async_file:
        streams = await create_standard_streams(sys.stdin.buffer,
                                                sys.stdout.buffer,
                                                sys.stderr.buffer)
        reader, writer, _ = streams
        input = AsyncConsoleInput(reader)
        output = AsyncConsoleOutput(writer)
        arbiter = Arbiter(input, output, ViewDataFactory(),
            ConfirmCommandFactory())
        queue = ConfirmPutQueue(arbiter, asyncio.Queue())
        file = File(file=async_file, queue=queue)

        client = Client(queue, output)

        read_file = asyncio.create_task(file.read())
        write_console = asyncio.create_task(client.write())

        await asyncio.gather(read_file, write_console)

        return ExitStatus.success

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Start a file server.")

    parser.add_argument("-f", "--file", type=str, help="file to be served")

    parser.add_argument("-v", "--version",
                        action='store_true', help="show version")

    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit(ExitStatus.success)

    loop = asyncio.get_event_loop()

    try:
        status = loop.run_until_complete(main(args.file))
    except FileNotFoundError as e:
        print(f'main.py: error: file "{args.file}": not found', file=sys.stderr)
        sys.exit(ExitStatus.failure)
    except TypeError as e:
        print(f'main.py: error: type error: {e}', file=sys.stderr)
        sys.exit(ExitStatus.failure)
    finally:
        loop.close()

    sys.exit(status)
