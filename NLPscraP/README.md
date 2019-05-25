NLscraP
===================

This repository contains a scraper (Scrapy framework) that crawls the web by parsing urls from a csv file. The spider used to crawl web news articles titles and description is `/scrapy_url/scrapy_url/spiders/url_spider.py`.
The output csv file containing the urls scrapped, their title and their description will be saved in `/scrapy_url/`. A sample is shared here, named `scrapped_test.csv`.

`NLP_analysis.ipynb` performs Natural Language processing tasks for Topic modelling. It analyses the urls, the title and description and assigns topic depending on their contents.
