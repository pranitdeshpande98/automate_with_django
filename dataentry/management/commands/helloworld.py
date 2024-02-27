from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "To print Hello World on the terminal"

    def handle(self,*args,**kwargs):
        self.stdout.write("Hello World")