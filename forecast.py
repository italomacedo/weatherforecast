from io import StringIO

import pandas as pd
import sqlite3
import numpy as np
import requests

from sklearn.linear_model import LinearRegression

import pickle

key = 'H3CFB251KRDPFS4KR084UEQMP'
accountId = '1'
futureDate = '2020-08-26'
database_file = "./resources/database.sqlite"
pkl_filename = "./resources/linearregression.pkl"

def loadModel(conn):
    

    try:
        with open(pkl_filename, 'rb') as file:
            pickle_model = pickle.load(file)
        return pickle_model

    except:
        user_features = pd.read_sql_query("select * from user_history;", conn)
        weather_features = pd.read_sql_query("select * from weather_history;", conn)

        campaign_weather_sample = pd.merge(user_features,weather_features, on='day')
    
        campaign_targets = campaign_weather_sample[['clicks', 'impressions']]
        campaign_features = campaign_weather_sample[['accountId', 'adgroupId', 'campaignId', 'keywordId', 'Precipitation', 'Wind Gust',	'Cloud Cover',	'Relative Humidity']]

        linear_regression = LinearRegression()
        campaign_features = campaign_features.apply(pd.to_numeric, errors='coerce')
        campaign_features.fillna(0, inplace=True)

        #regression model defined
        linear_regression.fit(campaign_features, campaign_targets)
        with open(pkl_filename, 'wb') as file:
            pickle.dump(linear_regression, file)

        with open(pkl_filename, 'rb') as file:
            pickle_model = pickle.load(file)

        return pickle_model

def main():
    conn = None

    try:
        conn = sqlite3.connect(database_file)
    except:
         print("Could not connect to database.")
         return

    model = loadModel(conn)    

    campaign_select = pd.read_sql_query("select accountId, adgroupId, campaignId, keywordId, '"+futureDate+"' as date from user_history where accountId = '"+accountId+"'group by accountId, adgroupId, campaignId, keywordId;", conn)
    
    r = requests.get('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?&aggregateHours=24&startDateTime='+futureDate+'T00:00:00&endDateTime='+futureDate+'T00:00:00&unitGroup=uk&contentType=csv&dayStartTime=0:0:00&dayEndTime=0:0:00&location=Gustav%20Adolfs%20torg,%20Stockholm&key='+key)
    weather_text = StringIO(r.text)
    weather_frame = pd.read_csv(weather_text, sep=",")
    weather_join_frame = pd.DataFrame({'date': [futureDate]}, index=[0])
    weather_frame = pd.concat([weather_frame, weather_join_frame], axis=1)
        
    weather_select = weather_frame[['date','Precipitation', 'Wind Gust',	'Cloud Cover',	'Relative Humidity']]
    
    input_frame = pd.merge(campaign_select, weather_select, on='date')
    input_frame.fillna(0, inplace=True)
    
    input_frame = input_frame[['accountId', 'adgroupId', 'campaignId', 'keywordId', 'Precipitation', 'Wind Gust',	'Cloud Cover',	'Relative Humidity']]
    
    campaign_predicts =  pd.DataFrame(model.predict(input_frame))
    
    campaign_predicts = pd.concat([campaign_select, campaign_predicts], axis=1)
    print(campaign_predicts)


if __name__ == '__main__':
    main()
