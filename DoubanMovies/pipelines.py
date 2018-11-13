# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import pymongo
# from urllib import request


class DoubanmoviesPipeline(object):
    collection_name = "Movies_Top250"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get("MONGO_URI"), crawler.settings.get("MONGO_DB"))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)  # 连接MongoDB数据库
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()  # 关闭MongoDB数据库连接

    def process_item(self, item, spider):
        item_data = dict(item)
        item_data.pop("img")
        item_data.pop("image_urls")
        item_data["images"][0]["path"] = spider.settings.get("IMAGES_STORE") + "/" + item_data["images"][0]["path"]
        item_data["imgs"] = item_data.pop("images")
        self.db[self.collection_name].insert_one(item_data)
        return item


# class SaveImgPipeLine(object):
#     def process_item(self, item, spider):
#         img_data = request.urlopen(item["img"]).read()
#         img_name = item["img"].split("/")[-1]
#
#         with open("./MoviesImages/" + img_name, "wb") as f:
#             f.write(img_data)
#
#         return item