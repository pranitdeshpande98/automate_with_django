from django.shortcuts import redirect, render
from . forms import EmailForm
from django.contrib import messages
# Create your views here.
def send_email(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email_form.save()

            ## Sending an email

            ## Display a success message
            messages.success(request,'Email Send Successfully')
            return redirect('send_email')
    else:
        email_form = EmailForm()
        context ={
            'email_form' : email_form,
        }
        return render(request,'emails/send-email.html', context)