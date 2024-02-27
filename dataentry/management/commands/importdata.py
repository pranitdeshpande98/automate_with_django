import csv
from django.core.management.base import BaseCommand, CommandParser
from dataentry.models import Student

## The proposed custom command is python manage.py importdata filepath
class Command(BaseCommand):

    help = 'To insert data from csv to the database'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='Path to the CSV file')

    def handle(self, *args,**kwargs):
        filepath = kwargs['filepath']
        with open (filepath,'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Student.objects.create(**row)
        self.stdout.write(self.style.SUCCESS("Data Imported from CSV Successfully!"))
