# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import logging

#
class MongodbPipeline:

    collection_name = "articles"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://moe:testtest@cluster0.pmexa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = self.client[spider.name]

    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        print('processing?')
        self.db[self.collection_name].insert(item)
        return item
