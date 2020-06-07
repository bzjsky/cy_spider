# -*- coding: utf-8 -*-

from scrapy.cmdline import execute


def crawl(spiders):
    for spider in spiders:
        execute(['scrapy', 'crawl', spider])


if __name__ == '__main__':
    crawl([
        # "xiaobei",
        # "proxy_ip",
        "anime",
    ])

