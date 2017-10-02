# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class GreatschoolsItem(scrapy.Item):
	schoolTitle = scrapy.Field()
	outOf5Stars = scrapy.Field()
	totalNumReviews = scrapy.Field()
	StarBreakout = scrapy.Field()

	grades = scrapy.Field()
	studentsNumber = scrapy.Field()
	types = scrapy.Field()

