from asyncfileserver.model.confirm_command import ConfirmCommand


class ConfirmCommandFactory(object):
    def create(self, data):
        return ConfirmCommand(data)
