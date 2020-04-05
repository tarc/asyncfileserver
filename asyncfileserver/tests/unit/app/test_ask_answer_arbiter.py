import asyncio
import aiounittest

from asyncfileserver.app.ask_answer_arbiter import AskAnswerArbiter
from asyncfileserver.tests.unit.infra.buffer_output import BufferOutput
from asyncfileserver.tests.unit.infra.queue_input import QueueInput


class DataViewMock(object):
    def __init__(self, representation):
        self._representation = representation

    def __str__(self):
        return self._representation


class ConfirmCommandMock(object):
    def __init__(self, go_on, yes):
        self._go_on = go_on
        self._yes = yes

    def go_on(self):
        return self._go_on

    def yes(self):
        return self._yes


class ParserMock(object):
    def __init__(self, instances):
        self._instances = instances
        self._index = 0

    def parse(self, data: bytearray):
        instance = self._instances[self._index]
        self._index = self._index + 1
        return instance


class FormatterMock(object):
    def __init__(self, instances):
        self._instances = instances
        self._index = 0

    def format(self, data: bytearray):
        instance = self._instances[self._index]
        self._index = self._index + 1
        return instance


class TestConsoleArbiter(aiounittest.AsyncTestCase):

    def get_event_loop(self):
        return asyncio.get_event_loop()

    async def test_simple_inquire_response(self):
        output_buffer = []
        output = BufferOutput(output_buffer)

        input_buffer = [object()]
        input_queue = QueueInput(input_buffer)

        view = DataViewMock("DATA")
        command = ConfirmCommandMock(False, True)

        arbiter = AskAnswerArbiter(input_queue, output,
                                   FormatterMock([view]),
                                   ParserMock([command]))

        singular_object = object()

        self.assertTrue(await arbiter.should_put(singular_object))
        self.assertEqual(output_buffer, [f"\n{view}\n> "])

    async def test_deny_and_allow(self):
        input_buffer = [object(), object(), object(), object()]
        input_queue = QueueInput(input_buffer)

        output_buffer = []
        output = BufferOutput(output_buffer)

        view1 = DataViewMock("DATA1")
        view2 = DataViewMock("DATA2")
        view3 = DataViewMock("DATA3")
        view4 = DataViewMock("DATA4")

        command1 = ConfirmCommandMock(False, False)
        command2 = ConfirmCommandMock(False, True)
        command3 = ConfirmCommandMock(True, False)
        command4 = ConfirmCommandMock(False, False)

        arbiter = AskAnswerArbiter(input_queue, output,
                                   FormatterMock([view1, view2, view3, view4]),
                                   ParserMock([command1, command2, command3,
                                               command4]))

        singular_object1 = object()
        singular_object2 = object()
        singular_object3 = object()
        singular_object4 = object()

        self.assertFalse(await arbiter.should_put(singular_object1))
        self.assertEqual(output_buffer, [f"\n{view1}\n> "])

        self.assertTrue(await arbiter.should_put(singular_object2))
        self.assertEqual(output_buffer, [f"\n{view1}\n> ", f"\n{view2}\n> "])

        self.assertTrue(await arbiter.should_put(singular_object3))
        self.assertEqual(output_buffer,
                         [f"\n{view1}\n> ", f"\n{view2}\n> ", f"\n{view3}\n> "])

        self.assertTrue(await arbiter.should_put(singular_object4))
        self.assertEqual(output_buffer,
                         [f"\n{view1}\n> ", f"\n{view2}\n> ", f"\n{view3}\n> "])
