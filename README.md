# 🚲 **Bike Sharing Analysis**  
An interactive Streamlit application that analyzes the behavior of bike-sharing users in Washington D.C. for the years 2011 and 2012. This app provides data-driven insights and predictive models to improve bike-sharing services.

---

## **Features**
- 📊 **Time-Series Analysis**: Visualize trends in total, registered, and casual rentals over time.
- 📅 **Seasonality Insights**: Discover monthly and daily rental patterns.
- 🕒 **Hourly Analysis**: Compare rental behaviors across different times of the day and week.
- 🌦️ **Weather Impact**: Analyze how weather conditions influence bike rentals.
- 🔍 **Business Insights**: Recommendations for dynamic pricing, predictive maintenance, and bike relocation.
- 🤖 **Machine Learning Predictions**: Predict demand using an XGBoost model to inform business strategies.

---

## Data

The app uses bike-sharing data from 2011 and 2012 in Washington D.C.

	•	Data is processed and prepped using custom scripts (prep.py, map_data.py, machine_learning_data.py).

### Machine Learning

The app leverages an XGBoost Model with Grid Search and Cross Validation to predict demand:

	•	Hyperparameters:
	•	max_depth: 20
	•	n_estimators: 100
	•	learning_rate: 0.20 (Total), 0.10 (Casual, Registered)
	•	Performance:
	•	Mean Absolute Error (MAE): 0.84 (Total), 0.55 (Casual), 1.13 (Registered)
	•	Mean Absolute Percentage Error (MAPE): 0.46% (Total), 13.77% (Casual), 0.83% (Registered)

Technologies Used

	•	Frontend: Streamlit
	•	Data Analysis: Pandas, Numpy
	•	Visualizations: Plotly
	•	Machine Learning: XGBoost
	•	Mapping: Plotly Mapbox
	•	Additional Libraries: PIL, Statsmodels


## About

This project was created as part of a group assignment by:

	•	Roberto Delan
	•	Amanda Holsteinson
	•	Maud Lecerf
	•	Christopher Stephan
	•	Max Uebele
