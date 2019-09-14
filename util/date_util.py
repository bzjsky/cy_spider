# -*- coding: utf-8 -*-
import datetime
import time
from util.cy_logger import log


def get_date(millisecond):
    """
    时间转换
    :param millisecond: 毫秒
    :return:
    """
    if millisecond is None or millisecond < 0:
        return None
    return time.localtime(millisecond/1000)


def strptime(string, format):
    try:
        if string is None or len(string) == 0:
            return None
        return time.strptime(string, format)
    except Exception as e:
        log("时间转换失败===> params: {},{}".format(string, format) + str(e))


def date_before_h(hour):
    if hour is not None:
        return datetime.datetime.now()-datetime.timedelta(hours=hour)


def get_before_date_str(days):
    return str(datetime.date.today() - datetime.timedelta(days=days))
