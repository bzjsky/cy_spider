# -*- coding: utf-8 -*-
import re

from scrapy import Request

from cy_spider.spiders.BaseSpider import BaseSpider


class XiaoBeiSpider(BaseSpider):

    """
    小贝PS视频教程爬虫
    """

    # 自定义配置
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #     }
    # }

    name = "xiaobei"
    allowed_domains = ["mxiaobei.com"]

    start_urls = ['http://www.mxiaobei.com/?cate=18&page={page}'.format(page=page) for page in range(1, 40)]

    def __init__(self, *a, **kw):
        super(XiaoBeiSpider, self).__init__(*a, **kw)

    def parse(self, response):
        html = response.xpath('//*[@id="infinitescroll"]')
        items = html.xpath("li/div[1]/a")
        for item in items:
            yield Request(
                item.xpath("@href").extract_first(),
                dont_filter=True,
                headers={},
                callback=self.detail
            )

    def detail(self, response):
        items = re.findall(r'http://.+\.mp4', response.text)
        if items:
            yield Request(
                items[0],
                dont_filter=True,
                headers={},
                meta={"filename": response.xpath('/html/body/div[2]/div[1]/h2/text()').extract_first()},
                callback=self.download
            )

    def download(self, response):
        self.downloadfiles('/Users/zj/work/学习/ps/', "{filename}.mp4".format(filename=response.meta['filename']),
                           response.body)

