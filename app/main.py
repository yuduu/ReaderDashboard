from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, PlainTextResponse
from datetime import datetime
from babel.dates import format_datetime
from app.src.weather import get_weather, get_current_weather, get_hourly_weather, get_daily_weather
from app.src.compliments import select_random_compliment
from app.src.transit import get_departure_html


app = FastAPI()

# Create your main app
app = FastAPI()

# Add Jinja Template directory
templates = Jinja2Templates(directory="templates")


# Mount the static files under the /static route
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    response = templates.TemplateResponse(request, "home.html")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.get("/time", response_class=HTMLResponse)
async def get_time():
    current_time = format_datetime(datetime.now(), format='H:mm', locale='de')
    return current_time

@app.get("/date", response_class=HTMLResponse)
async def get_date():
    current_date = format_datetime(datetime.now(), format='EEEE, d. MMMM', locale='de')
    return current_date

@app.get("/weather")
async def get_weather_data():
    weather = get_weather()
    return weather

@app.get("/weather-current", response_class=HTMLResponse)
async def get_current_weather_data():
    current_weather = get_current_weather()
    return current_weather

@app.get("/weather-hourly", response_class=HTMLResponse)
async def get_hourly_weather_data():
    hourly_weather = get_hourly_weather()
    return hourly_weather


@app.get("/weather-daily", response_class=HTMLResponse)
async def get_daily_weather_data():
    daily_weather = get_daily_weather()
    return daily_weather

@app.get("/compliment", response_class=HTMLResponse)
async def get_compliment_data():
    compliments_file = "app/src/util/compliments.txt"
    selected_compliment = select_random_compliment(compliments_file)
    return selected_compliment


@app.get("/departures", response_class=HTMLResponse)
async def get_departure_data():
    departures = get_departure_html()
    return departures


if __name__ == "__main__":
    pass