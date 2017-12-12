# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutoScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    category = scrapy.Field()
    week_num = scrapy.Field()
    rank_num = scrapy.Field()
    car_name = scrapy.Field()
    place = scrapy.Field()
    price = scrapy.Field()
    entry_year = scrapy.Field()
    quantity_type = scrapy.Field()
    emission_load = scrapy.Field()
    fuel_consumption = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    price_range = scrapy.Field()
