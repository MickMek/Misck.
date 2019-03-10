import time
import bs4
import selenium
from bs4 import BeautifulSoup as soup
from selenium import webdriver

ENTER_NORAD_ID = input("Enter NORAD ID: ")
driver = webdriver.Safari()
#driver.get('https://www.n2yo.com/?s=43651')
driver.get(f'https://www.n2yo.com/?s={ENTER_NORAD_ID}&live=1')
while True:
    time.sleep(10)
    page_soup = soup(driver.page_source, 'lxml')
    filename = f"rnn_data_{ENTER_NORAD_ID}.csv"
    f = open(filename, 'a+')
    data1 = str()
    for tr in page_soup.find_all('tr')[1:15]:
        tds = tr.find_all('td')
        data1 = data1 + f"{tds[1].text},"
    data1 = data1 + str(page_soup.find_all("tr", {'class':"bgray"})[7].text.split(":")[1])
    lat = float(data1.split(",")[3])
    lon = float(data1.split(",")[4])
    alt = float(data1.split(",")[5])
    spd = float(data1.split(",")[7])
    azi = float(data1.split(",")[9].split(" ")[0])
    azi_cat = data1.split(",")[9].split(" ")[1]
    ele = float(data1.split(",")[10])
    asc_h = float(data1.split(",")[11].split(" ")[0][:-1])
    asc_m = float(data1.split(",")[11].split(" ")[1][:-1])
    asc_s = float(data1.split(",")[11].split(" ")[2][:-1])
    dec_deg = float(data1.split(",")[12].split(" ")[0][:-1])
    dec_deg2 = float(data1.split(",")[12].split(" ")[1][:-1])
    dec_deg3 = float(data1.split(",")[12].split(" ")[2][:-2])
    loc_time_h = float(data1.split(",")[13].split(" ")[0][:-1])
    loc_time_m = float(data1.split(",")[13].split(" ")[1][:-1])
    loc_time_s = float(data1.split(",")[13].split(" ")[2][:-1])

    data1 = f"{lat},{lon},{alt},{spd},{azi},{azi_cat},{ele},{asc_h},{asc_m},{asc_s},{dec_deg},{dec_deg2},{dec_deg3},{loc_time_h},{loc_time_m},{loc_time_s}\n"
    #print(data1)
    #print(tds[0].text, tds[1].text)
    f.write(data1)
    f.close()