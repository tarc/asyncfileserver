import asyncio
import aiounittest

from asyncfileserver.model.confirm_put_queue import ConfirmPutQueue


class AllowAll(object):
    async def process(self, item):
        return True


class TestConfirmPutQueue(aiounittest.AsyncTestCase):

    def get_event_loop(self):
        return asyncio.get_event_loop()

    async def test_allow_all_arbiter(self):
        allow_all = AllowAll()
        confirm_queue = ConfirmPutQueue(allow_all)

        singular_item = bytearray(b'')
        await confirm_queue.put(singular_item)
        same_element = await confirm_queue.get()

        self.assertEqual(same_element, b'')
