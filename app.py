import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from urllib.request import Request,urlopen
import re

headers = {"User-Agent":"Mozilla/5.0"}

url = "http://www.koeri.boun.edu.tr/scripts/lst9.asp" #COPYRIGHT Boğaziçi Üniversitesi Kandilli Rasathanesi ve Deprem Araştırma Enstitüsü Bölgesel Deprem-Tsunami İzleme Ve Değerlendirme Merkezi 

response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

pre = soup.find("pre") # All data is found inside the <pre> element on the page.


lines = []
for line in pre.text.strip().split("\n"):
    if re.match(r"\d{4}\.\d{2}\.\d{2}", line):  # YYYY.MM.DD format search
        lines.append(line)

print("This is the last earthquake:",lines[0]) #last earthquake
print("This is the 500th latest earthquake:",lines[499]) #the 500th latest earthquake

data = []
for line in lines:
    parts = line.strip().split()
    if len(parts) < 8:
        continue
    date = parts[0]
    time = parts[1]
    latitude = float(parts[2])
    longitude = float(parts[3])
    depth = float(parts[4])     
    
    #Kandilli has 3 types: MD (5), ML (6), MW (7)
    #ML is my last fallback, as it's the most common one.
    if parts[5] != '-.-':
        magnitude = float(parts[5])
    elif parts[7] != '-.-':
        magnitude = float(parts[7])
    else:
        magnitude = float(parts[6])
    if parts[5] != '-.-':
        type = str("MD")
    elif parts[7] != '-.-':
        type = str("MW")
    else:
        type = str("ML")
    location = " ".join(parts[8:10])
    data.append([date, time, latitude, longitude, depth, magnitude, type, location])

df = pd.DataFrame(data, columns=["Date", "Time", "Latitude(N)", "Longitude(E)", "Depth(km)", "Magnitude", "Type", "Location"]) 
print(df)
