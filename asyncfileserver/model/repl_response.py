class REPLResponse(object):
    def __init__(self, response):
        self._response = response

    def __str__(self):
        return "RESPONSE\n" if self._response else "NONE\n"
