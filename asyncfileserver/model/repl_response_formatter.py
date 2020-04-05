from asyncfileserver.model.repl_response import REPLResponse


class REPLResponseFormatter(object):
    def format(self, data):
        return REPLResponse(data)
