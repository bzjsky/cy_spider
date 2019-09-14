# -*- coding: utf-8 -*-
import re


def find_first(pattern, string):
    if string is None or len(string) == 0:
        return
    items = re.findall(pattern, string)
    if len(items) > 0:
        return items[0]


def remove(pattern, string):
    return re.sub(
        pattern=pattern,
        repl="",
        string=string
    )
