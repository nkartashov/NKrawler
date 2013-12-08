__author__ = 'nikita_kartashov'
# -*- coding: utf-8 -*-

import sys

from index import Index
from crawler import CustomCrawler


url = input("Input desired url")
depth = int(input("Input desired depth"))

#url = 'http://mit.spbau.ru/sewiki/index.php/SE_Wiki'
#url = 'http://en.wikipedia.org/wiki/World_Trade_Organization'


def build_index(url, depth):
    index = Index()
    crawler = CustomCrawler(url, depth, index)
    crawler.crawl_all_links()
    index.status()
    print('Страниц просмотрено %d' % len(crawler.visited))
    return index


#depth = 3
index = build_index(url, depth)

index.sort()

#for word in index._words.iterkeys():
#    print(word)

while True:
    query = raw_input('Ask Me Anything: ').decode(sys.stdin.encoding)
    if query == 'mischief managed':
        break
    result = index.query(query)
    for k, v in result:
        print("%d matches at %s" % (v, k))