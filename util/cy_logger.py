# -*- coding: utf-8 -*-
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# 自定义的日志输出
def log(msg, level=logging.INFO):
    logging.log(level, msg)


def error(msg):
    log(msg, logging.ERROR)


def debug(msg):
    log(msg, logging.DEBUG)
