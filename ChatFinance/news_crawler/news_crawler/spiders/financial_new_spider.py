from news_crawler.items import NewsCrawlerItem

from pathlib import Path

import scrapy
from scrapy.linkextractors import LinkExtractor


class FinancialNewsSpider(scrapy.Spider):
    name = "financial_news"

    def start_requests(self):
        urls = [
            "https://www.cnbc.com/quotes/IBM?qsearchterm=IBM",
            "https://www.cnbc.com/quotes/TELA?qsearchterm=TELA"
            
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def _extract_next(self, response):
        links = LinkExtractor(restrict_css=".LatestNews-headlineWrapper a").extract_links(response)
        urls = []
        for link in links:
            if link.url.startswith("http"):
                urls.append(link.url)
        return urls


    def parse(self, response):
        item = NewsCrawlerItem()
        item['url'] = response.url
        item['body'] = response.body
        self.log(f"Craw url: {response.url}")
        yield item

        next_urls = self._extract_next(response)
        for url in next_urls:
            yield scrapy.Request(url=url, callback=self.parse)