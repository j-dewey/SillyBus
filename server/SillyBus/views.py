from django.views.generic.base import TemplateResponse

def root(request):
    cntxt = {}
    return TemplateResponse(request, 'index.html', cntxt)
