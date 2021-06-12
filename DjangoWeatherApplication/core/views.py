import requests
import datetime
import re
import xlsxwriter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from DjangoWeatherApplication.core.models import WeatherData
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

API_KEY = 'a948ab4862c0d6055597ff96bec0f06d'
cities = ['London', 'Paris', 'Mumbai', 'Delhi', 'Kolkata', 'France', 'Tokyo', 'Berlin', 'Shanghai', 'Cairo', 'Lagos',
          'Bangalore', 'Bogota', 'Surat', 'Toronto', 'Alexandria', 'Sydney', 'Nairobi', 'Kabul', 'Rome', 'Medellin',
          'Athens', 'Dubai', 'Cali', 'Zibo', 'Yantai', 'Beirut', 'Houston', 'Agra', 'Mecca']


@api_view(['GET'])
def my_view(request):
    return Response(status=status.HTTP_200_OK, data="Hello")


@api_view(['GET'])
def get_weather_data(request):
    query = WeatherData.objects.all()
    query.delete()
    try:
        for city in sorted(cities):
            response = requests.post('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city, API_KEY))
            response = response.json()
            a = WeatherData(city_name=city, data=str(response))
            a.save()
        return render(request, 'refresh.html', {'Date': datetime.datetime.now()})
    except Exception as exception:
        return render(request, 'refresh.html', {'Exception': exception})


def index(request):
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
    try:
        email = request.GET['email_id']
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", email)
        # create_excel()
        return render(request, "home.html", {"Emails": emails})
    except Exception as exception:
        return render(request, "home.html", {"Exception": exception})


def create_excel():
    weather_data = WeatherData.objects.all()
    workbook = xlsxwriter.Workbook('Weather_Data.xlsx')
    # The workbook object is then used to add new
    # worksheet via the add_worksheet() method.
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'City')
    worksheet.write('B1', 'Json Data')
    count = 2
    for city in weather_data:
        worksheet.write('A{}'.format(count), city.city_name)
        worksheet.write('B{}'.format(count), city.data)
        count += 1
    workbook.close()

