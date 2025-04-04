from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import json
from datetime import datetime
from typing import Any

SCOPES = [
    "https://www.googleapis.com/auth/tasks"
]

TASK_SERVICE: None | Any = None

def init_service():
    global TASK_SERVICE
    if TASK_SERVICE: return
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", SCOPES
    )
    creds = flow.run_local_server(port=50125)  # Running on port 0
    TASK_SERVICE = build('tasks', 'v1', credentials=creds)

# returns start, end
def format_date(date: str) -> tuple[str, str]:
    month_day = date[5:10]
    return (f"2025-{month_day}T00:00:00-00:00", f"2025-{month_day}23:59:59+59:59")

def load_to_calendar(to_load: dict[str, Any], user_data):
    'refresh_token, token_uri, client_id, and client_secret.'
    if not TASK_SERVICE: return
    print(to_load)
    course: str = to_load['parent']
    assignments: list[dict[str,str]] = to_load['tasks']
    print('loaded credentials')
    # Create the task list
    task_list = TASK_SERVICE.tasklists().insert(body={ 'title': course }).execute()
    # Add tasks to the task list
    created_tasks = []
    print('loaded task list')
    for t in assignments:
        # Format the due date properly for the API
        try:
            due_date = datetime.fromisoformat(t['dueDate'].replace('-05:00', '-0500'))
        except KeyError:
            due_date = datetime.fromisoformat(t['due_date'].replace('-05:00', '-0500'))
        formatted_due = due_date.strftime("%Y-%m-%dT00:00:00.000Z")

        task_body = {
            'title': t['title'],
            'due': formatted_due,
            'status': 'needsAction'
        }

        new_task = TASK_SERVICE.tasks().insert(tasklist=task_list['id'], body=task_body).execute()
        print(f"Added task: {new_task['title']} (Due: {new_task.get('due', 'No due date')})")
        created_tasks.append(new_task)
