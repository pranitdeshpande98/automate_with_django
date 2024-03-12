from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Sum
from emails.models import Email, EmailTracking, Sent, Subscriber
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
            email_id = email_form.id
            ##handing email sending task to celery
            send_email_task.delay(mail_subject, message, to_email, attachment, email_id)
            ## Display a success message
            messages.success(request,'Email Send Successfully')
            return redirect('send_email')
    else:
        email_form = EmailForm()
        context ={
            'email_form' : email_form,
        }
        return render(request,'emails/send-email.html', context)
    

def track_click(request, unique_id):
    print(request)
    return

def track_open(request, unique_id):
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        if not email_tracking.opened_at:
            email_tracking.opened_at = timezone.now()
            email_tracking.save()
            return HttpResponse("Email Opened Successfully")
        else:
            print("Email Already Opened")
            return HttpResponse("Emailed Already Opened")
    except:
        return HttpResponse("Email Tracking Record Not Found!")

def track_dashboard(request):
    emails = Email.objects.all().annotate(total_sent=Sum('sent__total_sent'))
    context ={
        'emails': emails,
    }
    return render(request,'emails/track_dashboard.html', context)

def track_stats(request, pk):
    email = get_object_or_404(Email, pk=pk)
    sent= Sent.objects.get(email=email)
    context ={
        'email' : email,
        'total_sent' : sent.total_sent,
    }
    return render(request, 'emails/track_stats.html', context)