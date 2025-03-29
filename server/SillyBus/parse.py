from django.core.files.uploadedfile import InMemoryUploadedFile
from dotenv import load_dotenv
from os import environ as env
import convertapi
import requests

load_dotenv()
def parse_file(file: InMemoryUploadedFile):
    convertapi.api_credentials = env.get("KEYFORCONVERT")
    temp_file_path = f"/tmp/{file.name}"
    with open(temp_file_path, "wb") as temp_file:
        for chunk in file.chunks():
            temp_file.write(chunk)

    result = convertapi.convert('txt', {'File': temp_file_path}, from_format='pdf')
    converted_files = result.save_files("/tmp/")
    converted_txt_path = converted_files[0]
    with open(converted_txt_path, 'r', encoding='utf-8') as f:
        extracted_text = f.read()

    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "sonar",
        "messages": [
            {"role": "user", "content": "find the important dates in this syllabus and output in jason files with these keys: 1. parent:the name of the class 2. tasks: all the important dates. with title and due date, the due date should in format RFC3339. Only give me the final json format, no other things\n{extracted_text}"}
        ],
        "max_tokens": 2000
    }
    headers = {
        "Authorization": f"Bearer {env.get("KEYFORPERP")}", 
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
parse_file()