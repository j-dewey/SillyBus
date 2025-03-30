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

# returns start, end
def format_date(date: str) -> tuple[str, str]:
    month_day = date[5:10]
    return (f"2025-{month_day}T00:00:00-00:00", f"2025-{month_day}23:59:59+59:59")

def load_to_calendar(to_load: dict[str, Any], user_data):
    creds = Credentials(token=user_data)
    service = build('tasks', 'v1', credentials=creds)
    course: str = to_load['parent']
    assignments: list[dict[str,str]] = to_load['tasks']

    # Create the task list
    task_list = service.tasklists().insert(body={ 'title': course }).execute()
    # Add tasks to the task list
    created_tasks = self._add_tasks_to_list(task_list['id'], data['tasks'])

    for t in assignments:
        name = course + ' / ' + t['title']

        # Format the due date properly for the API
        due_date = datetime.fromisoformat(t['dueDate'].replace('-05:00', '-0500'))
        formatted_due = due_date.strftime("%Y-%m-%dT00:00:00.000Z")

        task_body = {
            'title': t['title'],
            'due': formatted_due,
            'status': 'needsAction'
        }

        new_task = service.tasks().insert(tasklist=t['title'], body=task_body).execute()
        print(f"Added task: {new_task['title']} (Due: {new_task.get('due', 'No due date')})")
        created_tasks.append(new_task)
