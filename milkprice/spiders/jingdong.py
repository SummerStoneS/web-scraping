# -*- coding: utf-8 -*-
import scrapy
from milkprice.items import MilkpriceItem


base_url = 'https://search.jd.com/s_new.php?keyword=%E5%A9%B4%E5%84%BF%E5%A5%B6%E7%B2%89&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E5%A9%B4%E5%84%BF%E5%A5%B6%E7%B2%89&stock=1&page=1&s=29&scrolling=y'

class JingdongSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['search.jd.com']
    start_urls = [base_url.replace('page=1', 'page='+str(i+1)) for i in range(6)]

    def parse(self, response):
        """
            直接获取每个sku-data
        """
        product = MilkpriceItem()

        sku_list = response.xpath('//li[@class="gl-item"]')
        name_selector = response.xpath('//div[@class="p-name p-name-type-2"]//em')

        for i in range(len(sku_list)):
            product['sku_id'] = sku_list[i].xpath('./@data-sku').extract()[0]   # xpath里的.是必须的，一定要选取当前节点。
            price = sku_list[i].xpath('.//div[@class="p-price"]//i//text()').extract_first()
            if price:
                product['price'] = float(price)
            else:
                product['price'] = ''
            product['brand'] = name_selector[i].xpath('./text()').extract()[0]
            product['name'] = name_selector[i].xpath('./text()').extract()[1:]
            yield product


class JingdongNewSpider(scrapy.Spider):
    name = 'jdnew'
    allowed_domains = ['search.jd.com']
    start_urls = [base_url.replace('page=1', 'page='+str(i+1)) for i in range(6)]

    def parse(self, response):
        """
            解析商品列表页，获取每个产品的link
        """
        url_list = response.xpath('//div[@class="p-name p-name-type-2"]//a/@href').extract()
        for url in url_list:
            request = scrapy.Request(url, callback=self.parse_product)
            yield request

    def parse_product(self, response):
        """
            解析每个商品详情里的价格，名称
        """
        product = MilkpriceItem()
        name_list = response.xpath('//div[@class="sku-name"]/text()').extract()
        name_list = [x.strip() for x in name_list if len(x.strip()) > 0]  # 去除名称的前后空格or换行符，去除空字符串
        product['name'] = name_list[0]
