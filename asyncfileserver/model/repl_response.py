class REPLResponse(object):
    def __init__(self, response):
        self._response = response

    def __str__(self):
        return f'RESPONSE: "{self._response}"\n'
