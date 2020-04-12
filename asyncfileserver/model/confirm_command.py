class ConfirmCommand(object):

    def __init__(self, command: bytes, error: bool = False):
        self._command = command.upper()
        self._error = error

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def go_on(self):
        return self._command == b"C"

    def yes(self):
        return self._command == b"Y"

    def error(self):
        return self._error
