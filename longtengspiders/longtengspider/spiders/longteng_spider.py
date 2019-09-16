# -*- coding: utf-8 -*-
import scrapy

from longtengspiders.longtengspider.items import LongtengspiderItem

class LongtengSpiderSpider(scrapy.Spider):
    name = 'longteng_spider'
    allowed_domains = ['wap.wanrenxs.org']
    start_urls = ['https://wap.wanrenxs.org/top/allvisit_1/']
    num = -1

    def parse(self, response):
        booklist = response.xpath("//section[2]/ul/li[2]/span[1]/a")
        for book in booklist[:3]:
            self.num = -1
            bookName = book.xpath('./text()').extract()[0]
            booklink = "https://wap.wanrenxs.org" + book.xpath("./@href").extract()[0]
            # print(booklink)
            yield scrapy.Request(booklink,meta={'bookName':bookName},callback=self.GetChapterCatalog)
        book_paging_list = response.xpath("/html/body/div[1]/a")
        if len(book_paging_list) == 2 and "首页" not in book_paging_list:
            next_book_paging = "https://wap.wanrenxs.org" + book_paging_list[0].xpath("./@href").extract()[0]
        elif len(book_paging_list) == 4:
            next_book_paging = "https://wap.wanrenxs.org" + book_paging_list[2].xpath("./@href").extract()[0]
        yield scrapy.Request(next_book_paging,callback=self.parse)
    def GetChapterCatalog(self,response):
        '''获得书籍的章节目录'''
        bookName = response.meta['bookName']

        AllChapterUrl = "https://wap.wanrenxs.org" + response.xpath("//div[1]/section[2]/div[2]/a/@href").extract()[0]
        yield scrapy.Request(AllChapterUrl,meta={"bookName":bookName},callback=self.GetChapterUrl)

    def GetChapterUrl(self,response):
        '''得到书籍每一个章节的url'''
        bookName = response.meta['bookName']
        chapterlist = response.xpath("//*[@id='zjlb']/ul/li/a[@class='xbk']")
        for chapter in chapterlist:
            chapterName = chapter.xpath("./text()").extract()[0]
            # print(bookName,chapterName)
            chapterUrl = "https://wap.wanrenxs.org" + chapter.xpath("./@href").extract()[0]
            yield scrapy.Request(chapterUrl,meta={"bookName":bookName,
                                                  "chapterName":chapterName,
                                                  "chapterUrl":chapterUrl},
                                 callback=self.GetChapterContent)
        chapter_pageing_list = response.xpath("//*[@id='zjlb']/div[2]/div[1]/div[4]/ul/li/a/@href").extract()
        if self.num < (len(chapter_pageing_list) - 1) and chapter_pageing_list:
            self.num += 1
            yield scrapy.Request("https://wap.wanrenxs.org" + chapter_pageing_list[self.num],
                                 meta={"bookName":bookName,
                                        "chapterName":chapterName,
                                        "chapterUrl":chapterUrl},
                                 callback=self.GetChapterUrl)
    def GetChapterContent(self,response):
        '''获得章节的内容'''
        bookName = response.meta["bookName"]
        chapterName = response.meta["chapterName"]
        chapterUrl = response.meta["chapterUrl"]

        chaptercontent = response.xpath("//*[@id='nr']/text()").extract()
        chapterContent = "".join(chaptercontent).strip()

        longteng_item = LongtengspiderItem()
        longteng_item["bookName"] = bookName
        longteng_item["chapterName"] = chapterName
        longteng_item["chapterUrl"] = chapterUrl
        longteng_item["chapterContent"] = chapterContent

        return longteng_item


