__author__ = 'nikita_kartashov'
# -*- coding: utf-8 -*-

import re
from pattern.web import plaintext
from pattern.web import Crawler, BREADTH, FILO
import inspect


class CustomCrawler(Crawler):
    def __init__(self, url, depth, index):
        Crawler.__init__(self, links=[url])
        re_text = u"""[абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЭЬЮЯ
        ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-]+"""
        self._clear_text_re = re.compile(re_text)
        self._index = index
        self._current_depth = -1
        self._depths = {self.next: 0}
        self._max_depth = depth

    def visit(self, link, source=None):
        if source:
            text = plaintext(source)
            words = self.split_text(text)
            self._index.add_words(link.url, words)

    def crawl_all_links(self):
        while self.crawl():
            pass

    def crawl(self, method=BREADTH, **kwargs):
        next_link = self.next
        if next_link:
            self._current_depth = self._depths[next_link]
            print('Crawling %dth page at depth %d' % (len(self.visited), self._current_depth))
            try:
                return Crawler.crawl(self, method, **kwargs)
            except Exception as e:
                print('Ошибка при построении индекса: %s' % e)
        return False

    def push(self, link, priority=1.0, sort=FILO):
        if inspect.stack()[2][3] == '__init__':
            Crawler.push(self, link, priority, sort)
        elif self._current_depth + 1 < self._max_depth:
            self._depths[link] = self._current_depth + 1
            Crawler.push(self, link, priority, sort)

    def split_text(self, text):
        split_text = self._clear_text_re.findall(text)
        result = []
        for string in split_text:
            result.extend(string.strip().split())
        return [word.lower() for word in result]





