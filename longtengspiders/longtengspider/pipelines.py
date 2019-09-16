# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os


class LongtengspiderPipeline(object):
    def process_item(self, item, spider):

        dirPath = r'F:\book9999' + '\\' + item['bookName']

        # dirpath = r"C:\Users\Administrator\Desktop\book" + "\\" + "a" + "\\" + "b"
        filepath = dirPath + "\\" + item['chapterName'] + ".txt"
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(item['chapterContent'])
        return item
