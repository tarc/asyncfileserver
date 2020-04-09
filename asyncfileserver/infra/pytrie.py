from pytrie import Trie


class TrieFactory(object):
    def get(self, keys, values):
        return Trie(zip(keys, values))
