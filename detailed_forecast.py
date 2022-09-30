import requests
import os
from datetime import datetime
from pprint import pprint

url = 'https://api.openweathermap.org/data/2.5/forecast'
# key = os.environ.get('WEATHER_KEY')
key = 'cef1079916e0dbcd5eed83f42cd53f1e'


def main():
    location = get_location()
    weather_data, error = get_current_weather(location, key)
    if error:
        print('Sorry, could not get weather')
    else:
        get_forecast(weather_data)


def get_location():
    city, country = '', ''
    while len(city) == 0:
        city = input('Enter the name of the city: ').strip()
    
    while len(country) != 2 or not country.isalpha():
        country = input('Enter the 2-letter counry code: ').strip()

    location = f'{city},{country}'
    return location


def get_current_weather(location, key):
    try:
        query={'q': location, 'units':'imperial', 'appid':key}
        response = requests.get(url, params=query)
        response.raise_for_status()
        data = response.json()
        return data, None
    except Exception as ex:
        print(ex)
        print(response.text)
        return None, ex


def get_forecast(weather_data):
    try:
        list_of_forecasts = weather_data['list']

        for forecast in list_of_forecasts:
            temp = forecast['main']['temp']
            description = forecast['weather'][0]['description']
            wind = forecast['wind']['speed']
            timestamp = forecast['dt']
            forecast_date = datetime.fromtimestamp(timestamp)
            print(f'At {forecast_date} the temperature will be {temp}F, the weather is expected to be {description} , and wind speed is {wind}.')
    except KeyError:
        print('This data is not in the format expected')
        return 'Unknown'



if __name__=='__main__':
    main()