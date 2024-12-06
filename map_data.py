import time
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import statsmodels.api as sm

def map_data_import():
    data = pd.read_csv('Capital_Bikeshare_Locations_cleaned.csv')
    return data

def map_coordinates_tourism(): 
    coordinates = [
    {"latitude": 38.8977, "longitude": -77.0365},  # The White House
    {"latitude": 38.8893, "longitude": -77.0502},  # Lincoln Memorial
    {"latitude": 38.8899, "longitude": -77.0091},  # United States Capitol
    {"latitude": 38.8895, "longitude": -77.0353},  # Washington Monument
    {"latitude": 38.8882, "longitude": -77.0199},  # Smithsonian National Air and Space Museum
    {"latitude": 38.8913, "longitude": -77.0261},  # National Museum of Natural History
    {"latitude": 38.8913, "longitude": -77.0199},  # National Gallery of Art
    {"latitude": 38.8814, "longitude": -77.0365},  # Jefferson Memorial
    {"latitude": 38.8898, "longitude": -77.0230},  # The National Mall
    {"latitude": 38.9039, "longitude": -77.0653},  # Georgetown Waterfront Park
    {"latitude": 38.9296, "longitude": -77.0498},  # National Zoo
    {"latitude": 38.8887, "longitude": -77.0047},  # The Library of Congress
    {"latitude": 38.8837, "longitude": -77.0339},  # Tidal Basin
    {"latitude": 38.8790, "longitude": -77.0729}]  # Arlington National Cemetery
    
    return coordinates

def is_near_coordinates(latitude, longitude, coordinates, radius=0.01):
    for coord in coordinates:
        if (abs(latitude - coord['latitude']) <= radius and
            abs(longitude - coord['longitude']) <= radius):
            return True
    return False

#the data was prepared and analysed in the Bike_station_location 
#data from the website: https://opendata.dc.gov/datasets/DCGIS::capital-bikeshare-locations/about