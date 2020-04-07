import re
from asyncfileserver.model.confirm_command import ConfirmCommand


class ConfirmCommandParser(object):
    def __init__(self):
        self._command = None

    _non_command_pattern = re.compile(b'([^CcYy]|[CcYy]\w)')
    _command_pattern = re.compile(b'[CcYy]\W')
    _up_to_eol_pattern = re.compile(b'[^\n]*')
    _eol_pattern = re.compile(b'\n')

    def parse(self, data):
        if self._command != None:
            return self._consume_up_to_eol(data)

        m = re.match(self._non_command_pattern, data)
        if m != None:
            self._command = ConfirmCommand(data[:m.end()], True)
            return self._consume_up_to_eol(data, m.end()-1)

        m = re.match(self._command_pattern, data)
        if m != None:
            self._command = ConfirmCommand(data[:m.end()-1])
            return self._consume_up_to_eol(data, m.end()-1)

        return None, 0

    def _consume_up_to_eol(self, data, index=0):
        up_to_eol_match = self._up_to_eol_pattern.match(data, index)

        assert(up_to_eol_match != None)

        index = up_to_eol_match.end()
        eol_match = self._eol_pattern.match(data, index)

        if eol_match != None:
            index = eol_match.end()
            command = self._command
            self._command = None
            return command, index

        return None, index
