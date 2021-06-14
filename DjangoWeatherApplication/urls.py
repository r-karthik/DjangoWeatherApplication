from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path

from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", login_required(views.form_data), name="home"),
    path("list/", login_required(views.index), name="weather"),
]
