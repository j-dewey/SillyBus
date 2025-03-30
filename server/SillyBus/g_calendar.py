from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import json
import os
import tempfile
from typing import Any

SCOPES = [
    "https://www.googleapis.com/auth/tasks"
]

# returns start, end
def format_date(date: str) -> tuple[str, str]:
    month_day = date[5:10]
    return (f"2025-{month_day}T00:00:00-00:00", f"2025-{month_day}23:59:59+59:59")

def load_to_calendar(to_load: dict[str, Any], user_data):
    '''
    # make a temporary file to load from since Credentials can't accept
    # raw str
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, "user.json")
    with open(temp_file_path, "w") as temp_file:
        json.dump(user_data, temp_file)
    '''

    creds = Credentials(token=user_data)
    service = build('tasks', 'v1', credentials=creds)
    course: str = to_load['parent']
    assignments: list[dict[str,str]] = to_load['tasks']
    task_list = service.tasklists()
    for t in assignments:
        name = course + ' / ' + t['title']
        due = format_date(t['dueDate'])
        print(f"t: {title}, due: {due}")
