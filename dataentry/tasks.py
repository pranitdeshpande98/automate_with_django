from stuff.celery import app
import time
from django.core.management import call_command
from django.conf import settings



@app.task
def celery_test_task():
    time.sleep(10)
    return 'Task Executed Successfully'

@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e
    
    ## notify the user by email
    return 'Data imported successfully.'
