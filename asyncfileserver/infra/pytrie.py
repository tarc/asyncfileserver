import pytrie


class Trie(object):
    def __init__(self, trie):
        self._trie = trie

    def is_prefix_of_some_key(self, data):
        keys_prefixed_by_data_generator = self._trie.iterkeys(data)
        return next(keys_prefixed_by_data_generator, None) != None

    def longest_key_prefix_of(self, data):
        return self._trie.longest_prefix_item(data, None)

class TrieFactory(object):
    def get(self, keys, values):
        return Trie(pytrie.Trie(zip(keys, values)))
