from django.core.files.uploadedfile import InMemoryUploadedFile
from dotenv import load_dotenv
from os import environ as env
import convertapi
import requests
import tempfile
import os
import shutil

load_dotenv()

def parse_file(file: InMemoryUploadedFile):
    key = env.get("KEYFORCONVERT")
    convertapi.api_credentials = key
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    try:
        # Use os.path.join for platform-independent path handling
        temp_file_path = os.path.join(temp_dir, file.name)
        
        # Write the uploaded file to the temporary location
        with open(temp_file_path, "wb") as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)

        # Convert to text
        result = convertapi.convert('txt', {'File': temp_file_path}, from_format='pdf')
        converted_files = result.save_files(temp_dir)
        converted_txt_path = converted_files[0]
        
        # Read the converted text
        with open(converted_txt_path, 'r', encoding='utf-8') as f:
            extracted_text = f.read()

        url = "https://api.perplexity.ai/chat/completions"

        payload = {
            "model": "sonar",
            "messages": [
                {"role": "user", "content": f"find the important dates in this syllabus and output in JSON files with these keys: 1. parent:the name of the class 2. tasks: all the important dates. with title and due date, the due date should in format RFC3339. Only output the final json format, no other things{extracted_text}"}
            ],
            "max_tokens": 1000
        }
        perp_key = env.get('KEYFORPERP') 
        headers = {
            "Authorization": f"Bearer {perp_key}", 
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    
    finally:
        # Clean up temporary files in a try-except block to handle any permission issues
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception as e:
            print(f"Warning: Could not clean up temporary files: {e}")