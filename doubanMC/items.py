# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field


class DoubanmcItem(Item):
    movieName = Field()
    reviewer = Field()
    reviewTime = Field()
    reviewTopic = Field()
    reviewTitle = Field()
    reviewContent = Field()
