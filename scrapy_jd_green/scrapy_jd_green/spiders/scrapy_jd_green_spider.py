import scrapy


class ScrapyJdGreenSpiderSpider(scrapy.Spider):
    name = "scrapy_jd_green_spider"
    allowed_domains = ["green-japan.com"]
    start_urls = ["https://green-japan.com"]

    def parse(self, response):
        pass
