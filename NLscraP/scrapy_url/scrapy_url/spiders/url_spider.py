import scrapy
import pandas as pd

class QuotesSpider(scrapy.Spider):
    name = "url_articles"

    def start_requests(self):
    	df = pd.read_csv("/Users/home/Documents/GitHub/Misck./NLscraP/data.csv")
    	for i in range(0,len(df)):
    		print(df.iloc[i,0])
    		if "sport24.lefigaro" in str(df.iloc[i,0]): #Condition to debug sport24.figaro website
    			yield scrapy.Request(url=f"http://{str(df.iloc[i,0])}", callback=self.parse)
    		else:
    			yield scrapy.Request(url=f"https://{str(df.iloc[i,0])}", callback=self.parse)

    def parse(self, response):
        filename = "scrapped_url.csv"
        page_url = response.url
        title = response.xpath('//html/head/title/text()').get()
        description = response.xpath('//html/head/meta[@name="description"]/@content').get()
        with open(filename, 'a') as f:
            f.write(f"{page_url.replace(',',';')},{title.replace(',',';')},{description.replace(',',';')} \n")
        self.log(f"scrap added to {filename}")
        print("================")
        print(f"{page_url.replace(',',';')},{title.replace(',',';')},{description.replace(',',';')} \n")
        print("================")