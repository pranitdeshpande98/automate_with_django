import csv
import datetime
import os
from django.apps import apps
from django.db import DataError
from django.core.management import CommandError
from django.conf import settings
from django.core.mail import EmailMessage

from emails.models import Email, Sent

def get_all_custom_models():
    default_models = ['Session', 'ContentType','LogEntry','Group', 'Permission', 'User', 'Upload']
    custom_models = []

    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
    return custom_models


def check_csv_errors(file_path,model_name):
    model = None
        ## Search for the model across all the installed and configured apps in the project
    for app_config in apps.get_app_configs():
        try:
            model = apps.get_model(app_config.label,model_name)
            break
        except LookupError:
            continue  ## model not found then continue in all the apps in the project to get the model name 

    if not model:
        raise CommandError(f'Model "{model_name}" not found in any of the apps')
    

    model_fields = [field.name for field in model._meta.fields if field.name != 'id']

    try:
        with open (file_path,'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames
            ## Compare CSV header with model fieldnames

            if csv_header != model_fields:
                raise DataError(f"CSV file does not match with the given {model_name} table fields")
    except Exception as e:
        raise e
    
    return model


def send_email_notification(mail_subject, message, to_email, attachment=None, email_id=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=to_email)
        if attachment is not None:
             mail.attach_file(attachment)
        mail.content_subtype = "html"
        mail.send()

        ## Store the total sent emails in the sent model
        email = Email.objects.get(pk=email_id)
        sent = Sent()
        sent.email = email
        sent.total_sent = email.email_list.count_emails()
        sent.save()
    except Exception as e:
        raise e
    
def generate_csv_file(model_name):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    export_dir = 'exported_data'
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    return file_path