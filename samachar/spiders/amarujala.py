# -*- coding: utf-8 -*-
import scrapy
import logging
import urlparse

from scrapy.spiders import Spider
from scrapy.selector import Selector
from samachar.items import SamacharItem
import re
import sys

class AmarujalaSpider(scrapy.Spider):
    name = "amarujala"
    allowed_domains = ["amarujala.com"]
    start_urls = (
        'http://www.amarujala.com/bizarre-news',
    )

    def parse(self, response):
     
        news = Selector(response).xpath("//ul[@class='relNws']/li")
        print news
        for news in news:
            item = SamacharItem()
            item['title'] = news.xpath("a/text()").extract_first()
            item['url'] = news.xpath("a/@href").extract_first()

            if item['url']:
                request = scrapy.Request(url="http://www.amarujala.com"+item['url'], callback=self.parse_detail_page, meta={'item':item}, dont_filter=True)   
            request.meta['item'] =item
            yield request

    def parse_detail_page(self, response):
        item = response.meta['item']
        detailPageSelector = Selector(response)
        item['shortdesc'] = detailPageSelector.xpath("//h3[@id='desc']/text()").extract_first()
        item['description'] = detailPageSelector.xpath("//h3[@id='desc']/text()").extract_first()

        item['img_title'] = detailPageSelector.xpath("//img[@id='myImage']/@title").extract_first()

    	if detailPageSelector.xpath("//img[@id='myImage']/@src").extract_first():
        	item['img_urls'] = detailPageSelector.xpath("//img[@id='myImage']/@src").extract_first()
        else:
            item['img_urls'] = "No Image!"
        
        yield item
