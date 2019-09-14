# -*- coding: utf-8 -*
from scrapy import Request

from cy_spider.spiders.BaseSpider import BaseSpider


class ProxySpider(BaseSpider):
    # 自定义配置
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'cy_spider.middlewares.ProxyMiddleware': 543,
        }
    }

    name = 'proxy_ip'
    allowed_domains = []

    def __init__(self, *a, **kw):
        super(ProxySpider, self).__init__(*a, **kw)

    def start_requests(self):
        url = 'http://200019.ip138.com/'

        for i in range(4):
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        self.log(response.xpath("/html/body/p[1]/text()").extract_first())
