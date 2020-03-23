import asyncio
import aiofiles

from fileserver.infra.file import File


async def main(file_name: str) -> None:
    async with aiofiles.open(file_name, "rb") as async_file:
        file = File(async_file)

if __name__ == "__main__":
    import argparse
    import exitstatus

    parser = argparse.ArgumentParser(description="Start a file server.")

    parser.add_argument("-f", "--file", type=str, required=True,
                        help="file to be served")

    parser.add_argument("-c", "--ncon", type=int, default=10,
                        help="number of consumers")

    args = parser.parse_args()

    asyncio.run(main(args.file))
