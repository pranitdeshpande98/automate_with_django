from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from . forms import CompressImageForm
from PIL import Image
import io
# Create your views here.
def compress(request):
    user = request.user
    if request.method == 'POST':
        form = CompressImageForm(request.POST, request.FILES)
        if form.is_valid():
            original_img = form.cleaned_data['orginal_img']
            quality = form.cleaned_data['quality']
            compressed_image = form.save(commit=False)
            compressed_image.user = user
            ## Perform Compression
            img = Image.open(original_img)
            output_format = img.format
            buffer = io.BytesIO()
            img.save(buffer, format=output_format, quality=quality)
            buffer.seek(0)
            ## saving the compressed image inside the model
            compressed_image.compressed_img.save(f'compressed_{original_img}', buffer)

            ## Download the file
            response = HttpResponse(buffer.getvalue(), content_type=f'image/{output_format.lower()}')
            response['Content-Disposition'] = f'attachent; filename=compressed_{original_img}'
            return response
        else:
            ## Handling form error condition
            messages.error(request, 'Invalid values')
            return redirect('compress')
    else:

        form = CompressImageForm
        context ={
            'form' : form,
        }
        return render(request,'image_compression/compress.html', context)