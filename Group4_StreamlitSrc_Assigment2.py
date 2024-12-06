import time
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import statsmodels.api as sm

#importing the data through a scriot
import prep
import map_data as md
import machine_learning_data as ml

def main():
    data = prep.read_and_preprocess_data()
    
    #header
    st.markdown("**Group 4**")
    st.markdown("Roberto Delan, Amanda Holsteinson, Maud Lecerf, Christopher Stephan, Max Uebele")
    
    image = Image.open("bikes.jpg")
    st.image(image, use_column_width=True)

    st.header("Analysis of the Bike Sharing Service in 2011 and 2012 in Washington D.C.")
    
    
    
    #creating a sidebar to filter the rental type
    RENTAL_TYPE = st.sidebar.selectbox("Type of rentals to analyze",["Total", "Registered", "Casual"])
    
    
    #creating a slider to filter out a frame of dates
    start_date = data["date"].min().date() 
    end_date = data["date"].max().date()    
    DATE_RANGE = st.sidebar.slider("Date Range:",min_value=start_date,max_value=end_date, value=(start_date, end_date), format="YYYY-MM-DD")

    #creating a dataframe that uses the slider and select box in the sidebar
    aux = data[(data["date"] >= pd.to_datetime(DATE_RANGE[0])) & (data["date"] <= pd.to_datetime(DATE_RANGE[1]))]
    
    
    
    #figure 1: time series
    fig1 = px.line(aux,
        x="date",
        y=RENTAL_TYPE,
        title="{} Rentals".format(RENTAL_TYPE),
        template="plotly_white")

    fig1.update_xaxes(title="Date")
    fig1.update_yaxes(title= f"{RENTAL_TYPE} Rentals from 2011 to 2012 (all values)")

    st.plotly_chart(fig1, use_container_width=True)
    
    st.write("Overall increasing trend with a clear seasonal pattern. Registered users consistently outnumber casual ones, suggesting a **positive trend for long-term sustainability**.")

    
    #figure 2: monthly rentals 
    monthly = aux.groupby(aux['month']).sum(numeric_only=True)
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
               7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    monthly.index = monthly.index.map(month_names)
    fig2 = px.bar(monthly, y=RENTAL_TYPE, template = 'plotly_white', 
                  title = f"Number of {RENTAL_TYPE} Rentals per Month")
    
    st.plotly_chart(fig2, use_container_width=True)
    
    st.write("We can see **high seasonality** with more rentals between June to August and less rentals between November to February. When looking at Casual users, we see more fluctuations throughout the year, likely influenced by holidays, weather conditions and special events.")
    
    
    # figure 3: daily rentals per hour 
    daily_avg = aux.groupby(['weekday_name'])[['Registered', 'Casual', 'Total']].mean().reset_index()

    weekday_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    daily_avg['weekday_name'] = pd.Categorical(daily_avg['weekday_name'], categories=weekday_order, ordered=True)
    daily_avg = daily_avg.sort_values('weekday_name')

    fig3 = px.line(daily_avg,x='weekday_name',y=RENTAL_TYPE, title=f'Average {RENTAL_TYPE} Rentals Per Day',
        labels={'weekday_name': 'Day of the Week', RENTAL_TYPE: f'Average {RENTAL_TYPE} Rentals'},template='plotly_white')
    overall_avg = daily_avg[RENTAL_TYPE].mean()

    fig3.add_hline(y=overall_avg,line_dash="dash",line_color="#FF1493",
                   annotation_text=f"Overall Avg:{int(overall_avg)}",annotation_position="top left")
    
    fig3.update_layout(xaxis=dict(title="Day of the Week"),yaxis=dict(title=f"Average {RENTAL_TYPE} Rentals per Hour of the Day"))
    st.plotly_chart(fig3, use_container_width=True)
    
    st.write("The repartition of rentals between the days of the week is very different for the Casual and Registered users. One area to focus on could be **finding casual users that would use the bikes during the week**, such as tourists that come for extended holidays. Another area to focus on would be **having more registered users during the weekend**, with promotions on the weekends for example, depending on the subscription system.")
    
    
    #figure4: 
    hourly_avg_by_day = aux.groupby(['weekday', 'hour'])[RENTAL_TYPE].mean().reset_index()

    hourly_avg_by_day['weekday'] = hourly_avg_by_day['weekday'].map({
        1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 0: 'Sunday'})

    fig4 = px.line(hourly_avg_by_day, x='hour', y=RENTAL_TYPE, color='weekday', 
                  title=f'Average {RENTAL_TYPE} Bike Rentals by Hour for Each Day of the Week',
                  labels={'hour': 'Hour of the Day', 'Total': 'Average Total Rentals', 'Casual': 'Average Casual Rentals',
                          'Registered': 'Average Registered Rentals','weekday': 'Day of the Week'},
                  template = 'plotly_white')
    fig4.update_layout(xaxis=dict(dtick=1))
    
    st.plotly_chart(fig4, use_container_width=True)
    
    st.write("We have **distinct hour peaks**, 2 for the weekdays and 1 for the weekend, **coincidental with registered and casual users**. For the registered users during the week, we can attribute the peaks to commute times. ")
    
    
    #figure 5
    fig5 = px.box(aux, x='weather_situation_name', y=RENTAL_TYPE,
        category_orders={'season_name': ['Clear', 'Misty', 'Light Rain', 'Heavy Rain']},
        title=f"Distribution of {RENTAL_TYPE} Rentals by Weather Situation")

    fig5.update_layout(template="plotly_white", xaxis_title="Weather Situation", yaxis_title="Total Rentals", font=dict(size=14))
    st.plotly_chart(fig5, use_container_width=True)
    
    st.write("""
    Weather Situation Definition: 
    - **Clear**: Clear, Few clouds, Partly cloudy, Partly cloudy
    - **Mist**: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
    - **Light Rain**: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
    - **Heavy Rain**: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
    """)
    
    st.write("As can be expected, there are much less rentals in a *Heavy Rain* period. There are also much less casual rentals in *Light Rain* and *Heavy Rain* than there are registered rentals. Registered users might be less able to postpone their trip or change their transportation type in case of bad weather conditions than casual users.")
    
    
    #figure 6: scatterplot relations
    fig6 = px.scatter(aux, x= 'atemperature_celsius', y = RENTAL_TYPE, template = 'plotly_white', 
           trendline = 'ols', trendline_color_override = '#FF1493', 
           title = f'Relationship Between the Feeling Temperature in Celsius and the {RENTAL_TYPE} Rentals')
    
    trendline_results = px.get_trendline_results(fig6)
    ols_model = trendline_results.iloc[0]["px_fit_results"]
    slope = ols_model.params[1]
    intercept = ols_model.params[0]
    
    fig6.add_annotation(x=35,  y=150,  text= f"<b>y = {slope:.2f}x + {intercept:.2f}</b>",
                        showarrow=False,font=dict(color="#FF1493", size=18), align="right")
    st.plotly_chart(fig6, use_container_width=True)
    
    st.write('As can be expected, we have a **positive correlation between temperature and number of users**. However the intercept is negative for Casual rentals, showing that casual users will only ride in a nicer temperature whereas Registered user adapt more to the temperature and weather conditions.')
    
    
    
    #Business Insights 
    st.header('Business Recommendations')
    
    
    #business solution 1
    st.subheader('📈Dynamic Pricing to increase the number of users💰')
    
    st.write('By **adapting the pricing strategy based on the number of users during the day**, we can either control the demand to ensure supply, or incentivize users to take bikes during low-demand periods. This would only work for casual users as registered users probably have a subscription.')
    st.write('For registered users, we can give a **discount** for winter months **where there is less demand**. If the subscription is weekly, a ML model could predict what weeks will have less demands to offer discounts for those weeks.')
    
    st.success("Solution: Creation of an ML model to determine demand")
    
    
    #business solution 2
    st.subheader('🔧Predictive Maintenance and Bike Relocation🚚')
    
    st.write("As seen previously Registered users and Casual users have very different behaviours regarding the bike sharing service.A good way to make sure that demand is always met is to **plan maintenance** and **bike relocation from one place to another**")
    
    st.markdown("""
    *For example:
    - We know that the casual users use the bikes more between 10am and 4pm, mostly on weekends, whereas registered users use them mostly to commute before 9 am and after 4pm. 
    - One solution would be to plan transport of the bikes from a more business area to a more touristic area from 9am to 10pm and move the bikes back around 4pm, to ensure that all demand is met.* 
    """)
    
    #map with localisations of the bike share services, and weather they are in a turistic area or not
    df = md.map_data_import()
    coordinates = md.map_coordinates_tourism()
    df['TOURISTIC_NEAR'] = df.apply(lambda row: md.is_near_coordinates(row['LATITUDE'], row['LONGITUDE'], coordinates), axis=1)
    
    fig7 = px.scatter_mapbox(df, lat="LATITUDE", lon="LONGITUDE",
                       hover_name="NAME",  
                       hover_data=["STATION_ID"],  
                       color="TOURISTIC_NEAR", 
                       zoom=10, height=600) 
    fig7.update_layout(mapbox_style="carto-positron") 
    fig7.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    st.subheader('Map of the Bike Sharing Stations in Washington D.C.(2024)')
    st.plotly_chart(fig7, use_container_width=True)
    
    url = 'https://opendata.dc.gov/datasets/DCGIS::capital-bikeshare-locations/about'
    st.write("[Bike Share Map Data](%s)" % url)
     
    st.write(" To be able to correctly plan **maintenance** and **bike relocation** we need to be able to predict the rentals per hour of the day, for the total, registered and casual users.")
    
    st.success("Solution: Creation of an ML model to determine those values")

    
    #ML Modeling
    st.header('Machine Learning Predictions')
    
    st.write("To help predict demand to implement the previous business solutions, we tested Machine Learning models and determined the best one.")
             
    st.write("Best Model: XGBoost Grid Search with Cross Validation")
    
    st.markdown("""
| **Hyperparameters/Score**          | **Total**       | **Casual**      | **Registered**  |
|------------------------------------|-----------------|-----------------|-----------------|
| xgb_colsample_bytree               | 0.99            | 0.99            | 0.99            |
| xgblearning_rate                   | 0.20            | 0.10            | 0.10            |
| xgbmax_depth                       | 20              | 20              | 20              |
| xgbmin_child_weight                | 1               | 1               | 1               |
| xgbn_estimators                    | 100             | 100             | 100             |
| xgb_subsample                      | 0.99            | 0.80            | 0.80            |
| **Test Set MAE Score with Best Model**   | **0.84**        | **0.55**        | **1.13**        |
| **Total MAPE Score with Best Model**   | **0.46%**        | **13.77%**        | **0.83%**        |
    """)
    
    
    #ML results 
    xgb = ml.ml_data_import()
    
    fig8 = px.scatter(
    xgb,
    x=f"{RENTAL_TYPE} Prediction",
    y=RENTAL_TYPE,
    title=f"{RENTAL_TYPE} Users: Predictions vs. Actuals",
    labels={'y_test': RENTAL_TYPE, f"{RENTAL_TYPE} Prediction": f"Predicted {RENTAL_TYPE}"})

    fig8.add_scatter(
        x=xgb[f"{RENTAL_TYPE} Prediction"],
        y=xgb[f"{RENTAL_TYPE} Prediction"],  # Perfect predictions would follow this line
        mode='lines',
        name='Ideal Line',
        line=dict(color='#FF1493', width=3))
    
    st.plotly_chart(fig8, use_container_width=True)
    
    st.success("The predictions are following the test values very closely.")
    st.write('The Casual Predictions are furher from the line, showing the model performs less well. This is due to the casual data having less value, due to a lower number of casual users.')
             
    st.title('Conclusion')
    st.write('By looking at the original data, we were able to understand the behaviour of users, allowing us to create tailored business insights that can increase revenue. By using machine learning models, we are able to predict the demand and implement our business solutions: **dynamic pricing** and **predictive maintenance and transportation**.')


 ##########################################################


if __name__ == "__main__":
    # This is to configure some aspects of the app
    st.set_page_config(
        layout="wide", page_title="Bike Sharing Analysis", page_icon=":bike:"
    )

    # Write titles in the main frame and the side bar
    st.title("Bike Sharing Analysis")
    st.sidebar.title("Options")

    # Call main function
    main()


