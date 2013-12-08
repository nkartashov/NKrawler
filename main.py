__author__ = 'nikita_kartashov'

from index import Index
from crawler import Crawler

#url = input("Input desired url")
#depth = int(input("Input desired depth"))

url = "http://habrahabr.ru/hub/mesh_networking/"
depth = 1

index = Index()

crawler = Crawler()

crawler.crawl(url, depth, index)

print(crawler._pages_visited)
print(len(index._words))

