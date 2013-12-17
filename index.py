__author__ = 'nikita_kartashov'
# -*- coding: utf-8 -*-

from odict import odict
import nltk
from nltk.corpus import stopwords

MINIMUM_WORD_LENGTH = 3


def sort_by_value(item):
    return item[1]


class Index:
    def __init__(self):
        self._words = {}
        self._words_count = -1
        self._blacklisted_parts_of_speech = ('PRP', 'NUM', 'TO', 'PRO', 'UH', 'WH', 'IN', 'TO', 'CC', ':', 'P',)

    def normalize_word(self, word):
        word = word.lower()
        if len(word) < MINIMUM_WORD_LENGTH:
            return None

        lemmatizer = nltk.stem.WordNetLemmatizer()
        word = lemmatizer.lemmatize(word)
        return word

    def add_word(self, link, word):
        word = self.normalize_word(word)
        if not word:
            return
        if word not in self._words.keys():
            self._words[word] = {}
        urls = self._words[word]
        urls[link] = urls.get(link, 0) + 1

    def add_words(self, link, words):
        words = [word for word, tag in nltk.pos_tag(words) if tag not in self._blacklisted_parts_of_speech]
        for word in words:
            self.add_word(link, word)

    def sort(self):
        sorted_words = {}
        for word in self._words:
            sorted_words[word] = odict(sorted(self._words[word].iteritems(), key=sort_by_value, reverse=True))
        self._words = sorted_words

    def status(self):
        if self._words_count == -1:
            self._words_count = 0
            for k, v in self._words.iteritems():
                self._words_count += sum(count for site, count in v.iteritems())

        print('Уникальных слов в индексе %d' % len(self._words))
        print('Всего слов в индексе %d' % self._words_count)

    def query(self, query_text):
        words = [word.strip().lower() for word in query_text.split()]
        result = {}
        keys = self._words.keys()
        for word in words:
            if word in keys:
                for k, v in self._words[word].iteritems():
                    result[k] = result.get(k, 0) + v

        return sorted(result.iteritems(), key=sort_by_value, reverse=True)