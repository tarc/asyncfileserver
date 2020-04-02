from asyncfileserver.model.confirm_command import ConfirmCommand


class ConfirmCommandFactory(object):
    def create_command(self, data):
        return ConfirmCommand(data)
