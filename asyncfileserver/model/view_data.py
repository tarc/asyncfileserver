class ViewData(object):
    def __init__(self, data):
        self._data = data
    
    def __str__(self):
        return f"<DATA size: {len(self._data)}>"
