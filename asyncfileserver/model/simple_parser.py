import re


class SimpleParser(object):
    _up_to_eol_pattern = re.compile(b'[^\n]*')
    _eol_pattern = re.compile(b'\n')

    def __init__(self, command_tags, commands, error, trie_factory):
        self._trie = trie_factory.get(command_tags, commands)
        self._error = error
        self._command = None

    def parse(self, data):
        if self._command != None:
            return self._consume_up_to_eol(data)

        commands_prefixed_by_data = self._trie.iterkeys(data)
        if next(commands_prefixed_by_data, None) != None:
            return None, 0

        command_prefix_of_data = self._trie.longest_prefix_item(data, None)

        if command_prefix_of_data == None:
            self._command = self._error, data
            return self._consume_up_to_eol(data)

        prefix, command = command_prefix_of_data

        if data[len(prefix):len(prefix)+1].isalnum():
            self._command = self._error, data[:len(prefix) + 1]
            return self._consume_up_to_eol(data)

        self._command = command, data[:len(prefix) + 1]

        return self._consume_up_to_eol(data, len(prefix))

    def _consume_up_to_eol(self, data, index=0):
        up_to_eol_match = self._up_to_eol_pattern.match(data, index)

        assert(up_to_eol_match != None)

        index = up_to_eol_match.end()
        eol_match = self._eol_pattern.match(data, index)

        if eol_match != None:
            index = eol_match.end()
            command = self._command
            self._command = None
            return command, index

        return None, index
