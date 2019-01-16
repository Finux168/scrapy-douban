# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field

# 类似java中的实体类(model)
class DoubanmcItem(Item):
    movieName = Field()
    reviewer = Field()
    reviewTime = Field()
    reviewTopic = Field()
    reviewTitle = Field()
    reviewContent = Field()
    createTime = Field()
