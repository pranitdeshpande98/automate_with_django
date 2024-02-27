from django.core.management.base import BaseCommand
import csv
from dataentry.models import Student, Customer
import datetime

class Command(BaseCommand):
    help = 'Command to Export Data from Student Table to CSV Database'

    def handle(self,*args,**kwargs):
        ## first retrieve the data from database
        students = Student.objects.all()
  
        ## Define the csv file and filepath
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filepath = f'exported_data_data_{timestamp}.csv'

        ## Open the csv file and then save the data
        with open(filepath,'w',newline='') as file:
            writer = csv.writer(file)

            ## write the csv header
            writer.writerow(['Roll No', 'Name', 'Age'])

            #write data rows
            for student in students:
                writer.writerow([student.roll_no,student.name,student.age])

        self.stdout.write(self.style.SUCCESS('Data Exported Successfully!'))

        

