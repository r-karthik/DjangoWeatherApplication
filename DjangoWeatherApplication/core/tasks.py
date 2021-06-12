from celery import shared_task
from django.core.mail import EmailMessage
from time import sleep
from .constants import ActionNames
from .models import WeatherData
import xlwt
from io import BytesIO


@shared_task
def send_email_task(excel_file, emails):
    """
    Sends Email with Excel File attachment to given Email ID's

    :param excel_file: Excel file in Bytes
    :param emails: List of Mail ID's to send Email
    :return: None
    """
    sleep(1)
    mail = EmailMessage(subject=ActionNames.SUBJECT,
                        body=ActionNames.MESSAGE,
                        from_email=ActionNames.FROM_EMAIL,
                        to=emails)
    mail.attach(filename="Weather_Data.xls",
                content=excel_file.getvalue(),
                mimetype='application/vnd.ms-excel')
    mail.send()
    return None


def create_excel(emails):
    """
    Queries WeatherData table & appends the data to excel workbook

    :param emails: List of Mail ID's to send Email
    :return: Boolean
    """

    excel_file = BytesIO()
    weather_data = WeatherData.objects.all()
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Sheetname')
    # Writing data to cells using write function
    worksheet.write(0, 0, 'City')
    worksheet.write(0, 1, 'Json Data')
    # row_count to append data in sequence
    row_count = 1
    for city in weather_data:
        worksheet.write(row_count, 0, city.city_name)
        worksheet.write(row_count, 1, city.data)
        row_count += 1
    workbook.save(excel_file)
    # Calling send_email_task Function
    send_email_task(excel_file, emails)
    return True
