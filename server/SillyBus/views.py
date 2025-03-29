from django.http import HttpResponse
from django.views.generic.base import TemplateResponse

def root(request):
    cntxt = {}
    return TemplateResponse(request, 'index.html', cntxt)

def happy_upload(request):
    cntxt = {}
    return TemplateResponse(request, 'index.html', cntxt)

def file_upload(request):
    print(request)
    return happy_upload(request)
