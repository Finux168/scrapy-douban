# -*- coding: utf-8 -*-
import scrapy
from doubanMC.items import DoubanmcItem
from scrapy_splash import SplashRequest

class doubanMCSpiders(scrapy.Spider):
    name="doubanmc"

    # script = """
    #     function main(splash)
    #         --加载url
    #         assert(splash:go(splash.args.url))
    #         splash:wait(0.5)
    #         --自适应屏幕,防止出现某些元素无法加载
    #         splash:set_viewport_full()
    #         --选择所有class为review-short的元素
  	#         local reviewShorts = splash:select_all('.review-short');
  	#         --遍历元素,添加点击事件
	# 	    for _, reviewShort in ipairs(reviewShorts) do
    # 	        reviewShort:mouse_click()
	# 	    end
    #         --点击事件后,需要加载缓冲一会儿
    #         splash:wait(1)
    #         --返回点击事件后的html
    #         return splash:html()
    #     end
    # """

    #在脚本中写中文会有编码问题,具体注释如上
    script = """
        function main(splash)
            assert(splash:go(splash.args.url))
            splash:wait(0.5)
            splash:set_viewport_full()
            local reviewShorts = splash:select_all('.review-short');
    	    for _, reviewShort in ipairs(reviewShorts) do
    	        splash:wait(1)
    	        reviewShort:mouse_click()
    	    end
            splash:wait(1)
            return splash:html()
        end
    """

    def start_requests(self):
        yield SplashRequest('https://movie.douban.com/review/best/', self.parse,endpoint='execute',args={'lua_source':self.script,'wait':2})

    def parse(self,response):
        items = []
        # 取css的格式类似jQuery
        reviewItems = response.css('.main.review-item')
        tempItems = response.css('.review-content.clearfix')
        for reviewItem in reviewItems:
            # print reviewItem
            item = DoubanmcItem()
            item['movieName']=reviewItem.css('a img::attr(title)').extract_first()
            item['reviewer']=reviewItem.css('header a.name::text').extract_first()
            item['reviewTime']=reviewItem.css('header span.main-meta::text').extract_first()
            item['reviewTopic']=reviewItem.css('header a.rel-topic::text').extract_first()
            item['reviewTitle']=reviewItem.css('.main-bd h2 a::text').extract_first()
            contentItem = reviewItem.css('.review-content.clearfix')
            item['reviewContent']= contentItem.xpath('.//text()').extract()
            items.append(item)
        #返回之后,会到pipeline中进行处理
        return items