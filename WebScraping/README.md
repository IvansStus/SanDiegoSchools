
## Creating a New Scrapy project
1. Making scrapy project 
```
scrapy startproject greatschools
```

## Finding good start URLs using Inspect on Google Chrome (or Firefox)
1. The first in the list <b>start_urls</b> is: 
https://www.greatschools.org/california/san-diego/schools/

second start url is: 
https://www.greatschools.org/california/san-diego/schools/?page=2

the third start url is: 
https://www.greatschools.org/california/san-diego/schools/?page=3

```
start_urls = ["https://www.greatschools.org/california/san-diego/schools/"]

npages = 32

# This mimics getting the pages using the next button. 
for i in range(2, npages + 2 ):
	start_urls.append("https://www.greatschools.org/california/san-diego/schools/?page="+str(i)+"")
```

## Scrapy Shell for finding Individual School links

1. Using Scrapy shell 

```
scrapy shell 'https://www.greatschools.org/california/san-diego/schools/'
```

Type the following into scrapy shell to get campaign links: 

```
response.xpath("//div[contains(@class, 'ptm notranslate')]//a[contains(@class, 'open-sans_sb mbs font-size-medium rs-schoolName')]//@href").extract()
```

The code below is for getting all the school links for a given start url (more on this later in the First Spider section)

```

for href in response.xpath("//h2[contains(@class, 'title headline-font')]/a[contains(@class, 'campaign-link')]//@href"):
	# add the scheme, eg http:// 
	url  = "https://www.greatschools.org" + href.extract() 
```

2. Exit Scrapy Shell by typing <b>exit()</b>

## Inspecting Individual School Pages
While we should previously worked on understanding the structure of where individual school links are, this section goes over where things are on individual school pages.

1. Next we go to an individual school page (see link below) to scrape
```
https://www.greatschools.org/california/san-diego/6034-Los-Penasquitos-Elementary-School/
```

2. Using the same inspect process as before, we inspect the title on the page

3. Now we are going to use scrapy shell again, but this time with an individual school. We do this because we want to find out how individual campaigns are formatted (including finding out how to extract the title from the webpage).
In terminal type (mac/linux):

```
scrapy shell 'https://www.greatschools.org/california/san-diego/6034-Los-Penasquitos-Elementary-School/'
```

The code to get the school title is
```
response.xpath("//div[contains(@class, 'school-name-container')]/h1[contains(@class,'school-name')]").extract()[0]
```

4. 
outOf5Stars:

```
response.xpath("//div[contains(@class, 'n-out-of-5-stars')]/text()").extract()
```

totalNumReviews: 

```
response.xpath("//div[contains(@class, 'number-of-reviews')]/span[contains(@class, 'count')]/text()").extract()[0]
```





