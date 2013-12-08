__author__ = 'nikita_kartashov'
# -*- coding: utf-8 -*-

from codecs import open
import re
from pattern.web import URL
from pattern.web import DOM
from pattern.web import plaintext
from pattern.web import abs


class Crawler:
    def __init__(self):
        with open("stopwords.txt", encoding="utf-8") as f:
            self._stopwords = f.readlines()
        self._stopwords = [word.strip() for word in self._stopwords]
        re_text = u"""[абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЭЬЮЯ
        ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-]+"""
        self._clear_text_re = re.compile(re_text)
        self._visited = []
        self._pages_visited = 0

    def split_text(self, text):
        re.UNICODE = True
        split_text = self._clear_text_re.findall(text)
        result = []
        for string in split_text:
            result.extend(string.strip().split())
        return [word.lower() for word in result if word not in self._stopwords and len(word) > 2]

    def crawl(self, url, depth, index):
        self._visited.append(url)
        self._pages_visited += 1
        depth -= 1
        url = URL(url)
        html = url.download()
        text = plaintext(html)
        words = self.split_text(text)

        dom = DOM(html)
        links = []
        for link in dom('a'):
            links.append(abs(link.attributes.get('href', ''), base=url.redirect or url.string))

        links = [link for link in set(links) if link not in self._visited]

        if depth >= 0:
            for link in links:
                self.crawl(link, depth, index)
        for word in words:
            index.add_word(url, word)




