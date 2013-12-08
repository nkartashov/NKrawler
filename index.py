__author__ = 'nikita_kartashov'


class Index:
    def __init__(self):
        self._words = {}

    def add_word(self, url, word):
        if word not in self._words.keys():
            self._words[word] = {}
        urls = self._words[word]
        urls[url] = urls.get(url, 0) + 1