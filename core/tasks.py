import logging
from io import BytesIO
from time import sleep

import xlwt
from celery import shared_task
from django.core.mail import EmailMessage

from .constants import ActionNames
from .models import WeatherData

logger = logging.getLogger(__name__)


@shared_task
def send_email_task(emails):
    """
    Sends Email with Excel File attachment to given Email ID's

    :param emails: List of Mail ID's to send Email
    :return: None
    """
    sleep(1)
    mail = EmailMessage(
        subject=ActionNames.SUBJECT,
        body=ActionNames.MESSAGE,
        from_email=ActionNames.FROM_EMAIL,
        to=emails,
    )
    excel_file = create_excel()
    mail.attach(
        filename="Weather_Data.xls",
        content=excel_file.getvalue(),
        mimetype="application/vnd.ms-excel",
    )
    mail.send()
    logger.debug("Email has been Sent.")
    return True


def create_excel():
    """
    Queries WeatherData table & appends the data to excel workbook

    :return: Excel Bytes
    """

    excel_file = BytesIO()
    weather_data = WeatherData.objects.all()
    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet("Sheetname")
    # Writing data to cells using write function
    worksheet.write(0, 0, "City")
    worksheet.write(0, 1, "Json Data")
    # row_count to append data in sequence
    # row_count = 1
    for row_count, city in enumerate(weather_data, 1):
        worksheet.write(row_count, 0, city.city_name)
        worksheet.write(row_count, 1, city.data)
        # row_count += 1
    workbook.save(excel_file)
    logger.debug("Excel Bytes Generated")
    return excel_file
