import asyncio
import aiofiles
from aioconsole.stream import create_standard_streams
from exitstatus import ExitStatus

from fileserver.infra.file import File
from fileserver.infra.console import Client
from fileserver.infra.async_console_output import AsyncConsoleOutput
from fileserver.model.simple_queue import SimpleQueue


async def main(file_name: str) -> int:
    async with aiofiles.open(file_name, "rb") as async_file:
        queue = SimpleQueue(asyncio.Queue())
        file = File(file=async_file, queue=queue)

        streams = await create_standard_streams(sys.stdin.buffer,
                                                sys.stdout.buffer,
                                                sys.stderr.buffer)
        _, writer, _ = streams
        output = AsyncConsoleOutput(writer)
        client = Client(queue, output)

        read_file = asyncio.create_task(file.read())
        write_console = asyncio.create_task(client.write())

        await asyncio.gather(read_file, write_console)

        return ExitStatus.success

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Start a file server.")

    parser.add_argument("-f", "--file", type=str, required=True,
                        help="file to be served")

    args = parser.parse_args()

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
