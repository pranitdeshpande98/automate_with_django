import csv
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.db import DataError

from dataentry.utils import check_csv_errors

## The proposed custom command is python manage.py importdata filepath modelname
class Command(BaseCommand):

    help = 'To insert data from csv to the database'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='Path to the CSV file')
        parser.add_argument('modelname', type=str, help='Model Name where data will be inserted')

    def handle(self, *args,**kwargs):
        filepath = kwargs['filepath']
        modelname = kwargs['modelname'].capitalize()

        model = check_csv_errors(filepath,modelname)
        with open(filepath,'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS("Data Imported from CSV Successfully!"))
