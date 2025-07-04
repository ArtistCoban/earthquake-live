# Kandilli Earthquake Viewer

## Requirements
Python 3.8+  
Packages: `requests`, `beautifulsoup4`, `pandas`, `folium`

## Installation
pip install -r requirements.txt

## Running the Application
python app.py

## Creating an EXE
pyinstaller --onefile --noconsole --icon=quake.ico app.py

## Data Source
Earthquake data used in this project is retrieved from the official website of:

**Boğaziçi University Kandilli Observatory and Earthquake Research Institute**  
**Regional Earthquake-Tsunami Monitoring and Evaluation Center**  
http://www.koeri.boun.edu.tr/scripts/lst9.asp

Used for educational purposes only; not for commercial use.

> © Boğaziçi University Rectorate – All rights reserved.