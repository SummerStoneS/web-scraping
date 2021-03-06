# -*- coding: utf-8 -*-
import scrapy
from wangyi_suv.items import WangyiSuvItem
import urllib


base_url = 'http://product.auto.163.com'


class DifferentSuvSpider(scrapy.Spider):
    name = 'All_cartype'
    allowed_domains = ['product.auto.163.com']
    start_urls = ['http://product.auto.163.com/rank/index_by_cartype.html#fixedpos/']

    def parse(self, response):
        # 车的分类index
        suv_index = response.xpath('//*[@id="bd"]/div/div[1]/div[2]/div[2]/div[1]/h5/a')
        autoItem0 = WangyiSuvItem()
        for suv_type in suv_index:
            # 拿到每种suv的链接，和text
            autoItem = autoItem0.copy()
            suv_url = suv_type.xpath('./@href').extract()[0]
            category = suv_type.xpath('./text()').extract()[0]       # 例如：‘微型车
            autoItem['category'] = category                         # 记录是哪种suv车

            suv_url = urllib.parse.urljoin(base_url, suv_url)
            request = scrapy.Request(suv_url, meta={'item': autoItem}, callback=self.parse_suv_url)
            # request.meta['item'] = autoItem
            yield request

    def parse_suv_url(self, response):

        # 获得2017年51周的link
        week_2017 = response.xpath('//*[@id="historyrank_nav"]/div[2]/div[1]//h5')     # len = 50

        for week_index in week_2017:
            autoItem = response.meta['item'].copy()
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

