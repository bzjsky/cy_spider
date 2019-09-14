# -*- coding: utf-8 -*-


def string_to_dict(cookie):
    """
    字符串转cookies字典
    :param cookie: 可以从浏览器 Request Headers - Cookie 获取
    :return:
    """
    cookie_dict = {}
    items = cookie.split(';')
    for item in items:
        if '=' in item:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            cookie_dict[key] = value
    return cookie_dict


