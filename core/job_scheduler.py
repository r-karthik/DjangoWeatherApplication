import requests
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
from core.models import WeatherData
import logging


logger = logging.getLogger(__name__)


API_KEY = 'a948ab4862c0d6055597ff96bec0f06d'
cities = ['London', 'Paris', 'Mumbai', 'Delhi', 'Kolkata', 'France', 'Tokyo', 'Berlin', 'Shanghai', 'Cairo', 'Lagos',
          'Bangalore', 'Bogota', 'Surat', 'Toronto', 'Alexandria', 'Sydney', 'Nairobi', 'Kabul', 'Rome', 'Medellin',
          'Athens', 'Dubai', 'Cali', 'Zibo', 'Yantai', 'Beirut', 'Houston', 'Agra', 'Mecca']


def get_weather_data():
    """
    Deletes Existing records from weatherData table fetches new data & adds it to the table

    :return:
    """

    # Delete Existing Data
    query = WeatherData.objects.all()
    query.delete()
    logger.debug("Weather Data Deleted from DB")
    # Creating Dataframe to append fetched data
    df = pd.DataFrame(columns=["city_name", "data"])
    try:
        for city in sorted(cities):
            response = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city, API_KEY))
            response = response.json()
            df = df.append({'city_name': city, "data": response}, ignore_index=True)
        df_records = df.to_dict("records")
        # Creating WeatherData table objects
        model_instances = [WeatherData(
            city_name=record['city_name'],
            data=record['data'],
        ) for record in df_records]
        # Inserting all the records to table
        WeatherData.objects.bulk_create(model_instances)
        logger.info("Weather Data is Updated to DB")
    except Exception as exception:
        logger.error("Error in get_weather_data: {}".format(exception))


def start():
    """
    Scheduler to run Jobs

    :return:
    """
    scheduler = BackgroundScheduler()
    # Calling get_weather_data funtion for every 30 minutes
    scheduler.add_job(get_weather_data, "interval", minutes=30, id="Update_Data")
    scheduler.start()
    logger.debug("Background Scheduler Started")
