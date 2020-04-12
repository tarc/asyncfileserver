from asyncfileserver.model.repl_command import REPLCommand


class REPLCommandParser(object):
    def parse(self, data):
        return REPLCommand()
