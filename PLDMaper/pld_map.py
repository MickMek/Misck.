import folium
import os
import numpy as np
import pandas as pd
import time
import webbrowser

df = pd.read_csv("pld_brokers.csv", delimiter=";")

names = df["ADDRESSE "]
geoloc = df[" GEOLOCALISATION "]
urls = df[" URL_SITE "]

lat = []
lon = []
name = []
for i in range(0,len(df)):
    lon.append(float(geoloc[i].strip().split(",")[0][2:-1]))
    lat.append(float(geoloc[i].strip().split(",")[1][2:-2]))
    name.append(f"{names[i].strip()} \n {urls[i]}")

# Building map
data = pd.DataFrame({
'lat':lat,
'lon':lon,
'name':name,
})

m = folium.Map(location=[48.89198, 2.23881], tiles="OpenStreetMap", zoom_start=15)

for i in range(0,len(data)):
    folium.Marker([data.iloc[i]['lon'], data.iloc[i]['lat']], popup=data.iloc[i]['name']).add_to(m)
m   
m.save('ladefense_map.html')

filename = 'file:///Users/home/Documents/GitHub/Misck./PLDMaper/' + 'ladefense_map.html'
webbrowser.open_new_tab(filename)

