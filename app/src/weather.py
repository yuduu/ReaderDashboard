import os
import requests
from datetime import datetime, timedelta
import pytz
from babel.dates import format_datetime
import matplotlib.pyplot as plt
import io
import numpy as np

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
        hour['dt_raw'] = hour['dt']
        dt_hour = datetime.fromtimestamp(hour['dt']).astimezone(tz)
        hour['dt'] = dt_hour.strftime('%H:%M')

    for day in weather_data['daily']:
        day['dt_raw'] = day['dt']
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


def get_weather_graph():
    data = get_weather()
    # Example data for the plot
    # hours = ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]
    # temperatures = [5, 3, 2, 7, 12, 15, 10, 8]  # Example temperatures in °C
    # rain_chances = [20, 40, 10, 0, 0, 10, 50, 60]  # Rain chances in %

    hours = []
    temperatures = []
    rain_chances = []

    for i in range(0, 24):
        hours.append(data['hourly'][i]['dt'])
        temperatures.append(round(data['hourly'][i]['feels_like']))
        rain_chances.append(data['hourly'][i]['pop']*100)

    # Create figure and axis
    fig, ax1 = plt.subplots(figsize=(6, 3))

    # Plot the temperature as a line on the left Y-axis
    ax1.set_ylabel('Temperature (°C)', color='black')
    ax1.plot(hours, temperatures, color='black', linewidth=2, marker='o', markersize=5)
    ax1.tick_params(axis='y', labelcolor='black')


    # Set the Y-axis range for temperatures, with a margin to accommodate different extremes (-15°C to 40°C)
    ax1.set_ylim(min(temperatures) - 5, max(temperatures) + 5)

    # Create a second Y-axis for the rain chance
    ax2 = ax1.twinx()
    ax2.set_ylabel('Chance of Rain (%)', color='black')

    # Set positions for bars
    bar_positions = np.arange(len(hours))

    # Plot the rain chance as bars on the right Y-axis
    ax2.bar(bar_positions, rain_chances, color='black', alpha=0.6, width=0.5)
    ax2.set_xticks(bar_positions[::3])  # Set x-ticks to every third hour
    ax2.set_xticklabels(hours[::3])  # Set labels for the x-ticks
    ax2.tick_params(axis='y', labelcolor='black')

    # Set Y-axis range for rain chances (0% to 100%)
    ax2.set_ylim(0, 100)

    # Set x-axis limits to start at 00:00 and end at 23:00
    ax2.set_xlim(-0.5, len(hours) - 0.5)  # Adjust x-limits to fit the bars

    # Title and grid for better visibility
    plt.title('Weather Forecast: Temperature and Rain Chance', fontsize=12)
    ax1.grid(True, which='both', linestyle='--', color='gray', alpha=0.5)

    # Remove the background grid
    ax1.grid(False)

    # Improve layout to prevent label cutoff
    plt.tight_layout()

    # Save plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    buffer.seek(0)

    return buffer

if __name__ == '__main__':
    get_weather_graph()
    print(get_current_weather())
    print(get_hourly_weather())
    print(get_daily_weather())