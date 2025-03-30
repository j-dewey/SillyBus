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

    print(extracted_text)
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "sonar",
        "messages": [
            {"role": "user", "content": f"find the important dates in this syllabus and output in JSON files with these keys: 1. parent:the name of the class 2. tasks: all the important dates. with title and due date, the due date should in format RFC3339. Only output the final json format, no other things{extracted_text}"}
        ],
        "max_tokens": 1000
    }
    key = env.get('KEYFORPERP') 
    headers = {
        "Authorization": f"Bearer {key}", 
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return(response.json())