# -*- coding: utf-8 -*
from scrapy import Request

from cy_spider.items import IpItem
from cy_spider.spiders.BaseSpider import BaseSpider


class FreeIpSpider(BaseSpider):
    """
    获取免费代理IP
    """

    # 自定义配置
    custom_settings = {
        'ITEM_PIPELINES': {
            'cy_spider.pipelines.FreeIpSpiderPipeline': 500,
        },
    }

    name = 'freeIp'
    allowed_domains = []

    def __init__(self, *a, **kw):
        super(FreeIpSpider, self).__init__(*a, **kw)

    def start_requests(self):
        url = 'https://www.kuaidaili.com/free/'
        yield Request(
            url=url,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        items = response.xpath('//*[@id="list"]/table/tbody/tr')
        for item in items:
            pojo = IpItem()
            pojo['ip'] = item.xpath('td[1]/text()').extract_first()
            pojo['port'] = item.xpath('td[2]/text()').extract_first()
            yield pojo

