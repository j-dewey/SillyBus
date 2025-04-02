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
from .g_calendar import init_service, load_to_calendar

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
        init_service()
        for name, file in files.items():
            parsed = parse_file(file) # Asks perplexity to parse
            for resp in parsed:
                str_content = resp['message']['content']

                # Try to find the actual JSON boundaries
                try:
                    start_idx = str_content.find('{')
                    end_idx = str_content.rfind('}') + 1
                    json_content = str_content[start_idx:end_idx]

                    # Debug the JSON content
                    lines = json_content.split('\n')

                    if len(json_content) > 741:
                        context_start = max(0, 741 - 20)
                        context_end = min(len(json_content), 741 + 20)


                    # Try to clean the JSON before parsing
                    cleaned_json = json_content.replace('\n', ' ').replace('\r', '')
                    content = json.loads(cleaned_json)
                    try:
                        load_to_calendar(content, user)
                    except Exception as e:
                        pass

                except json.JSONDecodeError as e:
                    print(f"\nJSON Error: {e}")
                    print(f"Error position: {e.pos}")
                    print(f"Error line: {e.lineno}")
                    print(f"Error column: {e.colno}")
                    raise

    return HttpResponse(status=204)


@csrf_exempt
def sign_in(request):
    return render(request, 'sign_in.html')

@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
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
    return redirect('/')

def sign_out(request):
    del request.session['user_data']
    return redirect('sign_in')
