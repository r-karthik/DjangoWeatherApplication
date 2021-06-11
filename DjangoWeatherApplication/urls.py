from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from DjangoWeatherApplication.core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
    path('', login_required(views.form_data), name='home'),
    path('list/', login_required(views.index), name='weather'),
    path('refresh/', login_required(views.get_weather_data), name='weather_data'),
]
