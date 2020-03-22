import asyncio

async def main():
    pass

if __name__ == "__main__":
    import argparse
    import exitstatus

    parser = argparse.ArgumentParser(description="Start a file server.")

    parser.add_argument("-f", "--file", type=str,
        help="file to be served")

    parser.add_argument("-c", "--ncon", type=int, default=10,
        help="number of consumers")

    args = parser.parse_args()

    asyncio.run(main())
