import asyncio
import aiounittest

from fileserver.infra.file import Repository


class EmptyAsyncFile(object):
    async def read(self, size):
        return b""


class TestFileRepository(aiounittest.AsyncTestCase):

    def get_event_loop(self):
        return asyncio.get_event_loop()

    async def test_empty_file(self):
        repository = Repository(EmptyAsyncFile())

        data = repository.data()

        with self.assertRaises(StopAsyncIteration):
            await data.__anext__()
