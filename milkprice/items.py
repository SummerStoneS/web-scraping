# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MilkpriceItem(scrapy.Item):
    # define the fields for your item here like:
    sku_id = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()



