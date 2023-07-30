# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobDescription(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    job_title = scrapy.Field()
    job_role = scrapy.Field()
    business_details = scrapy.Field()
    job_description = scrapy.Field()
    outline = scrapy.Field()
    job_requirements = scrapy.Field()
    salary = scrapy.Field()
    selection_process = scrapy.Field()
    job_location = scrapy.Field()
    job_benefits = scrapy.Field()
    
    pass
