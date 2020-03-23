import aiofiles
from contextlib import closing


class File(object):
    def __init__(self, async_file):
        self._async_file = async_file
