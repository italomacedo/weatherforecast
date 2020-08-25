import pandas as pd
import numpy as np
import requests
from sklearn.linear_model import LinearRegression
from io import StringIO

campaign_text = StringIO("accountId, adgroupId, campaignId, keywordId\n1, 2, 1, 1")
features_campaign = pd.read_csv(campaign_text, sep=",")
key = ''    
date = '2020-08-25'
weather_sample = pd.read_csv("C:/italomacedo/git/weatherforecast/resources/data.csv")

def main():
    weather_targets = weather_sample[['clicks', 'impressions']]
    weather_features = weather_sample[['accountId', 'adgroupId', 'campaignId', 'keywordId', 'Precipitation', 'Wind Gust',	'Cloud Cover',	'Relative Humidity']]

    linear_regression = LinearRegression()
    #weather_features = weather_features.apply(pd.to_numeric, errors='coerce')
    #weather_features.fillna(0, inplace=True)

    #regression model defined
    linear_regression.fit(weather_features, weather_targets)
    
    r = requests.get('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?&aggregateHours=24&startDateTime='+date+'T00:00:00&endDateTime='+date+'T00:00:00&unitGroup=uk&contentType=csv&dayStartTime=0:0:00&dayEndTime=0:0:00&location=Gustav%20Adolfs%20torg,%20Stockholm&key='+key)
    
    weather_text = StringIO(r.text)
    weather_frame = pd.read_csv(weather_text, sep=",")

    features_weather = weather_frame[['Precipitation', 'Wind Gust',	'Cloud Cover',	'Relative Humidity']]

    input_frame = pd.concat([features_campaign,features_weather], axis=1)
    input_frame.fillna(0, inplace=True)

    weather_predicts = linear_regression.predict(input_frame)
    print(weather_predicts)


if __name__ == '__main__':
    main()
