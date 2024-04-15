from django import forms
from .models import UploadedFile

class UploadFileForm(forms.Form):
    file = forms.FileField()



class DocumentForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
        # widgets = {
        #     # 'file_name': forms.HiddenInput(),  # Optionally hide this if set automatically
        # }