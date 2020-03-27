import asyncio
import aiofiles

from fileserver.infra.file import Repository


async def main(file_name: str) -> int:
    async with aiofiles.open(file_name, "rb") as async_file:
        repository = Repository(async_file)

        count = 0
        async for data in repository.data():
            count = count + len(data)

        return count

if __name__ == "__main__":
    import argparse
    import exitstatus

    parser = argparse.ArgumentParser(description="Start a file server.")

    parser.add_argument("-f", "--file", type=str, required=True,
                        help="file to be served")

    parser.add_argument("-c", "--ncon", type=int, default=10,
                        help="number of consumers")

    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    try:
        count = loop.run_until_complete(main(args.file))
    finally:
        loop.close()

    print(count)