import argparse
import asyncio
import aiofiles
import sys
from aioconsole.stream import create_standard_streams
from exitstatus import ExitStatus
from contextlib import closing, suppress

from asyncfileserver.infra.file import File
from asyncfileserver.infra.async_console_input import AsyncConsoleInput
from asyncfileserver.infra.async_console_output import AsyncConsoleOutput
from asyncfileserver.infra.asyncio_server_factory import ServerFactory
from asyncfileserver.app.ask_answer_arbiter import AskAnswerArbiter as Arbiter
from asyncfileserver.app.controller import Controller
from asyncfileserver.app.client import Client
from asyncfileserver.model.confirm_put_queue import ConfirmPutQueue
from asyncfileserver.model.data_view_formatter import DataViewFormatter
from asyncfileserver.model.confirm_command_parser import ConfirmCommandParser
from asyncfileserver.model.repl_command_parser import REPLCommandParser
from asyncfileserver.model.simple_parser import SimpleParser
from asyncfileserver.model.repl_response_formatter import REPLResponseFormatter
from asyncfileserver.model.exception_formatter import ExceptionFormatter
from asyncfileserver.model.listener import listen


async def start_client(reader, writer):
    pass


class NullInput(object):
    pass


class NullParser(object):
    pass


class IdentityFormatter(object):
    def format(self, item):
        return item


class NullQueue(object):
    pass


async def asyncfileserver(file_name: str,
                          address: str = "0.0.0.0", port: int = 6666) -> int:

    streams = await create_standard_streams(sys.stdin.buffer,
                                            sys.stdout.buffer,
                                            sys.stderr.buffer)
    reader, writer, error = streams
    console_input = AsyncConsoleInput(reader)
    console_output = AsyncConsoleOutput(writer)
    error_output = AsyncConsoleOutput(error)

    server_factory = ServerFactory(address, port, start_client)

    async with listen(server_factory) as listener:
        command_queue = asyncio.Queue()
        read_task = None

        response_queue = asyncio.Queue()

        exception_formatter = ExceptionFormatter()

        controller = Controller(listener, command_queue, read_task,
                                response_queue, exception_formatter,
                                error_output)

        command_parser = SimpleParser(
            [b'O', b'o', b'C', b'c', b'Q', b'q'],
            [
                controller.open_command, controller.open_command,
                controller.close_command, controller.close_command,
                controller.quit_command, controller.quit_command
            ],
            controller.error_command)

        response_formatter = REPLResponseFormatter()

        client = Client(console_input, command_parser, command_queue,
                        response_queue, response_formatter, console_output)

        read_task = asyncio.create_task(client.read())
        write_task = asyncio.create_task(client.write())

        try:
            with suppress(asyncio.CancelledError):
                await asyncio.gather(read_task, write_task, controller.control())
        except Exception as e:
            exception_formatted = exception_formatter.format(e)
            await error_output.print(f"TOP LEVEL EXCEPTION: {exception_formatted}")
            return ExitStatus.failure

    return ExitStatus.success

    async with aiofiles.open(file_name, "rb") as async_file:
        streams = await create_standard_streams(sys.stdin.buffer,
                                                sys.stdout.buffer,
                                                sys.stderr.buffer)
        reader, writer, _ = streams
        input = AsyncConsoleInput(reader)
        output = AsyncConsoleOutput(writer)
        arbiter = Arbiter(input, output, DataViewFormatter(),
                          ConfirmCommandParser())
        queue = ConfirmPutQueue(arbiter, asyncio.Queue())
        file = File(file=async_file, queue=queue)

        client = Client(NullInput(), NullParser(), NullQueue(),
                        queue, IdentityFormatter(), output)

        read_file = asyncio.create_task(file.read())
        write_console = asyncio.create_task(client.write())

        await asyncio.gather(read_file, write_console)

        return ExitStatus.success


def main():

    parser = argparse.ArgumentParser(description="Start a file server.")

    parser.add_argument("-f", "--file", type=str,
                        help="file to be served")

    parser.add_argument("-v", "--version", action='store_true',
                        help="show version")

    args = parser.parse_args()

    if args.version:
        from asyncfileserver import __version__
        print(f"asyncfileserver version {__version__}")
        sys.exit(ExitStatus.success)

    if args.file == None:
        parser.error("the following argument is required: FILE")

    loop = asyncio.get_event_loop()

    try:
        status = loop.run_until_complete(asyncfileserver(args.file))
        sys.exit(status)
    except FileNotFoundError as e:
        parser.error(f'file "{args.file}": not found')
    except TypeError as e:
        parser.error(f'type error: {e}')
    finally:
        loop.close()


if __name__ == "__main__":
    main()
