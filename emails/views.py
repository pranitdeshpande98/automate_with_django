from django.shortcuts import redirect, render

from emails.models import Subscriber
from emails.tasks import send_email_task
from . forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
# Create your views here.
def send_email(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email_form = email_form.save()
            ## Sending an email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            email_list = request.POST.get('email_list')
            ## Access the list
            email_list = email_form.email_list

            ## Extract Email Addresses from the subscriber model from accessed abovelist
            subscribers = Subscriber.objects.filter(email_list=email_list)
            to_email = [email.email_address for email in subscribers]

            if email_form.attachment:
                attachment = email_form.attachment.path
            else:
                attachment = None
            
            ##handing email sending task to celery
            send_email_task.delay(mail_subject, message, to_email, attachment)
            ## Display a success message
            messages.success(request,'Email Send Successfully')
            return redirect('send_email')
    else:
        email_form = EmailForm()
        context ={
            'email_form' : email_form,
        }
        return render(request,'emails/send-email.html', context)