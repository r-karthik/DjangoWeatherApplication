import logging
import re

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from core.models import WeatherData

from .tasks import send_email_task

logger = logging.getLogger(__name__)


@login_required
def index(request):
    """
    Used to Paginate & Display weather data of 10 cities per page

    :param request: HTTP Request
    :return: Renders weather.html page
    """
    weather_data = WeatherData.objects.all()
    page = request.GET.get("page", 1)
    paginator = Paginator(weather_data, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, "weather.html", {"post_list": users})


@login_required
def form_data(request):
    """
    Fetches data from Form, Validates Email's using Regex & calls
    create_excel function

    :param request: HTTP Request
    :return: Renders home.html page
    """
    try:
        # Get Input from the form
        email = request.GET["email_id"]
        # Regular Expression to Extract & validate Email ID's from string
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", email)
        if_mail_sent = send_email_task(emails)
        if if_mail_sent:
            return render(
                request,
                "home.html",
                {"Emails": emails, "Message": "Email has been sent to:"},
            )
        return render(
            request,
            "home.html",
            {
                "Emails": emails,
                "Message": "Sending Email has failed. Please try again.",
            },
        )
    except Exception as exception:
        logger.warning(f"Warning in form_data: {exception}")
        return render(request, "home.html", {"Exception": exception})
