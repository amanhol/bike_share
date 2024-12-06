import time
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image


def read_and_preprocess_data():
    
    bike_data = pd.read_csv("bike-sharing-hourly.csv", sep = ',')
    
    bike_data = bike_data.rename(columns={
    'yr': 'year',
    'mnth': 'month',
    'hr': 'hour',
    'hum': 'humidity',
    'cnt': 'Total',
    'atemp': 'atemperature',
    'temp': 'temperature',
    'weathersit': 'weather_situation',
    'dteday': 'date', 
    'registered': 'Registered', 
    'casual': 'Casual'})
    
    bike_data['date'] = pd.to_datetime(bike_data['date'])
 
    #creating a dataframe made for graphs, that will not be used in preprocessing
    graph_data = bike_data.copy()

    graph_data['temperature_celsius'] = graph_data['temperature']*41
    graph_data['atemperature_celsius'] = graph_data['atemperature']*50
    graph_data['humidity_percent'] = graph_data['humidity']/100
    graph_data['windspeed_kmh'] = graph_data['windspeed']*67
    graph_data['weekday_name'] = graph_data['weekday'].map({0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'})
    graph_data['month_name'] = graph_data['month'].map({1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                                                        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'})
    graph_data['season_name'] = graph_data['season'].map({1: 'Winter', 2:'Spring', 3:'Summer', 4:'Fall' })
    graph_data['weather_situation_name'] = graph_data['weather_situation'].map({1: 'Clear', 2:'Mist', 3:'Light Rain', 4:'Heavy Rain' })

    return graph_data
