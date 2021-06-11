from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from DjangoWeatherApplication.core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('hello/', login_required(TemplateView.as_view(template_name='hello.html')), name='hello'),
    path('get_weather_data/', login_required(views.get_weather_data), name='weather')
]
