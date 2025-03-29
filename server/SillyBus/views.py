from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.http import MultiValueDict
from django.views.generic.base import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import FileUploadForm

def root(request):
    cntxt = {}
    return TemplateResponse(request, 'index.html', cntxt)

def happy_upload(request):
    cntxt = {}
    return TemplateResponse(request, 'index.html', cntxt)

@csrf_exempt
def file_upload(request):
    if request.method == "POST":
        print(request.FILES)
        files: dict[str, InMemoryUploadedFile ] = request.FILES.dict()
        print(files)
        for name, file in files.items():
            print("Handling file upload...")

    return happy_upload(request)
