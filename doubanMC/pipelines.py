# -*- coding: utf-8 -*-
import json
import codecs
from collections import OrderedDict

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanmcPipeline(object):

    def __init__(self):
        #使用utf-8编码打开json文件
        self.file = codecs.open('doubanmc.jl','w',encoding='utf-8')

    def process_item(self, item, spider):
        #OrderedDict将item对象序列化成字典,同时根据key进行排序
        #将item序列化成字符串,写入文件
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=True) + "\n"
        self.file.write(line)
        return item

    def close_spider(self,spider):
        #关闭文件
        self.file.close()
