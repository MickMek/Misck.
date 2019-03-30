import pandas as pd
import time
import bs4
import selenium
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from selenium import webdriver

# All brokers URLs
urls = [
    #"https://immobilier.jll.fr/search?tenureType=rent&propertyType=office&placeName=Paris&lat=48.89020516885645&lng=2.2439543000000413&radius=1.6925951641182715&sortBy=rank&orderBy=asc&page=1",
    "https://www.bnppre.fr/a-louer/bureau/hauts-de-seine-92/la-defense-92998/",
    #"https://www.bureauxlocaux.com/immobilier-d-entreprise/annonces/quartier/la-defense/location-bureaux"
    ]

# Geocoding function (from adress to lat/long max 50 queries daily)
def geocode(adrs):
    driver = webdriver.Safari()

    # Entering address to search
    driver.get("https://www.latlong.net/convert-address-to-lat-long.html")
    form = driver.find_element_by_tag_name("label")
    inp_id = form.get_attribute("for")

    box = driver.find_element_by_xpath(f"//*[@id='{inp_id}']")
    box.send_keys(adrs)
    submit = driver.find_element_by_tag_name('button')
    submit.submit()
    time.sleep(5)

    #Extracting geolocation information
    result1 = driver.find_element_by_id("lat").get_attribute("value")
    result2 = driver.find_element_by_id("lng").get_attribute("value")
    driver.close()
    return [result1,result2]

filename = "pld_brokers2.csv" 
for complete_url in urls:
    print(complete_url)
    if "bureauxlocaux" in complete_url:
        print(1)
        NBR_PAGES = 3 #Original page @around 30 pages
        links1 = []
        driver = webdriver.Safari()
        driver.get(complete_url)
        try:
            driver.switch_to.alert()
            driver.find_element_by_xpath('//*[@id="cboxClose"]/svg').click()
            time.sleep(2)
        except:
             None
        for i in range(0,NBR_PAGES+1):
            time.sleep(3)
            try:
                driver.find_element_by_xpath('//*[@id="cboxClose"]/button').click()
                url=driver.current_url
                driver.close()
                driver = webdriver.Safari()
                driver.get(url)
            except:
                None
            time.sleep(3)
            try: #trying with selenium (gives empty page_soup)
                page_html = driver.page_source
                from bs4 import BeautifulSoup as soup
                page_soup = soup(page_html, 'html.parser')
                soup = page_soup.find('ul',{'class':"list-cards"})
            except: #trying with uReq (forbidden 403)
                uClient = uReq(url)
                page_html = uClient.read()
                uClient.close()
                from bs4 import BeautifulSoup as soup
                page_soup = soup(page_html, 'html.parser')
                soup = page_soup.find('ul',{'class':"list-cards"})   
            try:
                driver.find_element_by_xpath('//*[@id="react-pagination"]/div/ul/li[7]/a').click()
            except:
                driver.find_element_by_xpath('//*[@id="react-pagination"]/div/ul/li[6]/a').click()

            links = [link['href'] for link in soup('a') if 'href' in link.attrs]
            links = list(set(links))
            print(links)
            links1.append(links)
        driver.close()

        # Getting information for each page
        links2=[]
        for i in range(0,len(links1)):
            for j in range(0,len(links1[i])):
                links2.append(links1[i][j])

        for i in range(0,len(links2)):
            driver = webdriver.Safari()
            my_url = f"https://www.bureauxlocaux.com{links2[i]}"
            driver.get(my_url)
            try:
                driver.switch_to.alert()
                driver.find_element_by_xpath('//*[@id="cboxClose"]/svg').click()
                time.sleep(2)
            except:
	             None
            page_html = driver.page_source
            #driver.find_element_by_xpath('//*[@id="cboxClose"]').click()
            #url=driver.current_url
            time.sleep(3)
            driver.close()
            from bs4 import BeautifulSoup as soup
            page_soup = soup(page_html, 'html.parser')
            description = page_soup.find('div',{'class':"ad-core"}).text
            affiche = description.strip().split("\n\n")[0]
            address = affiche.split("\n")[1]
            geoloc = geocode(address)
            f = open(filename, 'a+')
            f.write(f"{address}; {geoloc}; {my_url}; \n")
            f.close()
            print(address)
            print(geoloc)
            print(my_url)
            print()
        print(f"{i} new ")
        
        
    elif "bnppre" in complete_url:
        print(2)
        driver = webdriver.Safari()
        driver.get(complete_url)
        driver.find_element_by_xpath('//*[@id="BtnResults"]/button').click()
        time.sleep(3)
        for i in range(0,2):
            try:
                driver.find_element_by_xpath('//*[@id="BtnResults"]/button').click()
                time.sleep(3)
            except:
                None
        from bs4 import BeautifulSoup as soup
        page_soup = soup(driver.page_source, 'lxml')
        soup = page_soup.find('ul',{'class':"list_annonces_wrapper"})
        links = [link['href'] for link in soup('a') if 'href' in link.attrs]
        driver.close()

        # Scrapping from all pages
        for j in range(0,len(links)):
            my_url = f"https://www.bnppre.fr{links[j]}"
            uClient = uReq(my_url)
            page_html = uClient.read().decode('utf-8')
            uClient.close()
            from bs4 import BeautifulSoup as soup
            page_soup = soup(page_html, 'html.parser')

            rows = page_soup.find('div',{'id':'Detail'})
            name = rows.find('div',{'class':"block title"})
            try:
                address = rows.find('article',{'id':"BlocLocalisation"}).text.split(":")[1].split(" La DéfenseCarte")[0].strip()
                geoloc = geocode(address)
            except:
                None
            try:
                availability = rows.find('article',{'id':"BlocSurface"}).text.split('-')[1:len(rows.find('article',{'id':"BlocSurface"}).text.split('-'))]
            except:
                None
            surface = rows.find('tr',{'class':"surface"}).text
            loyer = rows.find('tr',{'class':"loyer"}).text
            print(address)
            print(geoloc)
            print(my_url)
            #print(availability)
            print(f"{surface}/{loyer}")
            print()
            f = open(filename, 'a+')
            f.write(f"{address}; {geoloc}; {my_url}; {surface}/{loyer} \n")
            f.close()
        print(f"{j} new ")
            
    elif "immobilier.jll" in complete_url:
        print(3)
        # Getting all links from homepage
        my_url = complete_url
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()

        page_soup = soup(page_html, 'html.parser')
        soup = page_soup.find('div',{'class':'SRPPropertyListing'})
        links = [link['href'] for link in soup('a') if 'href' in link.attrs]
        links = list(set(links))
        
        # Getting info from each link
        for j in range(0,len(links)):
            my_url = f"https://immobilier.jll.fr{links[j]}"
            uClient = uReq(my_url)
            page_html = uClient.read()
            uClient.close()
            from bs4 import BeautifulSoup as soup
            page_soup = soup(page_html, 'html.parser')
            #head = page_soup.find('div',{'class':'PDPDetailsCard__row PDPDetailsCard__head'})
            title = page_soup.find('div',{'class':'PDPDetailsCard__row PDPDetailsCard__title'})
            address = page_soup.find('div',{'class':'PDPDetailsCard__row PDPDetailsCard__address'})
            geoloc = geocode(address.text)
            metrics = page_soup.find('div',{'class':'PDPDetailsCard__metrics'})
            #description = page_soup.find('div',{'class':'PropertyDetailsPage__description'})
            #service = page_soup.find('ul',{'class':'TickList'})
            #description2 = page_soup.find('div',{'class':'PDPSpaceAvailability__floor PDPSpaceAvailability__floor-0'})

            #print(head.text)
            f = open(filename, 'a+')
            f.write(f"{title.text} - {address.text}; {geoloc}; {my_url}; {metrics.text} \n")
            f.close()
            print(f"{title.text} - {address.text}")
            print(geoloc)
            print(my_url)
            print(metrics.text)
            print()
            #print(description.text)
            #print(service.text)
            #print(description2.text)
        print(f"{j} new ")