from django import forms

class FileUploadForm(forms.Form):
    class Meta:
        fields = ['file_name', 'file']
        widgets = {
            'file': forms.FileField(),
            'file_name': forms.CharField(max_length=100)
        }

    file = forms.FileField()
    file_name = forms.CharField(max_length=100)
