# -*- coding: utf-8 -*-
import scrapy
from DoubanMovies.items import DoubanmoviesItem

class DoubanmoviesspiderSpider(scrapy.Spider):
    name = 'DoubanMoviesSpider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250?start=0']

    def parse(self, response):
        for sel in response.xpath('//div[@class="item"]'):
            item = DoubanmoviesItem()
            item["img"] = sel.xpath('div[@class="pic"]//img/@src').extract_first()
            item["title"] = "".join(sel.xpath('div[@class="info"]//span[@class="title"]/text()').extract()).replace('\xa0', ' ')
            item["desc"] = "".join(sel.xpath('div[@class="info"]/div[@class="bd"]/p/text()').extract()).replace('\xa0', ' ').strip()
            item["score"] = sel.xpath('div[@class="info"]//span[@class="rating_num"]/text()').extract_first()
            item["eval"] = sel.xpath('.//div[@class="star"]/span[4]/text()').extract_first()[:-3]

            item["image_urls"] = []
            item["image_urls"].append(item["img"])

            yield item

        url = response.urljoin(response.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract_first())

        if url:
            yield scrapy.Request(url, callback=self.parse)
