from django.db import models


class WeatherData(models.Model):
    id = models.BigAutoField(primary_key=True)
    city_name = models.CharField(max_length=30)
    data = models.CharField(max_length=300)
