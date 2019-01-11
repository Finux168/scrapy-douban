# -*- coding: utf-8 -*-
import scrapy
from doubanMC.items import DoubanmcItem

class doubanMCSpiders(scrapy.Spider):
    name="doubanmc"

    def start_requests(self):
        yield scrapy.Request(url='https://movie.douban.com/review/best/', callback=self.parse)

    def parse(self,response):
        items = []
        # 取css的格式类似jQuery
        reviewItems = response.css('.main.review-item')
        print 'review item'
        # print reviewItems
        for reviewItem in reviewItems:
            # print reviewItem
            item = DoubanmcItem()
            item['movieName']=reviewItem.css('a img::attr(title)').extract_first()
            item['reviewer']=reviewItem.css('header a.name::text').extract_first()
            item['reviewTime']=reviewItem.css('header span.main-meta::text').extract_first()
            item['reviewTopic']=reviewItem.css('header a.rel-topic::text').extract_first()
            item['reviewTitle']=reviewItem.css('.main-bd h2 a::text').extract_first()
            item['reviewContent']=reviewItem.css('.main-bd div.review-short div.short-content::text').extract_first()
            items.append(item)
        return items