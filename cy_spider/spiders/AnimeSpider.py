# -*- coding: utf-8 -*
import os
import re
import execjs

from scrapy import Request

from cy_spider.spiders.BaseSpider import BaseSpider


class AnimeSpider(BaseSpider):
    """
    阿里漫画爬虫

    斗罗大陆
    http://www.alimanhua.com/manhua/74/index.html
    斗罗大陆2绝世唐门
    http://www.alimanhua.com/manhua/613/index.html
    斗罗大陆3龙王传说
    http://www.alimanhua.com/manhua/214/index.html
    斗罗大陆4终极斗罗
    http://www.alimanhua.com/manhua/3001/index.html
    武动乾坤
    http://www.alimanhua.com/manhua/159/
    """

    # 自定义配置
    custom_settings = {
    }

    name = 'anime'
    allowed_domains = []

    def __init__(self, *a, **kw):
        super(AnimeSpider, self).__init__(*a, **kw)
        self.root_url = "http://www.alimanhua.com/manhua/159/"
        self.target_dir = '/Users/zj/work/动漫/武动乾坤/'

    def start_requests(self):
        yield Request(
            url=self.root_url,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        items = response.xpath('//*[@id="play_0"]/ul/li')
        max_length = len(items)
        for item in items:
            dir = str(max_length)+"-"+item.xpath('a/text()').extract_first()
            max_length -= 1
            if not os.path.exists(self.target_dir + dir):
                yield Request(
                    url="http://www.alimanhua.com" + item.xpath('a/@href').extract_first(),
                    callback=self.detail,
                    dont_filter=True,
                    meta={"dir": dir},
                )

    def detail(self, response):
        str = re.findall(r'packed=".+\"', response.text)
        str = str[0][8:-1]
        items = listAll(str)
        print(response.meta["dir"])
        n = 0
        for item in items:
            n += 1
            if item:
                yield Request(
                    "http://res.img.fffmanhua.com/"+item,
                    dont_filter=True,
                    headers={},
                    meta={"dir": response.meta["dir"], "filename": n},
                    callback=self.download
                )

    def download(self, response):
        dir = response.meta["dir"]
        filename = response.meta['filename']
        self.download_files(self.target_dir+dir+"/", "{filename}.jpg".format(filename=filename),
                            response.body)


ctx = execjs.compile(
    """
    function base64decode(str) {
        var base64DecodeChars = new Array(-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1);
        var c1 = 0;
        var c2 = 0;
        var c3 = 0;
        var c4 = 0;
        var out = "";
        var len = str.length;
        var i = 0;
        while (i < len) {
            c1 = base64DecodeChars[str.charCodeAt(i++) & 255]
            while (i < len && c1 == -1) {
                c1 = base64DecodeChars[str.charCodeAt(i++) & 255]
            }
            if (c1 == -1) {
                break
            }
            c2 = base64DecodeChars[str.charCodeAt(i++) & 255]
            while (i < len && c2 == -1) {
                c2 = base64DecodeChars[str.charCodeAt(i++) & 255]
            }
            if (c2 == -1) {
                break
            };
            out += String.fromCharCode((c1 << 2) | ((c2 & 48) >> 4));
            c3 = str.charCodeAt(i++) & 255; if (c3 == 61) { return out } c3 = base64DecodeChars[c3]
            while (i < len && c3 == -1){
                c3 = str.charCodeAt(i++) & 255; if (c3 == 61) { return out } c3 = base64DecodeChars[c3]
            }
            if (c3 == -1) {
                break
            };
            out += String.fromCharCode(((c2 & 15) << 4) | ((c3 & 60) >> 2));
            c4 = str.charCodeAt(i++) & 255; if (c4 == 61) { return out } c4 = base64DecodeChars[c4]
            while (i < len && c4 == -1){
                c4 = str.charCodeAt(i++) & 255; if (c4 == 61) { return out } c4 = base64DecodeChars[c4]
            }
            if (c4 == -1) {
                break
            }
            out += String.fromCharCode(((c3 & 3) << 6) | c4)
        }
        return out.slice(4);
    };
    """
)


def listAll(str):
    n2 = ctx.call("base64decode", str)
    if n2.startswith("eval("):
        strJs = execjs.eval(n2[5:-2])
    else:
        strJs = execjs.eval(n2)
    strJs = strJs.split(";")
    allImageName = []
    for item in strJs:
        allImageName.append(item.split("=")[-1].replace("\"", ""))
    return allImageName

