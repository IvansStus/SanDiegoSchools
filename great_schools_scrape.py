import scrapy
from greatschools.items import GreatschoolsItem
from datetime import datetime
import re
import json
from flatten_json import flatten_json
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
from urlparse import urlparse



class Fundrazr(scrapy.Spider):
	name = "my_scraper"
	download_delay = 2

	def parse(self, response):
		profileDf = pd.read_csv('school_profiles.csv')
		for href in list(profileDf['overviewlink']):
			url  = href
			yield scrapy.Request(href, callback=self.parse_dir_contents)	
			
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

		newJson = json.loads(lookslikeJson[0])

		df = json_normalize(flatten_json(newJson))

		# Replacing Really Long Column Names
		df.columns = df.columns.str.replace('California Assessment of Student Performance and Progress \(CAASPP\)', 'CAASPP')

		# Science has a different standardized Test than English and Math, but calling them same for coding
		df.columns = df.columns.str.replace('California Standards Tests', 'CAASPP')

		# #creates a new dataframe that's empty
		allSubjectDF = pd.DataFrame(columns = ['Subject', 'Ethnicity', 'schoolScore','stateScore']) 

				# This is the start of column names this accounts for subjects 
		base_list = ['data_0_data_1', 'data_0_data_2', 'data_0_data_3']

		for base in base_list: 
		             
		    # Get School subject this will be merged in last to dataframe
		    subject = base + '_title'
		    subjectCol = df.columns[df.columns.str.contains(pat = subject)]
		    subjectToAdd = df[subjectCol.values].values[0]
		             
		    # Score
		    score = base + '_values_CAASPP_[0-9]_score'
		    scoreCol = df.columns[df.columns.str.contains(pat = score)]
		    scoreDf = pd.DataFrame(data = np.transpose(df[scoreCol.values].values), columns = ['schoolScore'])
		    
		    # State Score Comparison
		    stateScore = base + '_values_CAASPP_[0-9]_state_average$'
		    stateCol = df.columns[df.columns.str.contains(pat = stateScore)]
		    stateDf = pd.DataFrame(data = np.transpose(df[stateCol.values].values), columns = ['stateScore'])
		    
		    # Ethnicity of the Students
		    ethnicity = base + '_values_CAASPP_[0-9]_breakdown'
		    ethnicityCol = df.columns[df.columns.str.contains(pat = ethnicity)]
		    ethnicityDf = pd.DataFrame(data = np.transpose(df[ethnicityCol.values].values), columns = ['Ethnicity'])
		         
		    # Concatenating Dataframes 
		    ethSchoolStateDf = pd.concat([ethnicityDf, scoreDf, stateDf], axis = 1)
		    
		    ethSchoolStateDf['Subject'] = subjectToAdd[0]
		    
		    allSubjectDF = pd.concat([allSubjectDF, ethSchoolStateDf], axis = 0,ignore_index=True) # ignoring index is optional
		 
		allSubjectDF['gsID'] = response.url.rsplit('/', 2)[-2].split("-")[0]

		allSubjectDF.to_csv('greatSchoolsTestScore.csv', mode = 'a', header = False, index = False)

		yield item

