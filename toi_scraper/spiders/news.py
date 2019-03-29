# -*- coding: utf-8 -*-
import scrapy
from toi_scraper.items import NewsArticle


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['timesofindia.indiatimes.com/rss.cms']
    start_urls = ['https://timesofindia.indiatimes.com/rss.cms/']

    def parse(self, response):
        for url in response.xpath('//td[@width="120"]')[:17]:
            request = scrapy.Request(url.xpath('a/@href').get(), callback=self.parse_rss_feed)
            request.meta['category'] = url.xpath('a/text()').get()
            yield request
        

    def parse_rss_feed(self, response):
        items = response.xpath('//item')

        for item in items:
            news_item = NewsArticle()
            news_item['title'] = item.xpath('title/text()').get()
            news_item['description'] = item.xpath('description/text()').get()
            news_item['link'] = item.xpath('link/text()').get()
            news_item['pub_date'] = item.xpath('pubDate/text()').get()
            news_item['category'] = response.meta['category']
            
            yield news_item
