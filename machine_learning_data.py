import time
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import statsmodels.api as sm

def ml_data_import():
    data = pd.read_csv('xgb_chosen.csv')

    
    data = data.rename(columns={
    'xgb_cv_casual': 'Casual',
    'casual_test': 'Casual Prediction',
    'xgb_cv_registered': 'Registered',
    'registered_test': 'Registered Prediction',
    'xgb_cv_total': 'Total',
    'total_test': 'Total Prediction'})
    
    
    return data