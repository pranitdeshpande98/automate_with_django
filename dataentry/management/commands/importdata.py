import csv
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.db import DataError

## The proposed custom command is python manage.py importdata filepath modelname
class Command(BaseCommand):

    help = 'To insert data from csv to the database'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='Path to the CSV file')
        parser.add_argument('modelname', type=str, help='Model Name where data will be inserted')

    def handle(self, *args,**kwargs):
        filepath = kwargs['filepath']
        modelname = kwargs['modelname'].capitalize()
        model = None
        ## Search for the model across all the installed and configured apps in the project
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label,modelname)
                break
            except LookupError:
                continue  ## model not found then continue in all the apps in the project to get the model name 

        if not model:
            raise CommandError(f'Model "{modelname}" not found in any of the apps')
        

        
        model_fields = [field.name for field in model._meta.fields if field.name != 'id']

        with open (filepath,'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames
            ## Compare CSV header with model fieldnames

            if csv_header != model_fields:
                raise DataError(f"CSV file does not match with the given {modelname} table fields")
            for row in reader:
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS("Data Imported from CSV Successfully!"))
