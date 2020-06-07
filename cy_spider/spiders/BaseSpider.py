# -*- coding: utf-8 -*-
import logging
import os

from scrapy.spiders import CrawlSpider


class BaseSpider(CrawlSpider):
    name = None

    def __init__(self, *a, **kw):
        super(BaseSpider, self).__init__(*a, **kw)

    def parse(self, response):
        pass

    def log_error(self, msg):
        self.log(msg, logging.ERROR)

    def download_files(self, root_dir, filename, body):

        is_exists = os.path.exists(root_dir)  # 是否存在该目录
        if not is_exists:
            os.makedirs(root_dir)
            self.log('{0} creat successful!'.format(root_dir))
        with open(root_dir + filename, "wb") as f:
            f.write(body)
