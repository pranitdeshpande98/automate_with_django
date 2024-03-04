from django.conf import settings
from django.shortcuts import redirect, render
from django.core.management import call_command
from dataentry.utils import get_all_custom_models
from uploads.models import Upload
from django.contrib import messages
from . tasks import import_data_task

# Create your views here.
def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        ## Store this file in the upload model
        upload = Upload.objects.create(file = file_path, model_name = model_name)
        ## Construct full path
        relative_path = str(upload.file.url)
        base_url = str(settings.BASE_DIR)
        import os

        base_url = str(settings.BASE_DIR).replace('\\', '/')
        file_path = base_url+relative_path
        
        ## Handle the import data task here
        import_data_task.delay(file_path,model_name)

        messages.success(request,'Your data is being imported and you will be notified when it is done')
        return redirect('import_data')
    
    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models,
        }

    return render(request,'dataentry/importdata.html',context=context)
