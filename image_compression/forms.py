from django import forms
from . models import CompressImage

class CompressImageForm(forms.ModelForm):
    class Meta:
        model = CompressImage
        fields = ('orginal_img','quality')

    orginal_img=forms.ImageField(label='Upload an Image')