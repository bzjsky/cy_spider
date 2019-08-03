# -*- coding: utf-8 -*-
from scrapy import Request
from selenium import webdriver
from scrapy import signals
from pydispatch import dispatcher
from cy_spider.spiders.BaseSpider import BaseSpider


class PedailySeleniumSpider(BaseSpider):

    name = "zdb_selenium"
    allowed_domains = ["pedaily.cn"]
    # 抓取第1页数据
    start_urls = ['https://zdb.pedaily.cn/people/p{page}/'.format(page=page) for page in range(1, 2)]

    def __init__(self, *a, **kw):
        super(PedailySeleniumSpider, self).__init__(*a, **kw)
        chrome_options = webdriver.ChromeOptions()
        # 不打开浏览器窗口
        chrome_options.add_argument('headless')
        chrome_options.add_argument('no-sandbox')
        self.browser = webdriver.Chrome(executable_path=r'cy_spider/file/chromedriver.exe',
                                        chrome_options=chrome_options)
        # 传递信息,也就是当爬虫关闭时scrapy会发出一个spider_closed的信息,当这个信号发出时就调用closeSpider函数关闭这个浏览器.
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def start_requests(self):
        for start_url in self.start_urls:
            yield Request(
                start_url,
                meta={"selenium": True},
                dont_filter=True
            )

    def parse(self, response):
        self.log("*" * 100)
        self.log("列表地址：" + response.url)
        self.log("*" * 100)
        items = response.xpath('//*[@id="people-list"]/li')
        for item in items:
            yield Request(
                item.xpath('div[1]/a/@href').extract_first(),
                dont_filter=True,
                headers={},
                meta={"selenium": True},
                callback=self.detail
                )

    def detail(self, response):
        self.log("*" * 100)
        self.log("投资人物姓名：" + response.xpath("normalize-space(/html/body/div[3]/div[1]/div/"
                                            "div[2]/div[2]/h1/text())").extract_first())
        self.log("所属公司：" + response.xpath("normalize-space(/html/body/div[3]/div[1]/div/div[2]/div[2]/div/span["
                                          "1]/text())").extract_first())
        self.log("*" * 100)

    def spider_closed(self):
        self.log("spider closed")
        # 当爬虫退出的时关闭浏览器
        self.browser.quit()
