# -*- coding: utf-8 -*-
from scrapy import Selector


def str_to_selector(html_str):
    """
    字符串转变html选择器
    :param html_str:
    :return:
    """
    if html_str is None or len(html_str) == 0:
        return Selector()
    return Selector(text=html_str)
