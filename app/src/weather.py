import os
import requests
from datetime import datetime, timedelta
import pytz
from babel.dates import format_datetime

# Global variables to store cached data and timestamp
cached_weather_data = None
last_update_time = None

def get_weather():
    global cached_weather_data, last_update_time

    # Check if we have cached data and if it is less than an hour old
    if cached_weather_data and last_update_time and datetime.now() - last_update_time < timedelta(hours=1):
        return cached_weather_data

    # Fetch new data from the API
    appid = os.getenv('WEATHER_APPID', 'default_appid')
    lat = os.getenv('WEATHER_LAT', 'default_lat')
    lon = os.getenv('WEATHER_LON', 'default_lon')
    units = os.getenv('WEATHER_UNITS', 'metric')
    lang = os.getenv('WEATHER_LANG', 'de')

    tz = pytz.timezone('Europe/Berlin')
    url = 'https://api.openweathermap.org/data/3.0/onecall'
    params = {
        'appid': appid,
        'lat': lat,
        'lon': lon,
        'units': units,
        'lang': lang,
        'exclude': 'minutely,alerts'
    }
    response = requests.get(url, params=params)
    weather_data = response.json()
    
    for hour in weather_data['hourly']:
        dt_hour = datetime.fromtimestamp(hour['dt']).astimezone(tz)
        hour['dt'] = dt_hour.strftime('%H:%M')

    for day in weather_data['daily']:
        timezone = datetime.fromtimestamp(day['dt']).astimezone(tz)
        day['dt'] = format_datetime(timezone, format='E', locale='de').strip('.')

    # Update the cached data and timestamp
    cached_weather_data = weather_data
    last_update_time = datetime.now()

    return weather_data

def get_current_weather():
    data = get_weather()
    temp = round(data['current']['temp'])
    ico = data['current']['weather'][0]['id']
    like = round(data['current']['feels_like'])
    html = f"""
        <div id="current-weather">
            <span id="current-weather-ico"><i class="wi wi-owm-day-{ico}"></i></span>
            <span id="current-temp">{temp}°</span>
        </div>
        <div id="current-weather-feel">
            <span>Feels Like:</span>
            <span id="current-feels-like-temp">{like}°</span>
        </div>
    """
    return html

def get_hourly_weather():
    data = get_weather()
    html = ""
    for i in range(1, 12, 2):
        html += f"""
            <div class="box">
                <div class="weather-forecast-hourly center">{data['hourly'][i]['dt']}</div>
                <div class="weather-forecast-hourly center">{round(data['hourly'][i]['temp'])}°</div>
                <div class="weather-forecast-hourly center"><i class="wi wi-owm-{data['hourly'][i]['weather'][0]['id']}"></i></div>
            </div>
        """
    return html

def get_daily_weather():
    data = get_weather()
    html = ""
    for i in range(1, 7):
        html += f"""
            <div class="container border">
                <div class="box forecast-box">{data['daily'][i]['dt']}</div>
                <div class="box"><i class="wi wi-owm-{data['daily'][i]['weather'][0]['id']}"></i></div>
                <div class="box">{round(data['daily'][i]['temp']['min'])}</div>
                <div class="box">{round(data['daily'][i]['temp']['max'])}</div>
            </div>
        """
    return html

if __name__ == '__main__':
    print(get_current_weather())
    print(get_hourly_weather())
    print(get_daily_weather())