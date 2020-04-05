from asyncfileserver.model.confirm_command import ConfirmCommand


class ConfirmCommandParser(object):
    def parse(self, data):
        return ConfirmCommand(data)
