from stuff.celery import app
import time
from django.core.management import call_command
from django.conf import settings
from django.core.mail import EmailMessage
from . utils import send_email_notification

@app.task
def celery_test_task():
    time.sleep(10)
    mail_subject = 'Test Subject'
    message = 'This is some test email'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email)
    return 'Email Sent Successfully'

@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e
    
    ## notify the user by email
    mail_subject = 'Import Data Completed'
    message = 'Your Data Import has been successfully completed'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email)
    return 'Data imported successfully.'
