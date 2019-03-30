# PLDMaper

This folder contains scripts used during the BM&A Hackathon 2019 at ESCP Europe - Paris. 

`PLD_scrapper.py` is a script that crawls the web for real estate availability in Paris - La Defense area and surroundings.
Its output is a csv file (`pld_brokers2.csv`) with information on available office spaces, including:
- address
- geolocalization
- description and price

`pld_map.py` creates a map of Paris - La Defense area and marks available information from `pld_brokers2.csv`). Its output is the map as an html file (`ladefense_map.html`) 

![Alt text](https://github.com/MickMek/Misck./PLDMaper/blob/master/pld_map.png?raw=true "Paris - La Defense (offices availabilities)")
