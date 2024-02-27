from django.core.management.base import BaseCommand

from dataentry.models import Student

class Command(BaseCommand):
    help = 'To insert data to the database'

    def handle(self, *args, **kwargs):

        dataset = [
            {'roll_no': 1002, 'name': 'Sachin', 'age': 28},
            {'roll_no': 1003, 'name': 'Virat', 'age': 34},
            {'roll_no': 1004, 'name': 'Rohit', 'age': 37},
            {'roll_no': 1005, 'name': 'Ravindra', 'age': 29},
        ]
        for data in dataset:
            roll_no = data['roll_no']
            existing_record = Student.objects.filter(roll_no=roll_no).exists()

            if not existing_record:
                Student.objects.create(roll_no=data['roll_no'], name=data['name'], age=data['age'])
            else:
                self.stdout.write(self.style.WARNING(f"Student with roll number {roll_no} already exists in the database"))
        self.stdout.write(self.style.SUCCESS("Data Entered Successfully!"))