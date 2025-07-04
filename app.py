import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import re
import time
import folium
import webbrowser
import os

headers = {"User-Agent":"Mozilla/5.0"}

url = "http://www.koeri.boun.edu.tr/scripts/lst9.asp" #COPYRIGHT Boğaziçi Üniversitesi Kandilli Rasathanesi ve Deprem Araştırma Enstitüsü Bölgesel Deprem-Tsunami İzleme Ve Değerlendirme Merkezi 

response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

pre = soup.find("pre") # All data is found inside the <pre> element on the page.


lines = []
for line in pre.text.strip().split("\n"):
    if re.match(r"\d{4}\.\d{2}\.\d{2}", line):  # YYYY.MM.DD format search
        lines.append(line)

# print("This is the last earthquake:",lines[0]) #last earthquake
# print("This is the 500th latest earthquake:",lines[499]) #the 500th latest earthquake

data = []
for line in lines:
    parts = line.strip().split()
    if len(parts) < 8:
        continue
    date = parts[0]
    time_str = parts[1]
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
    i = 8
    location_parts = []
    while i < len(parts) and (parts[i] != "İlksel" and parts[i] != "REVIZE01"): # Collect all location parts until we reach the status marker ("İlksel" or "REVIZE01")
        location_parts.append(parts[i])
        i += 1
    location = " ".join(location_parts)
    data.append([date, time_str, latitude, longitude, depth, magnitude, type, location])

df = pd.DataFrame(data, columns=["Date", "Time", "Latitude(N)", "Longitude(E)", "Depth(km)", "Magnitude", "Type", "Location"]) 

#APP START
def refresh_():
    global df
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    pre = soup.find("pre")

    lines = []
    for line in pre.text.strip().split("\n"):
        if re.match(r"\d{4}\.\d{2}\.\d{2}", line):
            lines.append(line)

    data = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 8:
            continue
        date = parts[0]
        time_str = parts[1]
        latitude = float(parts[2])
        longitude = float(parts[3])
        depth = float(parts[4])
        if parts[5] != '-.-':
            magnitude = float(parts[5])
            typ = "MD"
        elif parts[7] != '-.-':
            magnitude = float(parts[7])
            typ = "MW"
        else:
            magnitude = float(parts[6])
            typ = "ML"
        i = 8
        location_parts = []
        while i < len(parts) and (parts[i] != "İlksel" and parts[i] != "REVIZE01"):
            location_parts.append(parts[i])
            i += 1
        location = " ".join(location_parts)
        data.append([date, time_str, latitude, longitude, depth, magnitude, typ, location])

    df = pd.DataFrame(data, columns=["Date", "Time", "Latitude(N)", "Longitude(E)", "Depth(km)", "Magnitude", "Type", "Location"])
    time.sleep(1)
    messagebox.showinfo("Info", "Data refreshed!")

def show_latest():
    quake = df.iloc[0]
    messagebox.showinfo("Latest Quake", quake.to_string())

def show_biggest():
    quake = df.loc[df["Magnitude"].idxmax()]
    messagebox.showinfo("Biggest Quake", quake.to_string())

def show_all():
    window = tk.Toplevel(root)
    window.title("Last 500 Quakes")

    text_widget = tk.Text(window, wrap="none", width=150)
    text_widget.insert(tk.END, df.to_string(index=True))
    text_widget.pack(expand=True, fill="both")
def save_to_csv():
    df.to_csv("latest_earthquakes.csv", index=False)
    messagebox.showinfo("Save CSV", "Data saved to latest_earthquakes.csv")

def open_map():
    map_center = [38.0, 35.0]
    m = folium.Map(location=map_center, zoom_start=5)

    for idx, row in df.iterrows():
        folium.CircleMarker(
            location=[row["Latitude(N)"], row["Longitude(E)"]],
            radius=row["Magnitude"] * 2,
            popup=f"""
            Location: {row['Location']}<br>
            Magnitude: {row['Magnitude']}<br>
            Depth: {row['Depth(km)']} km
            """,
            color="navy",
            fill=True,
            fill_color="darkblue"
        ).add_to(m)

    filepath = os.path.abspath("earthquake_map.html")
    m.save(filepath)
    webbrowser.open(f"file://{filepath}")
    messagebox.showinfo("Map", "Map saved and opened in your browser.")

root = tk.Tk()
root.title("Kandilli Earthquake Viewer")
label = tk.Label(root, text="Welcome! You can check the latest 500 earthquakes.")
label.pack(padx=10, pady=10)

refresh = tk.Button(root, text="Refresh Data", command=refresh_)
refresh.pack(padx=10, pady=10)

all = tk.Button(root, text="Show All", command=show_all)
all.pack(padx=10, pady=10)

latest = tk.Button(root, text="Show Latest Quake", command=show_latest)
latest.pack(padx=10, pady=10)

biggest = tk.Button(root, text="Show Biggest Quake", command=show_biggest)
biggest.pack(padx=10, pady=10)

save = tk.Button(root, text="Save CSV", command=save_to_csv)
save.pack(padx=10, pady=10)

map_button = tk.Button(root, text="Show Map", command=open_map)
map_button.pack(padx=10, pady=10)

exit = tk.Button(root, text="Exit", command=root.quit)
exit.pack(padx=10, pady=10)

root.mainloop()
