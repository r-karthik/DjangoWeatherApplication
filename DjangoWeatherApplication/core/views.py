import requests
import datetime
import re
from rest_framework.decorators import api_view
from django.shortcuts import render
from DjangoWeatherApplication.core.models import WeatherData
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .tasks import create_excel

API_KEY = 'a948ab4862c0d6055597ff96bec0f06d'
cities = ['London', 'Paris', 'Mumbai', 'Delhi', 'Kolkata', 'France', 'Tokyo', 'Berlin', 'Shanghai', 'Cairo', 'Lagos',
          'Bangalore', 'Bogota', 'Surat', 'Toronto', 'Alexandria', 'Sydney', 'Nairobi', 'Kabul', 'Rome', 'Medellin',
          'Athens', 'Dubai', 'Cali', 'Zibo', 'Yantai', 'Beirut', 'Houston', 'Agra', 'Mecca']


@api_view(['GET'])
def get_weather_data(request):
    """
    Used to Fetch Weather Data from openweathermap.org website

    :param request: HTTP Request
    :return: Renders refresh.html page
    """

    # Query WeatherData table & delete all rows
    query = WeatherData.objects.all()
    query.delete()
    try:
        # Iterate Over all the cities & Fetch weather data using city & API_KEY
        for city in sorted(cities):
            response = requests.post('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city, API_KEY))
            response = response.json()
            a = WeatherData(city_name=city, data=str(response))
            a.save()  # Saving the Data to DB
        return render(request, 'refresh.html', {'Date': datetime.datetime.now()})
    except Exception as exception:
        return render(request, 'refresh.html', {'Exception': exception})


def index(request):
    """
    Used to Paginate & Display weather data of 10 cities per page

    :param request: HTTP Request
    :return: Renders weather.html page
    """
    weather_data = WeatherData.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(weather_data, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'weather.html', {'post_list': users})


def form_data(request):
    """
    Fetches data from Form, Validates Email's using Regex & calls create_excel function

    :param request: HTTP Request
    :return: Renders home.html page
    """
    try:
        # Get Input from the form
        email = request.GET['email_id']
        # Regular Expression to Extract & validate Email ID's from string
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", email)
        if_mail_sent = create_excel(emails)
        if if_mail_sent:
            return render(request, "home.html", {"Emails": emails,
                                                 "Message": "Email has been sent to:"})
        return render(request, "home.html", {"Emails": emails,
                                             "Message": "Sending Email has failed. Please try again."})
    except Exception as exception:
        return render(request, "home.html", {"Exception": exception})
