from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from rest_framework import status
from django.shortcuts import render

API_KEY = 'a948ab4862c0d6055597ff96bec0f06d'
cities = ['London', 'Paris', 'Mumbai', 'Delhi', 'Kolkata', 'France', 'Tokyo', 'Berlin']


@api_view(['GET'])
def my_view(request):
    return Response(status=status.HTTP_200_OK, data="Hello")


@login_required
@api_view(['GET'])
def get_weather_data(request):
    try:
        data = {}
        for city in sorted(cities):
            response = requests.post('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city, API_KEY))
            response = response.json()
            data[city] = response
        return render(request, 'weather.html', context={'Data': data})
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=e)

