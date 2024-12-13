# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()

    key_phrases = scrapy.Field()  # For storing extracted key phrases
    sentiment = scrapy.Field()    # For storing sentiment analysis
    sentiment_score = scrapy.Field()  # Store sentiment score (e.g., confidence level)

