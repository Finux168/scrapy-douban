# -*- coding: utf-8 -*-
import json
import codecs
from collections import OrderedDict
import pymongo
import time

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


class MongoPipeline(object):
    def __init__(self,mongoUrl,mongoDB,mongoColl):
        self.mongoUrl = mongoUrl
        self.mongoDB = mongoDB
        self.mongoColl = mongoColl

    @classmethod
    def from_crawler(cls,crawler):
        '''
            scrapy为我们访问settings提供了这样的一个方法，这里，
            我们需要从settings.py文件中，取得数据库的URI和数据库名称
        '''
        return cls(
            mongoUrl=crawler.settings.get('MONGO_URI'),
            mongoDB=crawler.settings.get('MONGO_DB'),
            mongoColl=crawler.settings.get('MONGO_COLL')
        )

    # 爬虫一旦开启，就会实现这个方法，连接到数据库
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongoUrl)
        self.db = self.client[self.mongoDB]
        #做了一个清除集合的操作,如果是不断新增,注释即可
        self.db.drop_collection(self.mongoColl)
        self.collection = self.db[self.mongoColl]

    # 爬虫一旦关闭，就会实现这个方法，关闭数据库连接
    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        '''
            每个实现保存的类里面必须都要有这个方法，且名字固定，用来具体实现怎么保存
        '''
        #增加创建时间
        item['createTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        #将对象序列化成字符串
        document = OrderedDict(item)
        #将文档插入集合
        self.collection.insert(document)
        return item