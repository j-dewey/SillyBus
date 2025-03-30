import os.path
import json
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class TaskObject:

    # Scopes for API access
    SCOPES = ["https://www.googleapis.com/auth/tasks"]

    def __init__(self):
        """Initialize the TaskObject with Google API credentials."""
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google API and build the service."""
        creds = None
        # The file token.json stores the user's access and refresh tokens
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)

        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)  # Running on port 0

            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            self.service = build("tasks", "v1", credentials=creds)
        except HttpError as err:
            print(f"An error occurred during service initialization: {err}")
            raise

    def call(self, data):
        if not self.service:
            raise ValueError("Service not initialized. Authentication may have failed.")

        try:
            # Create the task list
            task_list_body = {
                'title': data['parent']
            }
            task_list = self.service.tasklists().insert(body=task_list_body).execute()
            print(f"Created task list: {task_list['title']} (ID: {task_list['id']})")

            # Add tasks to the task list
            created_tasks = self._add_tasks_to_list(task_list['id'], data['tasks'])

            return {
                'task_list': task_list,
                'tasks': created_tasks
            }

        except HttpError as err:
            print(f"An error occurred while creating tasks: {err}")
            raise

    def _add_tasks_to_list(self, task_list_id, tasks):
        created_tasks = []

        for task in tasks:
            try:
                # Format the due date properly for the API
                due_date = datetime.fromisoformat(task['dueDate'].replace('-05:00', '-0500'))
                formatted_due = due_date.strftime("%Y-%m-%dT00:00:00.000Z")

                task_body = {
                    'title': task['title'],
                    'due': formatted_due,
                    'status': 'needsAction'
                }

                new_task = self.service.tasks().insert(tasklist=task_list_id, body=task_body).execute()
                print(f"Added task: {new_task['title']} (Due: {new_task.get('due', 'No due date')})")
                created_tasks.append(new_task)

            except Exception as e:
                print(f"Error adding task '{task['title']}': {e}")
                # Continue with other tasks even if one fails

        return created_tasks

# Example usage
if __name__ == "__main__":
    pass
