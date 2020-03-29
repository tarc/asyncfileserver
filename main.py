import asyncio
import aiofiles
from exitstatus import ExitStatus

from fileserver.infra.file import File
from fileserver.infra.console import Client


async def main(file_name: str) -> int:
    async with aiofiles.open(file_name, "rb") as async_file:
        queue = asyncio.Queue()
        file = File(file=async_file, queue=queue)
        client = Client(queue)

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

    parser.add_argument("-c", "--ncon", type=int, default=10,
                        help="number of consumers")

    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    try:
        status = loop.run_until_complete(main(args.file))
    except FileNotFoundError as e:
        print(f'main.py: error: file "{args.file}": not found')
        sys.exit(ExitStatus.failure)
    finally:
        loop.close()

    sys.exit(status)
