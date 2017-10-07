import scrapy
from greatschools.items import GreatschoolsItem
from datetime import datetime
import re
import json


class Fundrazr(scrapy.Spider):
	name = "my_scraper"

	# First Start Url
	start_urls = ["https://www.greatschools.org/california/san-diego/schools/"]

	npages = 32
	download_delay = 2

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

		# get url of website
		item['url'] = response.url

		# Getting School Title
		item['schoolTitle'] = response.xpath("//div[contains(@class, 'school-name-container')]/h1[contains(@class,'school-name')]/text()").extract()[0]

		# Getting outOf5Stars
		item['outOf5Stars']= response.xpath("//div[contains(@class, 'n-out-of-5-stars')]/text()").extract()

		# Getting totalNumReviews:
		potentialReview = response.xpath("//div[contains(@class, 'number-of-reviews')]/span[contains(@class, 'count')]/text()").extract()

		if len(potentialReview) > 0: 
			item['totalNumReviews']  = potentialReview

		else: 
			item['totalNumReviews'] = 'None'

		# StarBreakdown 
		item['StarBreakout'] = response.xpath("//div[contains(@class, 'star-rating-bar-viz')]/span[contains(@class, 'answer-count')]/text()").extract()

		# Basically getting basic information about the school grades, studentsNumber, types
		# Code below removes wierd spaces and new line characters. If this wasn't for short term project (like for production) I would make less error prone code. 
		toDistributeList = [x.strip() for x in response.xpath("//div[@class='school-info__item']/descendant::text()").extract() if len(x.strip()) > 0]
		item['grades'] = toDistributeList[1]
		item['studentsNumber'] = toDistributeList[3]
		item['types'] = toDistributeList[5]


		# The following section gets Race/ethnicity, Low-income students, students with disabilities
		lookslikeJson = response.xpath("//div[contains(@data-component-name, 'SchoolProfileComponent')]/@data-props").extract()

		jsonDict = {}
		for oneJson in lookslikeJson:
			newJson = json.loads(oneJson) 

			# This is to make it easier to know what nested JSON are
			jsonDict[newJson['anchor']] = newJson

		item['lowIncomeRaceDisbilityJson'] = jsonDict

		yield item

