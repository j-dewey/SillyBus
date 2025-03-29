from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.generic.base import HttpResponse, TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from .parse import parse_file

from dotenv import load_dotenv

load_dotenv()

def root(request):
    cntxt = {}
    return TemplateResponse(request, 'index.html', cntxt)

def happy_upload(request):
    return HttpResponse(status=204)

@csrf_exempt
def file_upload(request):
    if request.method == "POST":
        print(request.FILES)
        files: dict[str, InMemoryUploadedFile ] = request.FILES.dict()
        print(files)
        for name, file in files.items():
            print("Handling file upload...")
            parsed = parse_file(file)
            print(parsed)

    return happy_upload(request)
