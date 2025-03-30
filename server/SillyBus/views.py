from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.generic.base import HttpResponse, TemplateResponse
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

from google.oauth2 import id_token
from google.auth.transport import requests

from dotenv import load_dotenv
import json
import os

from .parse import parse_file
from .g_calendar import load_to_calendar

load_dotenv()

def root(request):
    cntxt = {}
    return TemplateResponse(request, 'index.html', cntxt)

@csrf_exempt
def file_upload(request):
    try:
        session: SessionStore = request.session
        user  = session['user_data']
    except KeyError:
        return HttpResponse(status=401)

    if request.method == "POST":
        files: dict[str, InMemoryUploadedFile ] = request.FILES.dict()
        for name, file in files.items():
            print("Handling file upload...")
            parsed = parse_file(file)
            for resp in parsed:
                # data is stored as ```json\n{<actual json>}\n```
                front_pad = 8
                back_pad = 4
                str_content =  resp['message']['content']
                content = json.loads( str_content[front_pad:-back_pad] )
                load_to_calendar(content, user)

    return HttpResponse(status=204)


@csrf_exempt
def sign_in(request):
    return render(request, 'sign_in.html')

@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    print('Inside')
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)

    # In a real app, I'd also save any new user here to the database.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session['user_data'] = user_data
    print('redirecting...')
    return redirect('/')

def sign_out(request):
    del request.session['user_data']
    return redirect('sign_in')
