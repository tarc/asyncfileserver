import asyncio
import aiounittest

from asyncfileserver.infra.console_arbiter import Arbiter
from .buffer_output import BufferOutput
from .queue_input import QueueInput


class TestConsoleArbiter(aiounittest.AsyncTestCase):

    def get_event_loop(self):
        return asyncio.get_event_loop()

    async def test_simple_inquire_response(self):
        output_buffer = []
        output = BufferOutput(output_buffer)
        input_queue = [b'Y\n']
        input = QueueInput(input_queue)
        arbiter = Arbiter(input, output)

        singular_object = object()

        self.assertTrue(await arbiter.should_put(singular_object))
        self.assertEqual(output_buffer, [singular_object])

    async def test_deny_and_allow(self):
        output_buffer = []
        output = BufferOutput(output_buffer)
        input_queue = [b'N\n', b'Y\n']
        input = QueueInput(input_queue)
        arbiter = Arbiter(input, output)

        first_element = object()
        second_element = object()

        self.assertFalse(await arbiter.should_put(first_element))
        self.assertEqual(output_buffer, [first_element])

        self.assertTrue(await arbiter.should_put(second_element))
        self.assertEqual(output_buffer, [first_element, second_element])