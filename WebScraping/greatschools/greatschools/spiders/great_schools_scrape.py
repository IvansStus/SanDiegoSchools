import scrapy
from greatschools.items import GreatschoolsItem
from datetime import datetime
import re


class Fundrazr(scrapy.Spider):
	name = "my_scraper"

	# First Start Url
	start_urls = ["https://www.greatschools.org/california/san-diego/schools/"]

	npages = 2

	# This mimics getting the pages using the next button. 
	for i in range(2, npages + 2 ):
		start_urls.append("https://www.greatschools.org/california/san-diego/schools/?page="+str(i)+"")
	
	def parse(self, response):
		for href in response.xpath("//div[contains(@class, 'ptm notranslate')]//a[contains(@class, 'open-sans_sb mbs font-size-medium rs-schoolName')]//@href"):
			# add the scheme, eg http:// 
			url  = "https://www.greatschools.org" + href.extract() 
			yield scrapy.Request(url, callback=self.parse_dir_contents)	
					
	def parse_dir_contents(self, response):
		item = GreatschoolsItem()

		# Getting School Title
		item['schoolTitle'] = response.xpath("//div[contains(@class, 'school-name-container')]/h1[contains(@class,'school-name')]/text()").extract()[0]

		# Getting outOf5Stars
		item['outOf5Stars']= response.xpath("//div[contains(@class, 'n-out-of-5-stars')]/text()").extract()

		# Getting totalNumReviews:
		item['totalNumReviews'] = response.xpath("//div[contains(@class, 'number-of-reviews')]/span[contains(@class, 'count')]/text()").extract()[0]

		# StarBreakout
		item['StarBreakout'] = response.xpath("//div[contains(@class, 'star-rating-bar-viz')]/span[contains(@class, 'answer-count')]/text()").extract()

		yield item

