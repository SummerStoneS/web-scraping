# -*- coding: utf-8 -*-
import scrapy
from suv.items import SuvItem
import urllib

base_url = 'http://product.auto.163.com'


class SuvALLSpider(scrapy.Spider):
    name = 'suv_all'
    allowed_domains = ['product.auto.163.com']
    start_urls = [
        # 'http://product.auto.163.com/rank/hotIndices_SUV.html#fixedpos'
    # 'http://product.auto.163.com/rank/hotIndices_paoche.html#fixedpos'
    #                'http://product.auto.163.com/rank/hotIndices_liangxiang.html#fixedpos'
                   'http://product.auto.163.com/rank/hotIndices_sanxiang.html#fixedpos']

    def parse(self, response):

        # 获得2017年50周的link
        week_2017 = response.xpath('//*[@id="historyrank_nav"]/div[2]/div[1]//h5')     # len = 50

        for week_index in week_2017:
            autoItem = SuvItem()
            week_url = week_index.xpath('.//a/@href').extract()[0]
            week_num = week_index.xpath('.//a/text()').extract()[0].strip()    # 2017年第50周榜，去掉左右两端的换行符
            # week_num = week_index.xpath('.//a/@title').extract()[0]
            autoItem['week_num'] = week_num             # 记录是第几周的

            week_url = urllib.parse.urljoin(base_url, week_url)
            request = scrapy.Request(week_url, meta={'item': autoItem}, callback=self.parse_week_url)
            # request.meta['item'] = autoItem
            yield request

    def parse_week_url(self, response):
        # 排行榜的node list
        autoItem0 = response.meta['item']
        autoItem0['url'] = response.url
        autoItem0['time'] = response.url[response.url.find('.html')-8:response.url.find('.html')]
        # autoItem0['price_range'] = response.url[response.url.find('SUV_')+4:response.url.find('.html')-8]

        rank_list = response.xpath('//*[@id="ranklstbox_d"]/div[2]/div')

        for rank_index in rank_list:
            autoItem = autoItem0.copy()
            autoItem['rank_num'] = rank_index.xpath('.//div[@class="imgbox"]/span/text()').extract()[0]         # 排名
            autoItem['car_name'] = rank_index.xpath('.//div[@class="txtbox"]//h5/a/text()').extract()[0]        # 车的名字
            autoItem['place'] = rank_index.xpath('.//div[@class="txtbox"]//span/text()').extract()[0]           # 国产
            autoItem['price'] = rank_index.xpath('.//div[@class="txtbox"]//span/text()').extract()[2].strip()
            autoItem['entry_year'] = rank_index.xpath('.//div[@class="txtbox"]//p/text()')[5].extract()         # 上市年份
            autoItem['quantity_type'] = rank_index.xpath('.//div[@class="txtbox"]//p/text()')[7].extract().strip() # 在产车型
            autoItem['emission_load'] = rank_index.xpath('.//div[@class="txtbox"]//p/text()')[9].extract().strip() #排放量
            autoItem['fuel_consumption'] = rank_index.xpath('.//div[@class="txtbox"]//p/text()')[11].extract().strip() # 油耗
            yield autoItem
