# -*- coding: utf-8 -*-
import scrapy


class AutoCommentSpider(scrapy.Spider):
    name = 'auto_comment'
    allowed_domains = ['k.autohome.com.cn']
    start_urls = ['https://k.autohome.com.cn/521/8609/#pvareaid=101484']

    def parse(self, response):

        pass
