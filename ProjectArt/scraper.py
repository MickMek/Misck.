#USING SELENIUM PACKAGE FOR LOGIN
import time
from selenium import webdriver
import selenium
import random
import bs4
import numpy as np
from bs4 import BeautifulSoup as soup

driver = webdriver.Safari()
driver.get('https://www.artprice.com/identity')

# Login
time.sleep(10)
driver.find_element_by_name('login').send_keys('') #MUST ENTER USERNAME
driver.find_element_by_name('pass').send_keys('') #MUST ENTER PASSWORD
driver.find_element_by_xpath('//*[@id="weblog_form"]/button').click()

NUMBER_OF_PAGES = 32
for j in range(1,NUMBER_OF_PAGES+1):
    time.sleep(random.randrange(10,20))
    driver.get(f"https://www.artprice.com/artist/30269/andy-warhol/lots/pasts?ipp=100&p={j}")
    page_html = driver.page_source
    page_soup = soup(page_html, 'html.parser')
    containers = page_soup.findAll("div",{"class":"col-xs-8 col-sm-6"})
    
    filename = "a-warhol_artpieces.csv"
    f = open(filename, 'a+')
    
    for i in range(1,len(containers)+1):
        try:
            title_piece = containers[i].a["title"].replace(",",";")
            date = containers[i].date.text.strip().replace(")","").replace("(","")
            date = date.replace("c.","")
            misc_info = containers[i].findAll("p")[1].text.strip().split(",")
            art_type = misc_info[0]
            material_used = misc_info[1]
            if len(containers[i].findAll("p")[1].text.strip().split(",")) > 3:
                size = misc_info[-1]
                size = size.split("in")[1]
                for k in range (2, len(containers[i].findAll("p")[1].text.strip().split(","))-1):
                    misc_info1 = misc_info[k].strip()
                    material_used = material_used.strip()+f"/{misc_info1}"
            else:
                size = misc_info[2]
                size = size.split("in")[1]
            try:
                low_estimate = containers[i].findAll("p")[2].findAll("span")[0].text.strip().split("-")[0].strip().split(" ")[1].replace(",","")
                high_estimate = containers[i].findAll("p")[2].findAll("span")[0].text.strip().split("-")[1].strip().split(" ")[1].replace(",","")
            except:
                low_estimate = containers[i].findAll("p")[2].findAll("span")[0].text.strip().split("-")[0].strip().split(" ")[1].replace(",","")
                high_estimate = ""
            if "Lot" in containers[i].findAll("p")[3].findAll("span")[0].text:
                hammer_price = "lot not sold"
            else:
                if "communicated" in containers[i].findAll("p")[3].findAll("span")[0].text:
                    hammer_price = "not communicated"
                else:
                    hammer_price = containers[i].findAll("p")[3].findAll("span")[0].text.strip().split(" ")[1].replace(",","")
            auction_house = containers[i].findAll("p")[4].findAll("strong")[0].text.strip()
            auction_date = containers[i].findAll("p")[4].text.split(",")[1].strip()
            auction_location = containers[i].findAll("p")[5].text.strip()
            #print(title_piece + "," + date+ "," +art_type+ "," +material_used+ "," +size+ "," +low_estimate+ "," +high_estimate+ "," +hammer_price+ "," +auction_house+ "," +auction_date+ "," +auction_location+"\n")
            f.write(title_piece + "," + date+ "," +art_type+ "," +material_used+ "," +size+ "," +low_estimate+ "," +high_estimate+ "," +hammer_price+ "," +auction_house+ "," +auction_date+ "," +auction_location+"\n")

        except:
            if i==100:
                print(f"Completed scraping page{j}")
            else:
                print(f"Formating error while parsing for item {i}, page{j}")

    f.close()