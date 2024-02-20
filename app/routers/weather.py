from fastapi import APIRouter
import requests
import pandas as pd
from starlette.responses import FileResponse

from app.config import settings

API_KEY = settings.weather_api_key
BASE_URL = 'http://api.weatherapi.com/v1'

# Assuming the endpoint for future weather forecast allows specifying a range or getting extended forecasts
forecast_days = 3  # free plan only gives 3 days
location = 'Sari'  # Specify the location

# Construct the URL
url = f"{BASE_URL}/forecast.json?key={API_KEY}&q={location}&days={forecast_days}"

router = APIRouter(
    tags=['Weather Forcast']
)


@router.get('/bot')
async def fetch_weather_data_and_save():
    response = requests.get(url)
    data = response.json()
    print(data)

    # Example of processing and saving the data
    # Adjust the parsing according to the actual structure of your API response
    df = pd.DataFrame(columns=['Date', 'MaxTemp', 'MinTemp', 'Condition'])
    for day in data['forecast']['forecastday']:
        date = day['date']
        max_temp = day['day']['maxtemp_c']
        min_temp = day['day']['mintemp_c']
        condition = day['day']['condition']['text']
        df = df._append({'Date': date, 'MaxTemp': max_temp, 'MinTemp': min_temp, 'Condition': condition},
                        ignore_index=True)

    # Save to CSV
    csv_file_name = 'time.csv'
    df.to_csv(csv_file_name, index=False)

    # Return the CSV file as a response
    return FileResponse(csv_file_name, media_type='text/csv', filename=csv_file_name)
